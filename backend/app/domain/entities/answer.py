from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.excaptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class AnswerEntity:
    """Domain entity representing an answer."""

    id: UUID
    question_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise DomainValidationError("Answer text cannot be empty.")
