import uuid

import pytest
import pytest_asyncio

from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from app.infrastructure.db.mappers.question_db_mapper import (
    QuestionDbMapper,
    QuestionWithAnswersDbMapper,
)
from app.infrastructure.db.repositories.question import SQLAlchemyQuestionRepository


@pytest_asyncio.fixture
async def question_repository(session):
    return SQLAlchemyQuestionRepository(
        session=session,
        mapper=QuestionDbMapper(),
        mapper_with_answers=QuestionWithAnswersDbMapper(),
    )


@pytest.mark.asyncio
async def test_add_and_get_by_id(session, question_repository):
    q_id = uuid.uuid4()
    entity = QuestionEntity(id=q_id, text="What is SQLAlchemy?")

    await question_repository.add(entity)
    await session.commit()

    got = await question_repository.get_by_id(q_id)
    assert got is not None
    assert got.id == entity.id
    assert got.text == entity.text


@pytest.mark.asyncio
async def test_get_by_id_not_found(question_repository):
    q_id = uuid.uuid4()

    got = await question_repository.get_by_id(q_id)
    assert got is None


@pytest.mark.asyncio
async def test_delete(session, question_repository):
    q_id = uuid.uuid4()
    entity = QuestionEntity(id=q_id, text="Test question")

    await question_repository.add(entity)
    await session.commit()

    await question_repository.delete(q_id)
    await session.commit()

    got = await question_repository.get_by_id(q_id)
    assert got is None


@pytest.mark.asyncio
async def test_get_list(session, question_repository):
    q1 = QuestionEntity(id=uuid.uuid4(), text="Question 1")
    q2 = QuestionEntity(id=uuid.uuid4(), text="Question 2")

    await question_repository.add(q1)
    await question_repository.add(q2)
    await session.commit()

    result = await question_repository.get_list()
    assert len(result) == 2
    ids = {q.id for q in result}
    assert q1.id in ids
    assert q2.id in ids


@pytest.mark.asyncio
async def test_get_by_id_with_answers(session, question_repository):
    q_id = uuid.uuid4()
    answers = [
        AnswerEntity(id=uuid.uuid4(), question_id=q_id, user_id=uuid.uuid4(), text="Blue"),
        AnswerEntity(id=uuid.uuid4(), question_id=q_id, user_id=uuid.uuid4(), text="Green"),
    ]
    entity = QuestionEntity(id=q_id, text="Test question", answers=answers)

    await question_repository.add(entity)
    await session.commit()

    got = await question_repository.get_by_id_with_answers(q_id)
    assert got is not None
    assert got.id == entity.id
    assert got.text == entity.text
    assert len(got.answers) == 2
