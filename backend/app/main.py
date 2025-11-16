import structlog
from dishka import make_async_container
from dishka.integrations.fastapi import FromDishka, inject, setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI

from app.config.ioc.main import get_providers
from app.config.logging import setup_logging
from app.representation.api.rest.v1.routes.answers import router as answers_router
from app.representation.api.rest.v1.routes.questions import router as questions_router

load_dotenv()
setup_logging()
logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(answers_router)
    app.include_router(questions_router)
    return app


def create_production_app() -> FastAPI:
    app = create_app()
    container = make_async_container(*get_providers())
    setup_dishka(container, app)
    return app


app = create_production_app()
logger.info("Application started")
