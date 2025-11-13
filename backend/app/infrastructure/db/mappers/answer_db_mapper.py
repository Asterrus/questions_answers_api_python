from dataclasses import dataclass

from app.domain.entities.answer import AnswerEntity
from app.infrastructure.db.models.answer import AnswerModel


@dataclass(frozen=True, slots=True)
class AnswerDbMapper:
    def to_entity(self, model: AnswerModel) -> AnswerEntity:
        return AnswerEntity(
            id=model.id,
            question_id=model.question_id,
            user_id=model.user_id,
            text=model.text,
            created_at=model.created_at,
        )

    def to_model(self, entity: AnswerEntity) -> AnswerModel:
        return AnswerModel(
            id=entity.id,
            question_id=entity.question_id,
            user_id=entity.user_id,
            text=entity.text,
            created_at=entity.created_at,
        )

    def update_model_from_entity(self, model: AnswerModel, entity: AnswerEntity) -> None:
        model.text = entity.text
        model.created_at = entity.created_at
        model.question_id = entity.question_id
        model.user_id = entity.user_id
