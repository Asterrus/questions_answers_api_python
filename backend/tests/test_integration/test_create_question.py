from uuid import UUID

import pytest
import pytest_asyncio

from app.application.use_cases.create_question import CreateQuestionCommand, CreateQuestionUseCase
from app.infrastructure.db.mappers.question_db_mapper import (
    QuestionDbMapper,
    QuestionWithAnswersDbMapper,
)
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository
from app.infrastructure.db.uow import SQLAlchemyUnitOfWork


@pytest_asyncio.fixture
async def question_repository(session):
    return SQLAlchemyQuestionRepository(
        session=session,
        mapper=QuestionDbMapper(),
        mapper_with_answers=QuestionWithAnswersDbMapper(),
    )


class TestCreateQuestion:
    @pytest.mark.asyncio
    async def test_create_question_success(self, session, question_repository):
        uow = SQLAlchemyUnitOfWork(session=session)
        use_case = CreateQuestionUseCase(question_repository, uow)
        cmd = CreateQuestionCommand(text="test")

        result = await use_case.execute(cmd)

        assert result
        assert isinstance(result, UUID)
