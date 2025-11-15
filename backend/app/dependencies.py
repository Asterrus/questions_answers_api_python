import os
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository
from app.infrastructure.db.session import create_engine, get_session_factory
from app.infrastructure.mappers.question_mapper import QuestionEntityToDtoMapper
from app.representation.api.rest.v1.mappers.questions import QuestionsListDtoToApiMapper


async def get_engine() -> AsyncEngine:
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT")
    postgres_db = os.getenv("POSTGRES_DB")
    database_url = f"postgresql+psycopg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    engine: AsyncEngine = create_engine(database_url, is_echo=True)
    return engine


async def get_session(
    engine: Annotated[AsyncEngine, Depends(get_engine)],
) -> AsyncGenerator[AsyncSession]:
    session_factory = get_session_factory(engine)

    async with session_factory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


def get_question_repo(
    session: Session,
) -> SQLAlchemyQuestionRepository:
    return SQLAlchemyQuestionRepository(session=session, mapper=QuestionDbMapper())


async def get_question_entity_to_dto_mapper() -> QuestionEntityToDtoMapper:
    return QuestionEntityToDtoMapper()


async def get_questions_use_case(
    question_repository: Annotated[
        SQLAlchemyQuestionRepository,
        Depends(get_question_repo),
    ],
    question_mapper: Annotated[
        QuestionEntityToDtoMapper,
        Depends(get_question_entity_to_dto_mapper),
    ],
) -> GetQuestionsUseCase:
    return GetQuestionsUseCase(
        question_repository=question_repository,
        question_mapper=question_mapper,
    )


async def get_questions_to_response_mapper() -> QuestionsListDtoToApiMapper:
    return QuestionsListDtoToApiMapper()
