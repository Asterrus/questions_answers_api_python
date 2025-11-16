import structlog
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.representation.api.rest.v1.mappers.questions import QuestionsListDtoToApiMapper
from app.representation.api.rest.v1.schemas.questions import ListQuestionsResponseSchema

router = APIRouter()


logger = structlog.get_logger(__name__)


@router.get("/questions/", tags=["questions"])
@inject
async def list_questions(
    use_case: FromDishka[GetQuestionsUseCase],
    mapper: FromDishka[QuestionsListDtoToApiMapper],
) -> ListQuestionsResponseSchema:
    logger.info("Getting list of questions")
    dto = await use_case.execute()
    logger.info("List of questions retrieved")
    return mapper.to_response(dto)
