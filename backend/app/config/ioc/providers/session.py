import os
from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.infrastructure.db.session import create_engine, get_session_factory


class SessionProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_engine(self) -> AsyncEngine:
        print(">>> GET ENGINE CALLED!")
        postgres_user = os.getenv("POSTGRES_USER")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_port = os.getenv("POSTGRES_PORT")
        postgres_db = os.getenv("POSTGRES_DB")
        database_url = f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
        engine: AsyncEngine = create_engine(database_url, is_echo=True)
        return engine

    @provide
    async def get_session(
        self,
        engine: AsyncEngine,
    ) -> AsyncGenerator[AsyncSession]:
        print(">>> GET SESSION CALLED!")
        session_factory = get_session_factory(engine)
        async with session_factory() as session:
            yield session
