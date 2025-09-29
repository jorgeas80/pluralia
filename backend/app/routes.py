from fastapi import APIRouter
import feedparser

router = APIRouter()

FEEDS = {
    "El País": "https://elpais.com/rss/elpais/portada.xml",
    "ABC": "https://www.abc.es/rss/feeds/abcPortada.xml",
}

@router.get("/news")
def get_news(limit: int = 5):
    """
    Devuelve titulares recientes de varios medios.
    :param limit: número de noticias por medio (default=5)
    """
    all_news = []

    for source, url in FEEDS.items():
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:limit]:
            all_news.append({
                "title": entry.title,
                "link": entry.link,
                "published": getattr(entry, "published", None),
                "source": source,
            })

    return {"news": all_news}
