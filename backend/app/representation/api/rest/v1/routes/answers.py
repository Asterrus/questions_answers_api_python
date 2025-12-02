from uuid import UUID, uuid4

import structlog
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.application.use_cases.create_answer import CreateAnswerCommand, CreateAnswerUseCase
from app.application.use_cases.delete_answer import DeleteAnswerUseCase
from app.application.use_cases.get_answer import GetAnswerUseCase
from app.representation.api.rest.v1.mappers.answers import AnswerDtoToApiMapper
from app.representation.api.rest.v1.schemas.answers import (
    CreateAnswerRequestSchema,
    GetAnswerResponseSchema,
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


@router.get(
    "/answers/{id}",
    tags=["answers"],
    status_code=200,
)
@inject
async def get_answer(
    use_case: FromDishka[GetAnswerUseCase],
    mapper: FromDishka[AnswerDtoToApiMapper],
    id: UUID,
) -> GetAnswerResponseSchema:
    "получить конкретный ответ"
    answer = await use_case.execute(id)
    return mapper.to_response(answer)


@router.delete(
    "/answers/{id}",
    tags=["answers"],
    status_code=204,
)
@inject
async def delete_answer(
    use_case: FromDishka[DeleteAnswerUseCase],
    id: UUID,
):
    "получить конкретный ответ"
    await use_case.execute(id)
    return None
