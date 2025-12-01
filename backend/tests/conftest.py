import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.orm.session import SessionTransaction

from app.application.interfaces.uow import UnitOfWork
from app.infrastructure.db.config import get_database_url
from app.infrastructure.db.models.answer import mapper_registry
from app.infrastructure.db.session import create_engine
from tests.fakes.fake_uow import FakeUnitOfWork

curr_dir = Path(__file__).parent
env_file_path = curr_dir.parent.parent / ".env.test"

if not env_file_path.exists():
    raise FileNotFoundError(f"Environment file not found: {env_file_path}")

load_dotenv(env_file_path, override=True)


@pytest.fixture
def fake_uow() -> UnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture(scope="session")
def engine():
    url = get_database_url()
    return create_engine(url, is_echo=True)


@pytest_asyncio.fixture(scope="session")
async def wait_for_db(engine: AsyncEngine):
    """Ожидаем, пока база данных станет доступна."""
    max_retries = 5
    for _ in range(max_retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return
        except Exception:
            await asyncio.sleep(1)
    raise RuntimeError("Database is not ready for tests")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database(
    engine: AsyncEngine,
    wait_for_db,  # noqa
):
    """Создаём таблицы перед тестами и удаляем после."""
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)


async_session_factory = async_sessionmaker(engine, expire_on_commit=False)  # type: ignore


@pytest_asyncio.fixture
async def session(engine: AsyncEngine):
    async with engine.connect() as conn:
        trans = await conn.begin()

        Session = async_session_factory

        async with Session(bind=conn) as s:
            await s.begin_nested()

            @event.listens_for(s.sync_session, "after_transaction_end")
            def restart_savepoint(sync_sess: SyncSession, transaction: SessionTransaction):
                if not transaction.nested:
                    return
                if sync_sess.is_active and sync_sess.get_transaction() is not None:
                    return
                sync_sess.begin_nested()

            try:
                yield s
            finally:
                await trans.rollback()
