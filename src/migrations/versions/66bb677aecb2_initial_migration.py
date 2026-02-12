"""initial migration

Revision ID: 66bb677aecb2
Revises: 
Create Date: 2026-02-13 00:56:49.211046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



revision: str = '66bb677aecb2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('hotels')
