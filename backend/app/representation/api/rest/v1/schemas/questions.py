from datetime import datetime

from pydantic import BaseModel


class QuestionsListItem(BaseModel):
    id: str
    text: str
    created_at: datetime


ListQuestionsResponseSchema = list[QuestionsListItem]


class CreateQuestionRequestSchema(BaseModel):
    text: str
