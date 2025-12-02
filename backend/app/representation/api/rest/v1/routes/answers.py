from uuid import UUID, uuid4

import structlog
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.application.use_cases.create_answer import CreateAnswerCommand, CreateAnswerUseCase
from app.representation.api.rest.v1.schemas.answers import (
    CreateAnswerRequestSchema,
)

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post(
    "/questions/{id}/answers/",
    tags=["answers"],
    status_code=201,
)
@inject
async def create_answer(
    use_case: FromDishka[CreateAnswerUseCase],
    id: UUID,
    request: CreateAnswerRequestSchema,
) -> UUID:
    "Создать ответ на вопрос"
    command = CreateAnswerCommand(
        question_id=id,
        user_id=uuid4(),
        text=request.text,
    )
    uuid = await use_case.execute(command)
    return uuid
