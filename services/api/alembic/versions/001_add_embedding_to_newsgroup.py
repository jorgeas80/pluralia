"""add embedding to newsgroup

Revision ID: 001
Revises: 
Create Date: 2024-11-21 02:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add embedding column to newsgroup table
    op.add_column('newsgroup', sa.Column('embedding', postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    # Remove embedding column from newsgroup table
    op.drop_column('newsgroup', 'embedding')


