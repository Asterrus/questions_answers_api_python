import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.engine import Transaction
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import Session as SyncSession

from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.db.models.answer import mapper_registry
from app.infrastructure.db.session import create_engine
from tests.fakes.fake_uow import FakeUnitOfWork

load_dotenv()


@pytest.fixture
def fake_uow() -> UnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture(scope="session")
def engine():
    url = os.environ["TEST_DB_URL"]
    return create_engine(url)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(engine):
    """Создаём таблицы перед тестами и удаляем после."""
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(engine: AsyncEngine):
    async with engine.connect() as conn:
        trans = await conn.begin()

        Session = async_session_factory

        async with Session(bind=conn) as s:
            await s.begin_nested()

            @event.listens_for(s.sync_session, "after_transaction_end")
            def restart_savepoint(sync_sess: SyncSession, transaction: Transaction):
                if not transaction.nested:
                    return
                if sync_sess.is_active and sync_sess.get_transaction() is not None:
                    return
                sync_sess.begin_nested()

            try:
                yield s
            finally:
                await trans.rollback()
