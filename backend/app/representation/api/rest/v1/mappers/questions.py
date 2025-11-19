from dataclasses import dataclass

from app.application.dtos.question import QuestionsListDTO, QuestionWithAnswersResponseDTO
from app.representation.api.rest.v1.schemas.questions import (
    AnswerListItem,
    GetQuestionWithAnswersResponseSchema,
    ListQuestionsResponseSchema,
    QuestionsListItem,
)


@dataclass(frozen=True, slots=True)
class QuestionsListDtoToApiMapper:
    def to_response(self, dto: QuestionsListDTO) -> ListQuestionsResponseSchema:
        return ListQuestionsResponseSchema(
            [
                QuestionsListItem(
                    id=q.id,
                    text=q.text,
                    created_at=q.created_at,
                )
                for q in dto
            ]
        )


@dataclass(frozen=True, slots=True)
class QuestionWithAnswersDtoToApiMapper:
    def to_response(
        self, dto: QuestionWithAnswersResponseDTO
    ) -> GetQuestionWithAnswersResponseSchema:
        return GetQuestionWithAnswersResponseSchema(
            id=dto.id,
            text=dto.text,
            created_at=dto.created_at,
            answers=[
                AnswerListItem(
                    id=a.id,
                    text=a.text,
                    created_at=a.created_at,
                )
                for a in dto.answers
            ],
        )
