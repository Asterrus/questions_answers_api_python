from datetime import datetime
from uuid import UUID, uuid4

import pytest

from app.domain.entities.question import QuestionEntity
from app.domain.excaptions import DomainValidationError


class TestQuestionEntity:
    def test_create_question_entity_success(self):
        answer = QuestionEntity(
            id=uuid4(),
            text="This is a valid question.",
        )

        assert answer.text == "This is a valid question."
        assert isinstance(answer.created_at, datetime)
        assert isinstance(answer.id, UUID)

    def test_create_question_entity_empty_text_raises_exception(self):
        with pytest.raises(DomainValidationError):
            QuestionEntity(
                id=uuid4(),
                text="   ",
            )
