from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from app.domain.excaptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class QuestionEntity:
    """Domain entity representing a question."""

    id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise DomainValidationError("Question text cannot be empty.")
