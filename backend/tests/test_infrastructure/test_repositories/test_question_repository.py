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
