import asyncio
from libs.domain.value_objects.bias import Bias
from services.ingest.src.application.ingest_news import IngestNews
from services.ingest.src.infrastructure.database.db import init_db, get_session
from services.ingest.src.infrastructure.repositories.sqlmodel_article_repository import SqlModelArticleRepository
from services.ingest.src.infrastructure.repositories.sqlmodel_news_group_repository import SqlModelNewsGroupRepository
from services.ingest.src.infrastructure.repositories.sqlmodel_source_repository import SqlModelSourceRepository
from services.ingest.src.infrastructure.services.rss_parser import RSSParser

FEEDS = {
    "El País": {
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "bias": Bias.left(),
    },
    "ABC": {
        "url": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
        "bias": Bias.right(),
    },
    "El Mundo": {
        "url": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
        "bias": Bias.right(),
    },
    "El Confidencial": {
        "url": "https://rss.elconfidencial.com/espana/",
        "bias": Bias.center(),
    },
    "El Diario": {
        "url": "https://www.eldiario.es/rss",
        "bias": Bias.left(),
    },
    "El Español": {
        "url": "https://www.elespanol.com/rss/espana/",
        "bias": Bias.right(),
    },
    "20 Minutos": {
        "url": "https://www.20minutos.es/rss/",
        "bias": Bias.center(),
    },
    "La Vanguardia": {
        "url": "https://www.lavanguardia.com/rss/home.xml",
        "bias": Bias.center(),
    },
    "The Objective": {
        "url": "https://www.theobjective.es/rss/espana/",
        "bias": Bias.right(),
    },
    "Público": {
        "url": "https://rss.app/feeds/H7MboPaDHQDwYKVw.xml",
        "bias": Bias.left(),
    },
}


async def main():
    """Main entry point for the ingest service."""
    init_db()

    with get_session() as session:
        source_repository = SqlModelSourceRepository(session)
        article_repository = SqlModelArticleRepository(session)
        news_group_repository = SqlModelNewsGroupRepository(session)
        rss_parser = RSSParser()

        ingest_news = IngestNews(
            source_repository=source_repository,
            article_repository=article_repository,
            news_group_repository=news_group_repository,
            rss_parser=rss_parser,
        )

        for name, config in FEEDS.items():
            print(f"Ingesting news from {name}...")
            await ingest_news.execute(
                source_name=name,
                source_url=config["url"],
                bias=config["bias"],
                limit=10,
            )
            print(f"✅ Completed {name}")

    print("✅ Ingest completed")


if __name__ == "__main__":
    asyncio.run(main())

