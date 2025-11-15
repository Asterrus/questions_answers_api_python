from typing import Annotated

import structlog
from fastapi import APIRouter, Depends

from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.dependencies import get_questions_to_response_mapper, get_questions_use_case
from app.representation.api.rest.v1.mappers.questions import QuestionsListDtoToApiMapper
from app.representation.api.rest.v1.schemas.questions import ListQuestionsResponseSchema

router = APIRouter()


logger = structlog.get_logger(__name__)


@router.get("/questions/", tags=["questions"])
async def list_questions(
    use_case: Annotated[GetQuestionsUseCase, Depends(get_questions_use_case)],
    mapper: Annotated[QuestionsListDtoToApiMapper, Depends(get_questions_to_response_mapper)],
) -> ListQuestionsResponseSchema:
    logger.info("Getting list of questions")
    dto = await use_case.execute()
    logger.info("List of questions retrieved")
    return mapper.to_response(dto)
