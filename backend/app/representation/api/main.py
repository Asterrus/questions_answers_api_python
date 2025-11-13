from fastapi import APIRouter

from app.api.routes import answers, questions, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(answers.router)
api_router.include_router(questions.router)
