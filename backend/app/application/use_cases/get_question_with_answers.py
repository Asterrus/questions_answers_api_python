from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.question import QuestionsListResponseDTO, QuestionWithAnswersResponseDTO
from app.application.interfaces.mappers import (
    QuestionWithAnswersEntityToDtoMapper,
)
from app.application.interfaces.repositories.answer_repository import AnswersByQuestionIdReader
from app.application.interfaces.repositories.question_repository import QuestionByIdReader


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
