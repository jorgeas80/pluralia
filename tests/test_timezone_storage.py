"""PostgreSQL checks; each test uses its own disposable schema.

Set TEST_DATABASE_URL to a dedicated PostgreSQL test database.
The API and ingest have separate SQLModel registries in production, so their
round trips run in separate processes as well.
"""
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

import psycopg2
from psycopg2 import sql
import pytest

ROOT = Path(__file__).resolve().parents[1]
OLD_REVISION = "a222917a1dfd"


def run(env, *args, cwd=ROOT):
    result = subprocess.run(
        [sys.executable, *args], env=env, cwd=cwd,
        capture_output=True, text=True, timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def migrate(env, direction, revision):
    run(env, "-m", "alembic", direction, revision, cwd=ROOT / "services/api")


@pytest.fixture
def isolated_database():
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL for PostgreSQL migration tests")
    schema = "timezone_test_" + uuid4().hex
    admin = psycopg2.connect(url)
    admin.autocommit = True
    with admin.cursor() as cursor:
        cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    options = f"-csearch_path={schema} -ctimezone=Europe/Madrid"
    env = {
        **os.environ, "DATABASE_URL": url, "PGOPTIONS": options,
        "PYTHONPATH": str(ROOT), "DROP_DB": "false",
    }
    connection = psycopg2.connect(url, options=options)
    connection.autocommit = True
    try:
        yield env, connection
    finally:
        connection.close()
        with admin.cursor() as cursor:
            cursor.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))
        admin.close()


def test_migration_preserves_utc_instants_and_rejects_undated_articles(isolated_database):
    env, connection = isolated_database
    migrate(env, "upgrade", OLD_REVISION)
    dates = [datetime(2026, 1, 15, 8), datetime(2026, 7, 15, 8),
             datetime(2026, 10, 25, 1, 30)]
    with connection.cursor() as cursor:
        for i, date in enumerate(dates):
            cursor.execute(
                "INSERT INTO newsgroup(id, topic_hash, created_at) VALUES (%s, %s, %s)",
                (str(i), str(i), date),
            )
            cursor.execute(
                "INSERT INTO article(id, title, link, published_at) VALUES (%s, %s, %s, %s)",
                (str(i), "Legacy", "https://example.com", date),
            )
        cursor.execute("INSERT INTO article(id, title, link) VALUES ('undated', 'Unknown', 'https://example.com')")

    migrate(env, "upgrade", "head")
    # Repeat just like a later deployment: migrations must be idempotent.
    migrate(env, "upgrade", "head")
    with connection.cursor() as cursor:
        cursor.execute("SELECT created_at FROM newsgroup ORDER BY id")
        assert [row[0] for row in cursor] == [d.replace(tzinfo=timezone.utc) for d in dates]
        cursor.execute("SELECT published_at FROM article ORDER BY id")
        assert [row[0] for row in cursor] == [d.replace(tzinfo=timezone.utc) for d in dates]
        cursor.execute("SELECT is_nullable FROM information_schema.columns WHERE table_schema = current_schema() AND table_name = 'article' AND column_name = 'published_at'")
        assert cursor.fetchone()[0] == "NO"
        cursor.execute("""SELECT data_type FROM information_schema.columns
            WHERE table_schema = current_schema()
            AND column_name IN ('created_at', 'published_at')""")
        assert [row[0] for row in cursor] == ["timestamp with time zone"] * 2

    migrate(env, "downgrade", OLD_REVISION)
    with connection.cursor() as cursor:
        cursor.execute("SELECT created_at FROM newsgroup ORDER BY id")
        assert [row[0] for row in cursor] == dates
        cursor.execute("SELECT published_at FROM article ORDER BY id")
        assert [row[0] for row in cursor] == dates


@pytest.mark.parametrize("service", ["api", "ingest"])
def test_service_roundtrip_and_json_keep_utc(isolated_database, service):
    env, _ = isolated_database
    migrate(env, "upgrade", "head")
    run(env, "tests/support/check_timezone_roundtrip.py", service)


def test_api_replaces_a_stale_pooled_connection(isolated_database):
    env, _ = isolated_database
    migrate(env, "upgrade", "head")
    run(env, "tests/support/check_stale_connection_recovery.py")
