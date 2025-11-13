import structlog
from fastapi import FastAPI

from app.config.logging import setup_logging
from app.representation.api.rest.v1.routes.answers import router as answers_router
from app.representation.api.rest.v1.routes.questions import router as questions_router

setup_logging()
logger = structlog.get_logger(__name__)


app = FastAPI()
app.include_router(answers_router)
app.include_router(questions_router)
logger.info("Application started")
