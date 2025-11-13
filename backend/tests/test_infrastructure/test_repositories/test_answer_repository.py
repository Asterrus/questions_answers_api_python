import uuid

import pytest

from app.domain.entities.answer import AnswerEntity
from app.domain.entities.question import QuestionEntity
from app.infrastructure.db.mappers.answer_db_mapper import AnswerDbMapper
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.repositories.answer import AnswerRepositorySQLAlchemy
from app.infrastructure.db.repositories.question import QuestionRepositorySQLAlchemy


@pytest.mark.asyncio
async def test_add_and_get_by_id(session):
    question_repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    answer_repo = AnswerRepositorySQLAlchemy(session=session, mapper=AnswerDbMapper())

    question_id = uuid.uuid4()
    question = QuestionEntity(id=question_id, text="Test question")
    await question_repo.add(question)

    answer_id = uuid.uuid4()
    user_id = uuid.uuid4()
    entity = AnswerEntity(
        id=answer_id, question_id=question_id, user_id=user_id, text="Test answer"
    )

    await answer_repo.add(entity)
    await session.commit()

    got = await answer_repo.get_by_id(answer_id)
    assert got is not None
    assert got.id == entity.id
    assert got.text == entity.text
    assert got.question_id == question_id
    assert got.user_id == user_id


@pytest.mark.asyncio
async def test_get_by_id_not_found(session):
    repo = AnswerRepositorySQLAlchemy(session=session, mapper=AnswerDbMapper())
    answer_id = uuid.uuid4()

    got = await repo.get_by_id(answer_id)
    assert got is None


@pytest.mark.asyncio
async def test_delete(session):
    question_repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    answer_repo = AnswerRepositorySQLAlchemy(session=session, mapper=AnswerDbMapper())

    question_id = uuid.uuid4()
    question = QuestionEntity(id=question_id, text="Test question")
    await question_repo.add(question)

    answer_id = uuid.uuid4()
    user_id = uuid.uuid4()
    entity = AnswerEntity(
        id=answer_id, question_id=question_id, user_id=user_id, text="Test answer"
    )

    await answer_repo.add(entity)
    await session.commit()

    await answer_repo.delete(answer_id)
    await session.commit()

    got = await answer_repo.get_by_id(answer_id)
    assert got is None


@pytest.mark.asyncio
async def test_get_by_question_id(session):
    question_repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    answer_repo = AnswerRepositorySQLAlchemy(session=session, mapper=AnswerDbMapper())

    question_id = uuid.uuid4()
    question = QuestionEntity(id=question_id, text="Test question")
    await question_repo.add(question)

    user_id = uuid.uuid4()
    a1 = AnswerEntity(id=uuid.uuid4(), question_id=question_id, user_id=user_id, text="Answer 1")
    a2 = AnswerEntity(id=uuid.uuid4(), question_id=question_id, user_id=user_id, text="Answer 2")

    await answer_repo.add(a1)
    await answer_repo.add(a2)
    await session.commit()

    result = await answer_repo.get_by_question_id(question_id)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_by_question_id_empty(session):
    repo = AnswerRepositorySQLAlchemy(session=session, mapper=AnswerDbMapper())
    question_id = uuid.uuid4()

    result = await repo.get_by_question_id(question_id)
    assert result == []
