from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.exceptions import QuestionNotFound


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(QuestionNotFound)
    async def question_not_found_handler(_: Request, exc: QuestionNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
