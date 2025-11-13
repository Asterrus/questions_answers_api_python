from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.interfaces.mappers import (
    QuestionWithAnswersEntityToDtoMapper,
)
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity


class QuestionByIdReader(Protocol):
    async def get_by_id(self, id: UUID) -> QuestionEntity | None: ...


class AnswersByQuestionIdReader(Protocol):
    async def get_by_question_id(self, id: UUID) -> list[AnswerEntity]: ...


@dataclass(frozen=True, slots=True)
class GetQuestionWithAnswersUseCase:
    question_repository: QuestionByIdReader
    question_mapper: QuestionWithAnswersEntityToDtoMapper
    answer_repository: AnswersByQuestionIdReader

    async def execute(self, question_id: UUID) -> QuestionWithAnswersResponseDTO | None:
        question = await self.question_repository.get_by_id(question_id)
        if not question:
            return None

        answers = await self.answer_repository.get_by_question_id(question_id)

        return self.question_mapper.to_dto(
            question=question,
            answers=answers,
        )
