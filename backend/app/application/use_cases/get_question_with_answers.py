from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.interfaces.mappers import (
    QuestionWithAnswersEntityToDtoMapper,
)
from app.application.interfaces.uow import UnitOfWorkProtocol
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class QuestionByIdReader(Protocol):
    async def get_by_id(self, id: UUID) -> QuestionEntity | None: ...


class AnswersByQuestionIdReader(Protocol):
    async def get_by_question_id(self, question_id: UUID) -> list[AnswerEntity]: ...


@dataclass(frozen=True, slots=True)
class GetQuestionWithAnswersUseCase:
    question_repository: QuestionByIdReader
    question_mapper: QuestionWithAnswersEntityToDtoMapper
    answer_repository: AnswersByQuestionIdReader
    uow: UnitOfWorkProtocol

    async def execute(self, question_id: UUID) -> QuestionWithAnswersResponseDTO | None:
        logger.info("Getting question with answers", question_id=question_id)

        async with self.uow:
            question = await self.question_repository.get_by_id(question_id)
            if not question:
                logger.warning("Question not found", question_id=question_id)
                return None

            answers = await self.answer_repository.get_by_question_id(question_id)
            logger.info("Question with answers retrieved", question_id=question_id)
            await self.uow.commit()
            return self.question_mapper.to_dto(
                question=question,
                answers=answers,
            )
