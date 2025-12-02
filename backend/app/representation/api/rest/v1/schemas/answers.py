from pydantic import BaseModel


class CreateAnswerRequestSchema(BaseModel):
    text: str
