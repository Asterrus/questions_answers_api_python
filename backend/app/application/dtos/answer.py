from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AnswerResponseDTO:
    """DTO for retrieving answers."""

    id: UUID
    question_id: UUID
    user_id: UUID
    text: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
