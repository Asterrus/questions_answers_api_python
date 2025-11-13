from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

logger = structlog.get_logger(__name__)


class AnswerDeleter(Protocol):
    async def delete(self, id: UUID) -> None: ...


@dataclass(frozen=True, slots=True)
class DeleteAnswerUseCase:
    answer_repository: AnswerDeleter

    async def execute(self, answer_id: UUID) -> None:
        logger.info("Deleting answer", answer_id=answer_id)
        await self.answer_repository.delete(answer_id)
        logger.info("Answer deleted", answer_id=answer_id)
