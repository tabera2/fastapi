"""add user table

Revision ID: 3ce6a2b38b53
Revises: 426599ca1ba8
Create Date: 2026-11-22 08:10:30.751516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ce6a2b38b53'
down_revision: Union[str, Sequence[str], None] = '426599ca1ba8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
