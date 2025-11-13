from typing import Protocol

from app.application.dtos.question import QuestionsListResponseDTO, QuestionWithAnswersResponseDTO
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity


class QuestionDtoToEntityMapper(Protocol):
    def to_entity(self, dto: QuestionsListResponseDTO) -> QuestionEntity: ...


class QuestionEntityToDtoMapper(Protocol):
    def to_dto(self, entity: QuestionEntity) -> QuestionsListResponseDTO: ...


class QuestionWithAnswersEntityToDtoMapper(Protocol):
    def to_dto(
        self,
        question: QuestionEntity,
        answers: list[AnswerEntity],
    ) -> QuestionWithAnswersResponseDTO: ...


class DtoEntityMapper(
    QuestionDtoToEntityMapper,
    QuestionEntityToDtoMapper,
): ...
