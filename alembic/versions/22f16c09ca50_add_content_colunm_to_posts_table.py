"""add content colunm to posts table

Revision ID: 22f16c09ca50
Revises: 302b92b32118
Create Date: 2022-08-19 14:47:54.093536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f16c09ca50'
down_revision = '302b92b32118'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
