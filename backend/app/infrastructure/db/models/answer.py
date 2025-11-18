from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.mapper import mapper_registry

if TYPE_CHECKING:
    from app.infrastructure.db.models.question import QuestionModel


@mapper_registry.mapped
class AnswerModel:
    __tablename__ = "answers"

    def __init__(
        self,
        *,
        id: UUID,
        question_id: UUID,
        user_id: UUID,
        text: str,
        created_at: datetime,
    ) -> None:
        self.id = id
        self.question_id = question_id
        self.user_id = user_id
        self.text = text
        self.created_at = created_at

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    question_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )
    question: Mapped[QuestionModel] = relationship(
        "QuestionModel",
        back_populates="answers",
    )

    def __repr__(self) -> str:
        return f"AnswerModel(id={self.id!r}, question_id={self.question_id!r}, user_id={self.user_id!r}, text={self.text!r}, created_at={self.created_at!r})"
