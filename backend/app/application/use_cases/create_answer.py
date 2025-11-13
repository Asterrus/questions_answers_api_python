from dataclasses import dataclass
from typing import Protocol
from uuid import UUID, uuid4

import structlog

from app.application.exceptions import QuestionNotFoundError
from app.application.interfaces.uow import UnitOfWorkProtocol
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity

logger = structlog.get_logger(__name__)


class AnswerWriter(Protocol):
    async def add(self, entity: AnswerEntity) -> UUID: ...


class QuestionReader(Protocol):
    async def get_by_id(self, id: UUID) -> QuestionEntity | None: ...


@dataclass(frozen=True)
class CreateAnswerCommand:
    question_id: UUID
    user_id: UUID
    text: str


@dataclass(frozen=True, slots=True)
class CreateAnswerUseCase:
    question_repository: QuestionReader
    answer_repository: AnswerWriter
    uow: UnitOfWorkProtocol

    async def execute(self, cmd: CreateAnswerCommand) -> UUID:
        logger.info("Creating answer", question_id=cmd.question_id, user_id=cmd.user_id)
        async with self.uow:
            question = await self.question_repository.get_by_id(cmd.question_id)
            if question is None:
                logger.error("Question not found", question_id=cmd.question_id)
                raise QuestionNotFoundError(f"Question with id {cmd.question_id} not found.")

            entity = AnswerEntity(
                id=uuid4(),
                question_id=cmd.question_id,
                user_id=cmd.user_id,
                text=cmd.text,
            )
            await self.answer_repository.add(entity)
            logger.info("Answer created", answer_id=entity.id)
            await self.uow.commit()
            return entity.id
