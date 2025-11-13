import structlog
from fastapi import FastAPI

from app.api.main import api_router
from app.config.logging import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)


app = FastAPI()
app.include_router(api_router)
logger.info("Application started")
