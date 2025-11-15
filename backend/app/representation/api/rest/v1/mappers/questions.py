from dataclasses import dataclass

from app.application.dtos.question import QuestionsListDTO
from app.representation.api.rest.v1.schemas.questions import (
    ListQuestionsResponseSchema,
    QuestionsListItem,
)


@dataclass(frozen=True, slots=True)
class QuestionsListDtoToApiMapper:
    def to_response(self, dto: QuestionsListDTO) -> ListQuestionsResponseSchema:
        return ListQuestionsResponseSchema(
            [
                QuestionsListItem(
                    id=str(q.id),
                    text=q.text,
                    created_at=q.created_at,
                )
                for q in dto
            ]
        )
