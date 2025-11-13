from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.application.dtos.answer import AnswerResponseDTO


@dataclass(frozen=True, slots=True)
class QuestionsListResponseDTO:
    """DTO for retrieving questions."""

    id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class QuestionWithAnswersResponseDTO:
    """DTO for retrieving question with answers."""

    id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    answers: list[AnswerResponseDTO] = field(default_factory=list)
