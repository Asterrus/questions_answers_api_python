from dataclasses import dataclass

from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from app.infrastructure.db.models.answer import AnswerModel
from app.infrastructure.db.models.question import QuestionModel


@dataclass(frozen=True, slots=True)
class QuestionDbMapper:
    def to_entity(self, model: QuestionModel) -> QuestionEntity:
        return QuestionEntity(id=model.id, text=model.text, created_at=model.created_at)

    def to_model(self, entity: QuestionEntity) -> QuestionModel:
        return QuestionModel(
            id=entity.id, text=entity.text, created_at=entity.created_at, answers=[]
        )

    def update_model_from_entity(self, model: QuestionModel, entity: QuestionEntity) -> None:
        model.text = entity.text
        model.created_at = entity.created_at


@dataclass(frozen=True, slots=True)
class QuestionWithAnswersDbMapper(QuestionDbMapper):
    def to_entity(self, model: QuestionModel) -> QuestionEntity:
        return QuestionEntity(
            id=model.id,
            text=model.text,
            created_at=model.created_at,
            answers=[
                AnswerEntity(
                    id=answer.id,
                    question_id=answer.question_id,
                    user_id=answer.user_id,
                    text=answer.text,
                    created_at=answer.created_at,
                )
                for answer in model.answers
            ],
        )

    def to_model(self, entity: QuestionEntity) -> QuestionModel:
        return QuestionModel(
            id=entity.id,
            text=entity.text,
            created_at=entity.created_at,
            answers=[
                AnswerModel(
                    id=answer.id,
                    question_id=answer.question_id,
                    user_id=answer.user_id,
                    text=answer.text,
                    created_at=answer.created_at,
                )
                for answer in entity.answers
            ],
        )

    def update_model_from_entity(self, model: QuestionModel, entity: QuestionEntity) -> None:
        model.text = entity.text
        model.created_at = entity.created_at
