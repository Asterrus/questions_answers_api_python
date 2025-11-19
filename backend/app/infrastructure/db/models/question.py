from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.mapper import mapper_registry

if TYPE_CHECKING:
    from app.infrastructure.db.models.answer import AnswerModel


@mapper_registry.mapped
class QuestionModel:
    __tablename__ = "questions"

    def __init__(
        self,
        *,
        id: UUID,
        text: str,
        created_at: datetime,
        answers: list[AnswerModel],
    ) -> None:
        self.id = id
        self.text = text
        self.created_at = created_at
        self.answers = answers

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )

    answers: Mapped[list[AnswerModel]] = relationship(
        "AnswerModel",
        back_populates="question",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"QuestionModel(id={self.id!r}, text={self.text!r}, created_at={self.created_at!r}, answers={self.answers!r})"
