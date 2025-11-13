from typing import Protocol

from app.application.dtos.question import QuestionWithAnswersResponseDTO
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity


class QuestionWithAnswersEntityToDtoMapper(Protocol):
    def to_dto(
        self,
        question: QuestionEntity,
        answers: list[AnswerEntity],
    ) -> QuestionWithAnswersResponseDTO: ...
