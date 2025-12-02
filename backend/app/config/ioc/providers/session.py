from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.infrastructure.db.config import get_database_url
from app.infrastructure.db.session import create_engine, get_session_factory


class SessionProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncEngine:
        database_url = get_database_url()
        engine: AsyncEngine = create_engine(database_url, is_echo=True)
        return engine

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        engine: AsyncEngine,
    ) -> AsyncGenerator[AsyncSession]:
        session_factory = get_session_factory(engine)
        async with session_factory() as session:
            yield session
