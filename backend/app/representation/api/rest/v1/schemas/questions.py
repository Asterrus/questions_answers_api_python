from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.application.dtos.question import QuestionsListDTO, QuestionWithAnswersResponseDTO


class QuestionsListItem(BaseModel):
    id: UUID
    text: str
    created_at: datetime


class ListQuestionsResponseSchema(BaseModel):
    questions: list[QuestionsListItem]

    @classmethod
    def from_dto(
        cls,
        dto: QuestionsListDTO,
    ) -> "ListQuestionsResponseSchema":
        return cls(
            questions=[
                QuestionsListItem(
                    id=q.id,
                    text=q.text,
                    created_at=q.created_at,
                )
                for q in dto
            ]
        )


class CreateQuestionRequestSchema(BaseModel):
    text: str


class AnswerListItem(BaseModel):
    id: UUID
    text: str
    created_at: datetime


class GetQuestionWithAnswersResponseSchema(BaseModel):
    id: UUID
    text: str
    created_at: datetime
    answers: list[AnswerListItem]

    @classmethod
    def from_dto(
        cls,
        dto: QuestionWithAnswersResponseDTO,
    ) -> "GetQuestionWithAnswersResponseSchema":
        return cls(
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
