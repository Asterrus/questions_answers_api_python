from typing import Protocol

from app.application.dtos.question import QuestionResponseDTO
from app.domain.entities.question import QuestionEntity


class QuestionDtoToEntityMapper(Protocol):
    def to_entity(self, dto: QuestionResponseDTO) -> QuestionEntity: ...


class QuestionEntityToDtoMapper(Protocol):
    def to_dto(self, entity: QuestionEntity) -> QuestionResponseDTO: ...


class DtoEntityMapper(
    QuestionDtoToEntityMapper,
    QuestionEntityToDtoMapper,
): ...
