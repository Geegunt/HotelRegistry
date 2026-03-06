"""make email unique

Revision ID: 0b494bfc1998
Revises: 3c34d4afbbb6
Create Date: 2026-02-24 01:21:54.401097

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0b494bfc1998"
down_revision: Union[str, Sequence[str], None] = "3c34d4afbbb6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")