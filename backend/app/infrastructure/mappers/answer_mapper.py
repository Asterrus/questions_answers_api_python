from app.application.dtos.answer import AnswerResponseDTO
from app.domain.entities.answer import AnswerEntity


class AnswerEntityToDtoMapper:
    def to_dto(self, entity: AnswerEntity) -> AnswerResponseDTO:
        return AnswerResponseDTO(
            id=entity.id,
            question_id=entity.question_id,
            user_id=entity.user_id,
            text=entity.text,
        )
