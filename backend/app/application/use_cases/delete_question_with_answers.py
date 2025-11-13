from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.interfaces.mappers import QuestionWithAnswersEntityToDtoMapper
from app.application.interfaces.uow import UnitOfWorkProtocol
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class QuestionWithAnswersDeleter(Protocol):
    async def delete(self, id: UUID) -> tuple[QuestionEntity | None, list[AnswerEntity]]: ...


@dataclass(frozen=True, slots=True)
class DeleteQuestionWithAnswersUseCase:
    question_repository: QuestionWithAnswersDeleter
    question_mapper: QuestionWithAnswersEntityToDtoMapper
    uow: UnitOfWorkProtocol

    async def execute(self, question_id: UUID) -> QuestionWithAnswersResponseDTO | None:
        logger.info("Deleting question with answers", question_id=question_id)
        async with self.uow:
            del_question, del_answers = await self.question_repository.delete(question_id)
            await self.uow.commit()
        if not del_question:
            logger.warning("Question not found for deletion", question_id=question_id)
            return None
        logger.info("Question with answers deleted", question_id=question_id)
        return self.question_mapper.to_dto(
            question=del_question,
            answers=del_answers,
        )
