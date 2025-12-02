from dataclasses import dataclass

from app.application.dtos.answer import AnswerResponseDTO
from app.representation.api.rest.v1.schemas.answers import GetAnswerResponseSchema


@dataclass(frozen=True, slots=True)
class AnswerDtoToApiMapper:
    def to_response(self, dto: AnswerResponseDTO) -> GetAnswerResponseSchema:
        return GetAnswerResponseSchema(
            question_id=dto.question_id,
            user_id=dto.user_id,
            text=dto.text,
            created_at=dto.created_at,
        )
