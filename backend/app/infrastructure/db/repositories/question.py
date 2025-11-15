from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.question import QuestionEntity
from app.infrastructure.db.exceptions import RepositoryAddError, RepositoryRetrievalError
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.models.question import QuestionModel


@dataclass(frozen=True, slots=True)
class SQLAlchemyQuestionRepository:
    session: AsyncSession
    mapper: QuestionDbMapper

    async def get_by_id(self, id: UUID) -> QuestionEntity | None:
        try:
            stmt = select(QuestionModel).where(QuestionModel.id == id)
            result = await self.session.execute(stmt)
            question_model = result.scalar_one_or_none()
            if question_model is None:
                return None
            return self.mapper.to_entity(question_model)
        except SQLAlchemyError as e:
            raise RepositoryRetrievalError(f"Error retrieving Answer: {e}") from e

    async def add(self, entity: QuestionEntity) -> None:
        try:
            stmt = select(QuestionModel).where(QuestionModel.id == entity.id)
            result = await self.session.execute(stmt)
            question_model = result.scalar_one_or_none()
            if question_model:
                self.mapper.update_model_from_entity(question_model, entity)
            else:
                question_model = self.mapper.to_model(entity)
            self.session.add(question_model)
        except SQLAlchemyError as e:
            raise RepositoryAddError(f"Error saving Question: {e}") from e

    async def delete(self, id: UUID) -> None:
        stmt = delete(QuestionModel).where(QuestionModel.id == id)
        await self.session.execute(stmt)

    async def get_list(self) -> list[QuestionEntity]:
        try:
            stmt = select(QuestionModel)
            result = await self.session.execute(stmt)
            question_models = result.scalars().all()
            return [self.mapper.to_entity(question_model) for question_model in question_models]
        except SQLAlchemyError as e:
            raise RepositoryRetrievalError(f"Error retrieving list of Questions: {e}") from e
