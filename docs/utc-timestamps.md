# UTC timestamps

Python domain entities and database models use timezone-aware datetimes.
Values with an offset are normalized to UTC; dates without timezone information
are rejected. Articles without a publication date retain `null`.

PostgreSQL stores `newsgroup.created_at` and `article.published_at` as
`timestamp with time zone` (`timestamptz`). This preserves the instant, not the
original publisher's timezone name or offset. API responses and newly generated
static JSON expose ISO 8601 dates with `+00:00`. The browser can display those
instants in the reader's local timezone.

## Existing data

Alembic revision `002_utc_timestamps` converts both existing columns using
`AT TIME ZONE 'UTC'`. This interpretation is based on the previous producers:
group creation used `datetime.utcnow()` and RSS publication dates used
feedparser's already-normalized UTC tuples. It does not depend on the database
session timezone, and preserves null publication dates.

The downgrade converts timestamps back to UTC wall-clock values without a
timezone, also independently of the session timezone.

## Rollout

1. Keep scheduled ingest disabled during deployment.
2. Deploy the updated API to Fly.io. Its existing release command runs
   `alembic upgrade head` before starting the new API.
3. Run the updated News Ingest workflow manually. It now runs the same migration
   command before ingestion, so it cannot write using the new models before the
   database migration succeeds. SQLModel and Alembic versions are pinned in both
   services. Avoid running migration/deployment jobs concurrently.
4. Verify the ingest, JSON generation and commit steps succeed, then check the
   Vercel deployment and `/data/news.json` for publication dates with UTC offsets.
   Existing checked-in JSON is refreshed by this ingestion, not by the migration.
5. Re-enable scheduled ingest when the manual run and publication are verified.

Changing column types takes a PostgreSQL table lock. Run the migration while
ingest is stopped. Never set `DROP_DB=true` for this rollout.

## Tests

Install the API, ingest and test requirements in a virtual environment, then run:

```bash
TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/pluralia_test \
  python -m pytest
```

Use a dedicated test database. PostgreSQL tests create and remove isolated
schemas and are skipped when `TEST_DATABASE_URL` is unset. They exercise the
migration and its reverse under `Europe/Madrid`, preserve winter/summer and DST
boundary instants, and check API/ingest storage plus JSON serialization. RSS
tests include positive/negative offsets, repeated DST hours and missing dates.
