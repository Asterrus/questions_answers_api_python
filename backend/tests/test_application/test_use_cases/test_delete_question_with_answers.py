from uuid import UUID, uuid4

import pytest

from app.application.use_cases.delete_question_with_answers import DeleteQuestionWithAnswersUseCase
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeQuestionWithAnswersDeleter:
    def __init__(self):
        self.deleted_id: UUID | None = None

    async def delete(self, id: UUID) -> None:
        self.deleted_id = id


class TestDeleteQuestionWithAnswersUseCase:
    @pytest.mark.asyncio
    async def test_delete_question_with_answers_success(self, fake_uow: FakeUnitOfWork):
        question_repo = FakeQuestionWithAnswersDeleter()
        uuid = uuid4()
        use_case = DeleteQuestionWithAnswersUseCase(
            question_repository=question_repo,
            uow=fake_uow,
        )

        await use_case.execute(uuid)

        assert question_repo.deleted_id == uuid
