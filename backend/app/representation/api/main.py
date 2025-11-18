from fastapi import APIRouter

from app.representation.api.rest.v1.routes import questions

api_router = APIRouter()

# api_router.include_router(answers.router)
api_router.include_router(questions.router)
