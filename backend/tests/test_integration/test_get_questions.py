from datetime import UTC, datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.application.dtos.question import QuestionsListItemDTO
from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.infrastructure.db.mappers.question_db_mapper import (
    QuestionDbMapper,
    QuestionWithAnswersDbMapper,
)
from app.infrastructure.db.models.question import QuestionModel
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository
from app.infrastructure.mappers.question_mapper import QuestionEntityToDtoMapper


@pytest_asyncio.fixture
async def question_repository(session):
    return SQLAlchemyQuestionRepository(
        session=session,
        mapper=QuestionDbMapper(),
        mapper_with_answers=QuestionWithAnswersDbMapper(),
    )


class TestGetQuestions:
    @pytest.mark.asyncio
    async def test_get_questions_success(self, session, question_repository):
        mapper = QuestionEntityToDtoMapper()

        question = QuestionModel(
            id=uuid4(), text="Test question", created_at=datetime.now(UTC), answers=[]
        )
        session.add(question)
        await session.commit()

        use_case = GetQuestionsUseCase(
            question_repository=question_repository,
            question_mapper=mapper,
        )

        result = await use_case.execute()

        assert len(result) == 1
        assert isinstance(result[0], QuestionsListItemDTO)
