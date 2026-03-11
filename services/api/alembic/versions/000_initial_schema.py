"""initial schema

Revision ID: 000
Revises:
Create Date: 2024-11-21 01:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '000'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'source',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('bias', sa.String(), nullable=False),
    )
    op.create_table(
        'newsgroup',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('topic_hash', sa.String(), nullable=False),
        sa.Column('summary', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'article',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('group_id', sa.String(), sa.ForeignKey('newsgroup.id'), nullable=True),
        sa.Column('source_id', sa.String(), sa.ForeignKey('source.id'), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('link', sa.String(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('article')
    op.drop_table('newsgroup')
    op.drop_table('source')
