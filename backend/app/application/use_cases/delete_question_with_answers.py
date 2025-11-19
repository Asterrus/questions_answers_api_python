from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.interfaces.uow import UnitOfWork

logger = structlog.get_logger(__name__)


class QuestionWithAnswersDeleter(Protocol):
    async def delete(self, id: UUID) -> None: ...


@dataclass(frozen=True, slots=True)
class DeleteQuestionWithAnswersUseCase:
    question_repository: QuestionWithAnswersDeleter
    uow: UnitOfWork

    async def execute(self, question_id: UUID) -> None:
        logger.info("Deleting question with answers", question_id=question_id)
        async with self.uow:
            await self.question_repository.delete(question_id)
            await self.uow.commit()
        logger.info("Question with answers deleted", question_id=question_id)
        return None
