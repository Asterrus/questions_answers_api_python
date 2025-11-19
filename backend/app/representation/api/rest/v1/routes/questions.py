from uuid import UUID

import structlog
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.application.use_cases.create_question import CreateQuestionCommand, CreateQuestionUseCase
from app.application.use_cases.delete_question_with_answers import DeleteQuestionWithAnswersUseCase
from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.representation.api.rest.v1.mappers.questions import QuestionsListDtoToApiMapper
from app.representation.api.rest.v1.schemas.questions import (
    CreateQuestionRequestSchema,
    ListQuestionsResponseSchema,
)

router = APIRouter()


logger = structlog.get_logger(__name__)


@router.get("/questions/", tags=["questions"])
@inject
async def list_questions(
    use_case: FromDishka[GetQuestionsUseCase],
    mapper: FromDishka[QuestionsListDtoToApiMapper],
) -> ListQuestionsResponseSchema:
    """список всех вопросов"""
    logger.info("Getting list of questions")
    dto = await use_case.execute()
    logger.info("List of questions retrieved")
    return mapper.to_response(dto)


@router.post("/questions/", tags=["questions"], status_code=201)
@inject
async def create_question(
    request: CreateQuestionRequestSchema,
    use_case: FromDishka[CreateQuestionUseCase],
) -> UUID:
    """создать новый вопрос"""
    logger.info("Creating question")
    cmd = CreateQuestionCommand(text=request.text)
    question_id = await use_case.execute(cmd)
    logger.info("Question created")
    return question_id


@router.delete("/questions/{id}/", tags=["questions"], status_code=204)
@inject
async def delete_question(
    id: UUID,
    use_case: FromDishka[DeleteQuestionWithAnswersUseCase],
) -> None:
    """удалить вопрос"""
    logger.info("Deleting question")
    await use_case.execute(id)
    logger.info("Question deleted")
    return None
