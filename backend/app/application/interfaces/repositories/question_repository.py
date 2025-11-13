from typing import Protocol

from app.domain.entities.question import QuestionEntity


class QuestionReader(Protocol):
    async def get_all(self) -> list[QuestionEntity]: ...


class QuestionRepository(QuestionReader):
    pass
