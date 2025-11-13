from uuid import UUID, uuid4

import pytest

from app.application.exceptions import QuestionNotFoundError
from app.application.use_cases.create_answer import CreateAnswerCommand, CreateAnswerUseCase
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeAnswerWriter:
    def __init__(self):
        self.saved_answers = []

    async def add(self, entity: AnswerEntity) -> UUID:
        self.saved_answers.append(entity)
        return entity.id


class FakeQuestionReader:
    def __init__(self, question: QuestionEntity | None = None):
        self.question = question

    async def get_by_id(self, id: UUID) -> QuestionEntity | None:
        return self.question


class TestCreateAnswerUseCase:
    @pytest.mark.asyncio
    async def test_create_answer_success(self, fake_uow: FakeUnitOfWork):
        question = QuestionEntity(
            id=uuid4(),
            text="What is your favorite color?",
        )
        question_repo = FakeQuestionReader(question=question)
        answer_repo = FakeAnswerWriter()

        use_case = CreateAnswerUseCase(
            question_repository=question_repo,
            answer_repository=answer_repo,
            uow=fake_uow,
        )

        cmd = CreateAnswerCommand(
            question_id=question.id,
            user_id=uuid4(),
            text="Blue",
        )
        result = await use_case.execute(cmd)
        assert result is not None
        assert len(answer_repo.saved_answers) == 1
        assert fake_uow.committed

    @pytest.mark.asyncio
    async def test_create_answer_question_not_found(self, fake_uow: FakeUnitOfWork):
        question_repo = FakeQuestionReader()
        answer_repo = FakeAnswerWriter()

        use_case = CreateAnswerUseCase(
            question_repository=question_repo,
            answer_repository=answer_repo,
            uow=fake_uow,
        )

        cmd = CreateAnswerCommand(
            question_id=uuid4(),
            user_id=uuid4(),
            text="Blue",
        )
        with pytest.raises(QuestionNotFoundError):
            await use_case.execute(cmd)
