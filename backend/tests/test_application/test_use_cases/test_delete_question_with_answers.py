from uuid import UUID, uuid4

import pytest

from app.application.dtos.question import AnswerResponseDTO, QuestionWithAnswersResponseDTO
from app.application.use_cases.delete_question_with_answers import DeleteQuestionWithAnswersUseCase
from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from tests.fakes.fake_uow import FakeUnitOfWork


class FakeQuestionWithAnswersDeleter:
    def __init__(self, answers: list[AnswerEntity], question: QuestionEntity | None = None):
        self.question = question
        self.answers = answers

    async def delete(self, id: UUID) -> tuple[QuestionEntity | None, list[AnswerEntity]]:
        return self.question, self.answers


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


class TestDeleteQuestionWithAnswersUseCase:
    @pytest.mark.asyncio
    async def test_delete_question_with_answers_success(self, fake_uow: FakeUnitOfWork):
        question = QuestionEntity(
            id=uuid4(),
            text="What is your favorite color?",
        )
        answers = [
            AnswerEntity(id=uuid4(), question_id=question.id, user_id=uuid4(), text="Blue"),
            AnswerEntity(id=uuid4(), question_id=question.id, user_id=uuid4(), text="Green"),
        ]

        question_repo = FakeQuestionWithAnswersDeleter(
            question=question,
            answers=answers,
        )
        mapper = FakeQuestionWithAnswersEntityToDtoMapper()

        use_case = DeleteQuestionWithAnswersUseCase(
            question_repository=question_repo,
            question_mapper=mapper,
            uow=fake_uow,
        )

        result = await use_case.execute(question.id)

        assert result is not None
        assert result.id == question.id
        assert result.text == question.text
        assert len(result.answers) == 2
