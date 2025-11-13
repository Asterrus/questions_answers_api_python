"""seed_questions_and_answers

Revision ID: a6f1a70819d1
Revises: 87f721a7ab61
Create Date: 2025-11-14 02:44:10.850692

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a6f1a70819d1"
down_revision: Union[str, Sequence[str], None] = "87f721a7ab61"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Seed questions and answers."""
    questions_table = sa.table(
        "questions",
        sa.column("id", sa.UUID),
        sa.column("text", sa.Text),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )

    answers_table = sa.table(
        "answers",
        sa.column("id", sa.UUID),
        sa.column("question_id", sa.UUID),
        sa.column("user_id", sa.UUID),
        sa.column("text", sa.Text),
        sa.column("created_at", sa.DateTime(timezone=True)),
    )

    # Questions
    q1_id = "11111111-1111-1111-1111-111111111111"

    op.bulk_insert(
        questions_table,
        [
            {
                "id": q1_id,
                "text": "Вопрос?",
            },
        ],
    )

    # Answers
    user1_id = "11111111-1111-1111-1111-111111111111"

    op.bulk_insert(
        answers_table,
        [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "question_id": q1_id,
                "user_id": user1_id,
                "text": "Ответ!",
            }
        ],
    )


def downgrade() -> None:
    """Remove seed data."""
    op.execute("DELETE FROM answers WHERE id = '11111111-1111-1111-1111-111111111111'")
    op.execute("DELETE FROM questions WHERE id = '11111111-1111-1111-1111-111111111111'")
