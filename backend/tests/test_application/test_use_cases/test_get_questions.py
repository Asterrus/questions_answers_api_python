from uuid import uuid4

import pytest

from app.application.dtos.question import QuestionsListDTO, QuestionsListItemDTO
from app.application.use_cases.get_questions import GetQuestionsUseCase
from app.domain.entities.question import QuestionEntity


class FakeQuestionsListReader:
    async def get_list(self):
        return [
            QuestionEntity(id=uuid4(), text="What is your name?"),
        ]


class FakeQuestionMapper:
    def to_dto(self, entity: list[QuestionEntity]) -> QuestionsListDTO:
        return QuestionsListDTO([QuestionsListItemDTO(id=q.id, text=q.text) for q in entity])


class TestGetQuestions:
    @pytest.mark.asyncio
    async def test_get_questions_success(self):
        repo = FakeQuestionsListReader()
        mapper = FakeQuestionMapper()
        use_case = GetQuestionsUseCase(
            question_repository=repo,
            question_mapper=mapper,
        )
        result = await use_case.execute()
        assert len(result) == 1
        assert isinstance(result[0], QuestionsListItemDTO)
