"""First migration

Revision ID: bd8c9bb7bbe8
Revises:
Create Date: 2020-05-24 20:13:58.353316

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bd8c9bb7bbe8"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("description", sa.String()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("item")
