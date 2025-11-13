from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.interfaces.uow import UnitOfWorkProtocol

logger = structlog.get_logger(__name__)


class AnswerDeleter(Protocol):
    async def delete(self, id: UUID) -> None: ...


@dataclass(frozen=True, slots=True)
class DeleteAnswerUseCase:
    answer_repository: AnswerDeleter
    uow: UnitOfWorkProtocol

    async def execute(self, answer_id: UUID) -> None:
        logger.info("Deleting answer", answer_id=answer_id)
        async with self.uow:
            await self.answer_repository.delete(answer_id)
        logger.info("Answer deleted", answer_id=answer_id)
