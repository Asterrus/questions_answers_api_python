from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QuestionsListItem(BaseModel):
    id: UUID
    text: str
    created_at: datetime


ListQuestionsResponseSchema = list[QuestionsListItem]


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
