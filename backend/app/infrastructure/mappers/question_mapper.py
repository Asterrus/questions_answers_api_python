from dataclasses import dataclass

from app.application.dtos.question import QuestionsListDTO, QuestionsListItemDTO
from app.domain.entities.question import QuestionEntity


@dataclass(frozen=True, slots=True)
class QuestionEntityToDtoMapper:
    def to_dto(self, entity: list[QuestionEntity]) -> QuestionsListDTO:
        return QuestionsListDTO([QuestionsListItemDTO(id=q.id, text=q.text) for q in entity])
