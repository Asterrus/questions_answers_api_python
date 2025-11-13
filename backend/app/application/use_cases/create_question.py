from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

import structlog

from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class QuestionWriter(Protocol):
    async def save(self, entity: QuestionEntity) -> UUID: ...


@dataclass(frozen=True)
class CreateQuestionCommand:
    text: str


@dataclass(frozen=True, slots=True)
class CreateQuestionUseCase:
    question_repository: QuestionWriter

    async def execute(self, cmd: CreateQuestionCommand) -> UUID:
        logger.info("Creating question", text=cmd.text)
        entity = QuestionEntity(
            id=uuid4(),
            text=cmd.text,
        )
        await self.question_repository.save(entity)
        logger.info("Question created", question_id=entity.id)
        return entity.id
