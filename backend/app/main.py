from fastapi import FastAPI

from app.routers.answers import router as answers_router
from app.routers.questions import router as questions_router
from app.routers.users import router as users_router

app = FastAPI()
app.include_router(answers_router)
app.include_router(questions_router)
app.include_router(users_router)
