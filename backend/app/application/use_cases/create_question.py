from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

import structlog

from app.application.interfaces.uow import UnitOfWork
from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class QuestionWriter(Protocol):
    async def add(self, entity: QuestionEntity) -> UUID: ...


@dataclass(frozen=True)
class CreateQuestionCommand:
    text: str


@dataclass(frozen=True, slots=True)
class CreateQuestionUseCase:
    question_repository: QuestionWriter
    uow: UnitOfWork

    async def execute(self, cmd: CreateQuestionCommand) -> UUID:
        logger.info("Creating question", text=cmd.text)
        async with self.uow:
            entity = QuestionEntity(
                id=uuid4(),
                text=cmd.text,
            )
            await self.question_repository.add(entity)
            logger.info("Question created", question_id=entity.id)
            await self.uow.commit()
            return entity.id
