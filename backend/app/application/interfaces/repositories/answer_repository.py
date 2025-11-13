from typing import Protocol
from uuid import UUID

from app.domain.entities.answer import AnswerEntity


class AnswersByQuestionIdReader(Protocol):
    async def get_by_question_id(self, id: UUID) -> list[AnswerEntity]: ...
