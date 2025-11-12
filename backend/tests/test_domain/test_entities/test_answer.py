from datetime import datetime
from uuid import UUID, uuid4

import pytest

from app.domain.entities.answer import AnswerEntity
from app.domain.excaptions import DomainValidationError


class TestAnswerEntity:
    def test_create_answer_entity_success(self):
        answer = AnswerEntity(
            id=uuid4(),
            question_id=uuid4(),
            user_id=uuid4(),
            text="This is a valid answer.",
        )

        assert answer.text == "This is a valid answer."
        assert isinstance(answer.created_at, datetime)
        assert isinstance(answer.id, UUID)
        assert isinstance(answer.question_id, UUID)
        assert isinstance(answer.user_id, UUID)

    def test_create_answer_entity_empty_text_raises_exception(self):
        with pytest.raises(DomainValidationError):
            AnswerEntity(
                id=uuid4(),
                question_id=uuid4(),
                user_id=uuid4(),
                text="   ",
            )
