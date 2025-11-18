from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.dtos.question import QuestionsListItemDTO
from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.models.question import QuestionModel
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository
from app.infrastructure.mappers.question_mapper import QuestionEntityToDtoMapper


class TestGetQuestions:
    @pytest.mark.asyncio
    async def test_get_questions_success(self, session):
        repo = SQLAlchemyQuestionRepository(
            session,
            QuestionDbMapper(),
        )
        mapper = QuestionEntityToDtoMapper()

        question = QuestionModel(id=uuid4(), text="Test question", created_at=datetime.now(UTC))
        session.add(question)
        await session.commit()

        use_case = GetQuestionsUseCase(
            question_repository=repo,
            question_mapper=mapper,
        )

        result = await use_case.execute()

        assert len(result) == 1
        assert isinstance(result[0], QuestionsListItemDTO)
