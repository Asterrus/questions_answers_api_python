from typing import Protocol
from uuid import UUID

from app.domain.entities.question import QuestionEntity


class QuestionListReader(Protocol):
    async def get_list(self) -> list[QuestionEntity]: ...


class QuestionByIdReader(Protocol):
    async def get_by_id(self, id: UUID) -> QuestionEntity | None: ...


class QuestionWriter(Protocol):
    async def save(self, entity: QuestionEntity) -> UUID: ...


class QuestionRepository(
    QuestionByIdReader,
    QuestionListReader,
    QuestionWriter,
): ...
