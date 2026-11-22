"""add content Column to posts table

Revision ID: 426599ca1ba8
Revises: b5535bf1b9cb
Create Date: 2026-11-22 08:05:01.890428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '426599ca1ba8'
down_revision: Union[str, Sequence[str], None] = 'b5535bf1b9cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
