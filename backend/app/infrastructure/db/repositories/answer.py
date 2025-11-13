from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.answer import AnswerEntity
from app.infrastructure.db.exceptions import RepositoryAddError, RepositoryRetrievalError
from app.infrastructure.db.mappers.answer_db_mapper import AnswerDbMapper
from app.infrastructure.db.models.answer import AnswerModel


@dataclass(frozen=True, slots=True)
class AnswerRepositorySQLAlchemy:
    session: AsyncSession
    mapper: AnswerDbMapper

    async def get_by_id(self, id: UUID) -> AnswerEntity | None:
        try:
            stmt = select(AnswerModel).where(AnswerModel.id == id)
            result = await self.session.execute(stmt)
            answer_model = result.scalar_one_or_none()
            if answer_model is None:
                return None
            return self.mapper.to_entity(answer_model)
        except SQLAlchemyError as e:
            raise RepositoryRetrievalError(f"Error retrieving Answer: {e}") from e

    async def add(self, entity: AnswerEntity) -> None:
        try:
            stmt = select(AnswerModel).where(AnswerModel.id == entity.id)
            result = await self.session.execute(stmt)
            answer_model = result.scalar_one_or_none()
            if answer_model:
                self.mapper.update_model_from_entity(answer_model, entity)
            else:
                answer_model = self.mapper.to_model(entity)
            self.session.add(answer_model)
        except SQLAlchemyError as e:
            raise RepositoryAddError(f"Error saving Answer: {e}") from e

    async def delete(self, id: UUID) -> None:
        stmt = delete(AnswerModel).where(AnswerModel.id == id)
        await self.session.execute(stmt)

    async def get_by_question_id(self, question_id: UUID) -> list[AnswerEntity]:
        try:
            stmt = select(AnswerModel).where(AnswerModel.question_id == question_id)
            result = await self.session.execute(stmt)
            answer_models = result.scalars().all()
            return [self.mapper.to_entity(answer_model) for answer_model in answer_models]
        except SQLAlchemyError as e:
            raise RepositoryRetrievalError(f"Error retrieving list of Answers: {e}") from e
