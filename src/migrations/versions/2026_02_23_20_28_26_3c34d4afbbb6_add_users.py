"""add users

Revision ID: 3c34d4afbbb6
Revises: a9097bd731b9
Create Date: 2026-02-23 20:28:26.979007

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3c34d4afbbb6"
down_revision: Union[str, Sequence[str], None] = "a9097bd731b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
