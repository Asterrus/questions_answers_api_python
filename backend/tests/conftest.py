import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, AsyncTransaction

from app.application.interfaces.uow import UnitOfWorkProtocol
from app.infrastructure.db.models.answer import mapper_registry
from app.infrastructure.db.session import create_engine, get_session_factory
from tests.fakes.fake_uow import FakeUnitOfWork


@pytest.fixture
def fake_uow() -> UnitOfWorkProtocol:
    return FakeUnitOfWork()


@pytest.fixture(scope="session")
def engine():
    load_dotenv()
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


@pytest_asyncio.fixture(scope="session")
async def session(engine: AsyncEngine):
    Session = get_session_factory(engine)
    async with engine.connect() as conn:
        transaction = await conn.begin()
        async with Session(bind=conn) as s:
            try:
                yield s
            finally:
                await transaction.rollback()
