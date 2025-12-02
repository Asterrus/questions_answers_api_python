from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.application.dtos.answer import AnswerResponseDTO


class CreateAnswerRequestSchema(BaseModel):
    text: str


class GetAnswerResponseSchema(BaseModel):
    question_id: UUID
    user_id: UUID
    text: str
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: AnswerResponseDTO) -> "GetAnswerResponseSchema":
        return cls(
            question_id=dto.question_id,
            user_id=dto.user_id,
            text=dto.text,
            created_at=dto.created_at,
        )
