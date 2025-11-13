from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class QuestionResponseDTO:
    """DTO for retrieving questions."""

    id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
