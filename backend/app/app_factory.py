from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.config.ioc.main import get_providers
from app.representation.api.rest.v1.routes.answers import router as answers_router
from app.representation.api.rest.v1.routes.questions import router as questions_router

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(answers_router)
    app.include_router(questions_router)
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    container = make_async_container(*get_providers())
    setup_dishka(container, app)
    return app
