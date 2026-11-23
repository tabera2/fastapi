"""Add owner-scoped creator deals.

Revision ID: af021bd2e7e1
Revises: e77dd0884a2f
"""
from alembic import op
import sqlalchemy as sa

revision = "af021bd2e7e1"
down_revision = "e77dd0884a2f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("brand", sa.String(200), nullable=False),
        sa.Column("creator", sa.String(200), nullable=False),
        sa.Column("deliverables", sa.String(2000), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("stage", sa.String(30), nullable=False, server_default="pitch"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_deals_owner_id", "deals", ["owner_id"])


def downgrade():
    op.drop_index("ix_deals_owner_id", table_name="deals")
    op.drop_table("deals")
