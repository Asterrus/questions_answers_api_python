from uuid import UUID

import pytest

from app.application.use_cases.create_question import CreateQuestionCommand, CreateQuestionUseCase
from app.domain.entities.question import QuestionEntity
from app.domain.excaptions import DomainValidationError
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeQuestionReader:
    def __init__(self):
        self.saved_entity: QuestionEntity | None = None

    async def add(self, entity: QuestionEntity) -> UUID:
        self.saved_entity = entity
        return entity.id


class TestCreateQuestion:
    @pytest.mark.asyncio
    async def test_create_question_success(self, fake_uow: FakeUnitOfWork):
        repo = FakeQuestionReader()
        use_case = CreateQuestionUseCase(
            question_repository=repo,
            uow=fake_uow,
        )
        cmd = CreateQuestionCommand(text="What is your favorite color?")
        result = await use_case.execute(cmd)
        assert isinstance(result, UUID)
        assert repo.saved_entity is not None
        assert repo.saved_entity.id == result

    @pytest.mark.asyncio
    async def test_create_question_empty_text(self, fake_uow: FakeUnitOfWork):
        repo = FakeQuestionReader()
        use_case = CreateQuestionUseCase(
            question_repository=repo,
            uow=fake_uow,
        )
        cmd = CreateQuestionCommand(text="")
        with pytest.raises(DomainValidationError):
            await use_case.execute(cmd)
