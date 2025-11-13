#!/usr/bin/env python3
"""Run Alembic migrations."""
import asyncio
import logging
import os
import sys
from time import sleep

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def wait_for_db(database_url: str, max_retries: int = 30) -> None:
    """Wait for database to be ready."""
    for i in range(max_retries):
        try:
            engine = create_async_engine(database_url)
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            logger.info("Database is ready!")
            return
        except Exception as e:
            if i < max_retries - 1:
                logger.info(f"Waiting for database... ({i+1}/{max_retries})")
                sleep(1)
            else:
                logger.error(f"Failed to connect to database: {e}")
                sys.exit(1)


def main() -> None:
    """Run migrations."""
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Construct from individual env vars
        postgres_user = os.getenv("POSTGRES_USER", "postgres")
        postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        postgres_db = os.getenv("POSTGRES_DB", "postgres")
        postgres_host = os.getenv("POSTGRES_HOST", "db")
        postgres_port = os.getenv("POSTGRES_PORT", "5432")
        database_url = f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    logger.info("Waiting for database to be ready...")
    asyncio.run(wait_for_db(database_url))

    logger.info("Running migrations...")
    os.system("alembic upgrade head")
    logger.info("Migrations completed successfully!")


if __name__ == "__main__":
    main()

