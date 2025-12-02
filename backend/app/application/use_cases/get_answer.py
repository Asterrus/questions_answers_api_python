from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

import structlog

from app.application.dtos.answer import AnswerResponseDTO
from app.application.exceptions import AnswerNotFound
from app.domain.entities.answer import AnswerEntity

logger = structlog.get_logger(__name__)


class AnswerEntityToDtoMapper(Protocol):
    def to_dto(
        self,
        entity: AnswerEntity,
    ) -> AnswerResponseDTO: ...


class AnswerByIdReader(Protocol):
    async def get_by_id(self, id: UUID) -> AnswerEntity | None: ...


@dataclass(frozen=True, slots=True)
class GetAnswerUseCase:
    answer_mapper: AnswerEntityToDtoMapper
    answer_repository: AnswerByIdReader

    async def execute(self, answer_id: UUID) -> AnswerResponseDTO:
        logger.info("Getting answer", answer_id=answer_id)
        answer = await self.answer_repository.get_by_id(answer_id)
        if not answer:
            logger.warning("Answer not found", answer_id=answer_id)
            raise AnswerNotFound(f"Answer with id {answer_id} not found.")
        logger.info("Answer retrieved", answer_id=answer_id)
        return self.answer_mapper.to_dto(answer)
