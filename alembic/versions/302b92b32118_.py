"""empty message

Revision ID: 302b92b32118
Revises: 
Create Date: 2022-08-19 14:40:40.642687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '302b92b32118'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
