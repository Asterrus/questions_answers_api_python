from uuid import UUID, uuid4

import pytest

from app.application.dtos.question import (
    AnswerResponseDTO,
    QuestionWithAnswersResponseDTO,
)
from app.application.use_cases.get_question_with_answers import GetQuestionWithAnswersUseCase
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeQuestionByIdReader:
    def __init__(self, question: QuestionEntity | None = None):
        self.question = question

    async def get_by_id(self, id: UUID) -> QuestionEntity | None:
        return self.question


class FakeAnswersByQuestionIdReader:
    def __init__(self, answers: list[AnswerEntity]):
        self.answers = answers

    async def get_by_question_id(self, question_id: UUID) -> list[AnswerEntity]:
        return self.answers


class FakeQuestionWithAnswersEntityToDtoMapper:
    def to_dto(
        self, question: QuestionEntity, answers: list[AnswerEntity]
    ) -> QuestionWithAnswersResponseDTO:
        question_answers = [
            AnswerResponseDTO(
                id=answer.id,
                question_id=answer.question_id,
                user_id=answer.user_id,
                text=answer.text,
            )
            for answer in answers
        ]
        return QuestionWithAnswersResponseDTO(
            id=question.id,
            text=question.text,
            answers=question_answers,
        )


class TestGetQuestionWithAnswersUseCase:
    @pytest.mark.asyncio
    async def test_get_question_with_answers_success(self, fake_uow: FakeUnitOfWork):
        question = QuestionEntity(
            id=uuid4(),
            text="What is your favorite color?",
        )
        answers = [
            AnswerEntity(id=uuid4(), question_id=question.id, user_id=uuid4(), text="Blue"),
            AnswerEntity(id=uuid4(), question_id=question.id, user_id=uuid4(), text="Green"),
        ]
        question_repo = FakeQuestionByIdReader(question=question)
        answer_repo = FakeAnswersByQuestionIdReader(answers=answers)
        mapper = FakeQuestionWithAnswersEntityToDtoMapper()

        use_case = GetQuestionWithAnswersUseCase(
            question_repository=question_repo,
            answer_repository=answer_repo,
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
        question_repo = FakeQuestionByIdReader()
        answer_repo = FakeAnswersByQuestionIdReader(answers=[])
        mapper = FakeQuestionWithAnswersEntityToDtoMapper()

        use_case = GetQuestionWithAnswersUseCase(
            question_repository=question_repo,
            answer_repository=answer_repo,
            question_mapper=mapper,
            uow=fake_uow,
        )

        result = await use_case.execute(question_id=uuid4())
        assert result is None
