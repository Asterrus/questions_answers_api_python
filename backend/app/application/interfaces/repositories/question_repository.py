from typing import Protocol
from uuid import UUID

from app.domain.entities.question import QuestionEntity


class QuestionReader(Protocol):
    async def get_all(self) -> list[QuestionEntity]: ...


class QuestionWriter(Protocol):
    async def save(self, entity: QuestionEntity) -> UUID: ...


class QuestionRepository(
    QuestionReader,
    QuestionWriter,
): ...
