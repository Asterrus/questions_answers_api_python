from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.application.interfaces.mappers import QuestionWithAnswersEntityToDtoMapper
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity


class QuestionWithAnswersDeleter(Protocol):
    async def delete_with_answers_by_id(
        self, id: UUID
    ) -> tuple[QuestionEntity | None, list[AnswerEntity]]: ...


@dataclass(frozen=True, slots=True)
class DeleteQuestionWithAnswersUseCase:
    question_repository: QuestionWithAnswersDeleter
    question_mapper: QuestionWithAnswersEntityToDtoMapper

    async def execute(self, question_id: UUID) -> QuestionWithAnswersResponseDTO | None:
        del_question, del_answers = await self.question_repository.delete_with_answers_by_id(
            question_id
        )
        if not del_question:
            return None
        return self.question_mapper.to_dto(
            question=del_question,
            answers=del_answers,
        )
