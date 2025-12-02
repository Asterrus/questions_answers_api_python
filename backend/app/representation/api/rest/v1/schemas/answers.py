from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateAnswerRequestSchema(BaseModel):
    text: str


class GetAnswerResponseSchema(BaseModel):
    question_id: UUID
    user_id: UUID
    text: str
    created_at: datetime
