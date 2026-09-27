"""Store article and group timestamps as timezone-aware UTC instants.

Existing values are UTC without a timezone: groups used datetime.utcnow(),
and RSS dates came from feedparser's UTC published_parsed tuples.
"""
from alembic import op
import sqlalchemy as sa

revision = "002_utc_timestamps"
down_revision = "a222917a1dfd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for table, column, nullable in (
        ("newsgroup", "created_at", False),
        ("article", "published_at", True),
    ):
        op.alter_column(
            table, column,
            existing_type=sa.DateTime(timezone=False),
            type_=sa.DateTime(timezone=True),
            existing_nullable=nullable,
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )


def downgrade() -> None:
    for table, column, nullable in (
        ("article", "published_at", True),
        ("newsgroup", "created_at", False),
    ):
        op.alter_column(
            table, column,
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(timezone=False),
            existing_nullable=nullable,
            postgresql_using=f"{column} AT TIME ZONE 'UTC'",
        )
