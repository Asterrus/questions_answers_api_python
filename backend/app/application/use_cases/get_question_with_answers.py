from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.exceptions import QuestionNotFound
from app.application.interfaces.mappers import (
    QuestionWithAnswersEntityToDtoMapper,
)
from app.application.interfaces.uow import UnitOfWork
from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class QuestionWithAnswersReaderById(Protocol):
    async def get_by_id_with_answers(self, id: UUID) -> QuestionEntity | None: ...


@dataclass(frozen=True, slots=True)
class GetQuestionWithAnswersUseCase:
    question_repository: QuestionWithAnswersReaderById
    question_mapper: QuestionWithAnswersEntityToDtoMapper
    uow: UnitOfWork

    async def execute(self, question_id: UUID) -> QuestionWithAnswersResponseDTO:
        logger.info("Getting question with answers", question_id=question_id)

        async with self.uow:
            question = await self.question_repository.get_by_id_with_answers(question_id)
            if not question:
                raise QuestionNotFound(question_id)

            logger.info("Question with answers retrieved", question_id=question_id)
            await self.uow.commit()
            return self.question_mapper.to_dto(
                entity=question,
            )
