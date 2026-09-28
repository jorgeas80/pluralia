"""Require a publication timestamp for every stored article."""
from alembic import op
import sqlalchemy as sa


revision = "003_article_publication_date"
down_revision = "002_utc_timestamps"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Undated entries cannot participate in the live-news retention policy.
    op.execute("DELETE FROM article WHERE published_at IS NULL")
    op.alter_column(
        "article",
        "published_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=False,
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "article",
        "published_at",
        existing_type=sa.DateTime(timezone=True),
        nullable=True,
        existing_nullable=False,
    )
