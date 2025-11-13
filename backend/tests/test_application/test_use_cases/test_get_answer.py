import asyncio
from uuid import UUID, uuid4

import pytest

from app.application.dtos.question import (
    AnswerResponseDTO,
)
from app.application.use_cases.get_answer import GetAnswerUseCase
from app.domain.entities.answer import AnswerEntity


class FakeAnswerByIdReader:
    def __init__(self, answer: AnswerEntity | None = None):
        self.answer = answer

    async def get_by_id(self, id: UUID) -> AnswerEntity | None:
        return self.answer


class FakeAnswerEntityToDtoMapper:
    def to_dto(self, entity: AnswerEntity) -> AnswerResponseDTO:
        return AnswerResponseDTO(
            id=entity.id,
            question_id=entity.question_id,
            user_id=entity.user_id,
            text=entity.text,
        )


class TestGetQuestionWithAnswersUseCase:
    @pytest.mark.asyncio
    async def test_get_answer_success(self):
        answer = AnswerEntity(
            id=uuid4(),
            question_id=uuid4(),
            user_id=uuid4(),
            text="Blue",
        )

        answer_repo = FakeAnswerByIdReader(answer=answer)
        mapper = FakeAnswerEntityToDtoMapper()

        use_case = GetAnswerUseCase(
            answer_mapper=mapper,
            answer_repository=answer_repo,
        )
        result = await use_case.execute(answer.id)
        assert result is not None
        assert isinstance(result, AnswerResponseDTO)
        assert result.id == answer.id
