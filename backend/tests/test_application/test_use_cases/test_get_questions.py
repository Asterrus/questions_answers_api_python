from uuid import uuid4

import pytest

from app.application.dtos.question import QuestionResponseDTO
from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.domain.entities.question import QuestionEntity


class FakeQuestionReader:
    async def get_all(self):
        return [
            QuestionEntity(id=uuid4(), text="What is your name?"),
        ]


class FakeQuestionMapper:
    def to_dto(self, entity: QuestionEntity) -> QuestionResponseDTO:
        return QuestionResponseDTO(id=entity.id, text=entity.text)


class TestGetQuestions:
    @pytest.mark.asyncio
    async def test_get_questions_success(self):
        repo = FakeQuestionReader()
        mapper = FakeQuestionMapper()
        use_case = GetQuestionsUseCase(
            question_repository=repo,
            question_mapper=mapper,
        )
        result = await use_case.execute()
        assert len(result) == 1
        assert isinstance(result[0], QuestionResponseDTO)
