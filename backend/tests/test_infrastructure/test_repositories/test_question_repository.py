import uuid

import pytest

from app.domain.entities.question import QuestionEntity
from app.infrastructure.db.mappers.question_db_mapper import QuestionDbMapper
from app.infrastructure.db.repositories.question import QuestionRepositorySQLAlchemy


@pytest.mark.asyncio
async def test_add_and_get_by_id(session):
    repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    q_id = uuid.uuid4()
    entity = QuestionEntity(id=q_id, text="What is SQLAlchemy?")

    await repo.add(entity)
    await session.commit()

    got = await repo.get_by_id(q_id)
    assert got is not None
    assert got.id == entity.id
    assert got.text == entity.text


@pytest.mark.asyncio
async def test_get_by_id_not_found(session):
    repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    q_id = uuid.uuid4()

    got = await repo.get_by_id(q_id)
    assert got is None


@pytest.mark.asyncio
async def test_delete(session):
    repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    q_id = uuid.uuid4()
    entity = QuestionEntity(id=q_id, text="Test question")

    await repo.add(entity)
    await session.commit()

    await repo.delete(q_id)
    await session.commit()

    got = await repo.get_by_id(q_id)
    assert got is None


@pytest.mark.asyncio
async def test_get_list(session):
    repo = QuestionRepositorySQLAlchemy(session=session, mapper=QuestionDbMapper())
    q1 = QuestionEntity(id=uuid.uuid4(), text="Question 1")
    q2 = QuestionEntity(id=uuid.uuid4(), text="Question 2")

    await repo.add(q1)
    await repo.add(q2)
    await session.commit()

    result = await repo.get_list()
    assert len(result) == 2
