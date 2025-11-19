from uuid import UUID, uuid4

import pytest

from app.application.dtos.question import (
    AnswerResponseDTO,
    QuestionWithAnswersResponseDTO,
)
from app.application.exceptions import QuestionNotFound
from app.application.use_cases.get_question_with_answers import GetQuestionWithAnswersUseCase
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeQuestionWithAnswersReaderById:
    def __init__(self, question: QuestionEntity | None = None):
        self.question = question

    async def get_by_id_with_answers(self, id: UUID) -> QuestionEntity | None:
        return self.question


class FakeQuestionWithAnswersEntityToDtoMapper:
    def to_dto(self, entity: QuestionEntity) -> QuestionWithAnswersResponseDTO:
        question_answers = [
            AnswerResponseDTO(
                id=answer.id,
                question_id=answer.question_id,
                user_id=answer.user_id,
                text=answer.text,
            )
            for answer in entity.answers
        ]
        return QuestionWithAnswersResponseDTO(
            id=entity.id,
            text=entity.text,
            answers=question_answers,
        )


class TestGetQuestionWithAnswersUseCase:
    @pytest.mark.asyncio
    async def test_get_question_with_answers_success(self, fake_uow: FakeUnitOfWork):
        question_id = uuid4()
        answers = [
            AnswerEntity(id=uuid4(), question_id=question_id, user_id=uuid4(), text="Blue"),
            AnswerEntity(id=uuid4(), question_id=question_id, user_id=uuid4(), text="Green"),
        ]
        question = QuestionEntity(
            id=uuid4(),
            text="What is your favorite color?",
            answers=answers,
        )

        question_repo = FakeQuestionWithAnswersReaderById(question=question)
        mapper = FakeQuestionWithAnswersEntityToDtoMapper()

        use_case = GetQuestionWithAnswersUseCase(
            question_repository=question_repo,
            question_mapper=mapper,
            uow=fake_uow,
        )

        result = await use_case.execute(question_id=question.id)
        assert result is not None
        assert result.id == question.id
        assert result.text == question.text
        assert len(result.answers) == 2
        assert isinstance(result.answers[0], AnswerResponseDTO)
        assert fake_uow.committed

    @pytest.mark.asyncio
    async def test_get_question_with_answers_not_found(self, fake_uow: FakeUnitOfWork):
        question_repo = FakeQuestionWithAnswersReaderById()
        mapper = FakeQuestionWithAnswersEntityToDtoMapper()

        use_case = GetQuestionWithAnswersUseCase(
            question_repository=question_repo,
            question_mapper=mapper,
            uow=fake_uow,
        )
        with pytest.raises(QuestionNotFound):
            await use_case.execute(question_id=uuid4())
