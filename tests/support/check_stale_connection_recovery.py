"""Prove the API replaces a server-terminated pooled PostgreSQL connection."""
import os

import psycopg2
from sqlalchemy import text

from services.api.src.infrastructure.database.db import engine


with engine.connect() as connection:
    first_pid = connection.execute(text("SELECT pg_backend_pid()")).scalar_one()

with psycopg2.connect(os.environ["DATABASE_URL"]) as admin:
    with admin.cursor() as cursor:
        cursor.execute("SELECT pg_terminate_backend(%s)", (first_pid,))
        terminated = cursor.fetchone()[0]
    assert terminated

# pool_pre_ping must discard the dead connection on checkout and reconnect.
with engine.connect() as connection:
    second_pid = connection.execute(text("SELECT pg_backend_pid()")).scalar_one()
assert second_pid != first_pid, (first_pid, second_pid)
print(f"Replaced terminated PostgreSQL connection {first_pid} with {second_pid}")
engine.dispose()
