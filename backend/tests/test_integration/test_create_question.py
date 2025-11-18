from uuid import UUID

import pytest

from app.application.use_cases.create_question import CreateQuestionCommand, CreateQuestionUseCase
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository
from app.infrastructure.db.uow import SQLAlchemyUnitOfWork


class TestCreateQuestion:
    @pytest.mark.asyncio
    async def test_create_question_success(self, session):
        repo = SQLAlchemyQuestionRepository(
            session,
            QuestionDbMapper(),
        )
        uow = SQLAlchemyUnitOfWork(session=session)
        use_case = CreateQuestionUseCase(repo, uow)
        cmd = CreateQuestionCommand(text="test")

        result = await use_case.execute(cmd)

        assert result
        assert isinstance(result, UUID)
