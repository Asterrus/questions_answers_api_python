from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

from app.domain.entities.question import QuestionEntity


class QuestionWriter(Protocol):
    async def save(self, entity: QuestionEntity) -> UUID: ...


@dataclass(frozen=True)
class CreateQuestionCommand:
    text: str


@dataclass(frozen=True, slots=True)
class CreateQuestionUseCase:
    question_repository: QuestionWriter

    async def execute(self, cmd: CreateQuestionCommand) -> UUID:
        entity = QuestionEntity(
            id=uuid4(),
            text=cmd.text,
        )
        await self.question_repository.save(entity)
        return entity.id
