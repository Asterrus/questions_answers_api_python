from dataclasses import dataclass

from app.application.dtos.answer import AnswerResponseDTO
from app.application.dtos.question import (
    QuestionsListDTO,
    QuestionsListItemDTO,
    QuestionWithAnswersResponseDTO,
)
from app.domain.entities.question import QuestionEntity


@dataclass(frozen=True, slots=True)
class QuestionEntityToDtoMapper:
    def to_dto(self, entity: list[QuestionEntity]) -> QuestionsListDTO:
        return QuestionsListDTO([QuestionsListItemDTO(id=q.id, text=q.text) for q in entity])


@dataclass(frozen=True, slots=True)
class QuestionWithAnswersEntityToDtoMapper:
    def to_dto(self, entity: QuestionEntity) -> QuestionWithAnswersResponseDTO:
        return QuestionWithAnswersResponseDTO(
            id=entity.id,
            text=entity.text,
            created_at=entity.created_at,
            answers=[
                AnswerResponseDTO(
                    id=a.id,
                    text=a.text,
                    created_at=a.created_at,
                    user_id=a.user_id,
                    question_id=a.question_id,
                )
                for a in entity.answers
            ],
        )
