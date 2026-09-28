# News data retention

Pluralia keeps live news for seven days in UTC. After a complete ingestion run,
GitHub Actions deletes older articles and groups that no longer have articles,
then generates the static JSON files. If ingestion fails, cleanup and publication
do not run.

RSS entries without a valid publication or update timestamp are skipped. The
database also requires `article.published_at`, so undated records cannot be
stored through another code path. The migration removes any existing undated
rows before enforcing that constraint.

The clusters JSON includes only groups with at least two articles in the live
window. Clusters are ordered by their newest article, with article count as a
tie breaker. Historical articles are not archived because the current product
does not use them.

The cleanup can be run manually with
`python -m services.ingest.src.cleanup_expired_news` after setting `DATABASE_URL`.
