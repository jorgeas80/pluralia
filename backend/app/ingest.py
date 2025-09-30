import hashlib
from datetime import datetime
import feedparser
from sqlmodel import Session, select

from .db import engine, init_db
from .models import Source, Article, NewsGroup

# Diccionario de fuentes con bias
FEEDS = {
    "El País": {
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "bias": "left"
    },
    "ABC": {
        "url": "https://www.abc.es/rss/feeds/abc_EspanaEspana.xml",
        "bias": "right"
    },
    "El Mundo": {
        "url": "https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml",
        "bias": "right"
    },
    "El Confidencial": {
        "url": "https://rss.elconfidencial.com/espana/",
        "bias": "center"
    },
    "El Diario": {
        "url": "https://www.eldiario.es/rss",
        "bias": "left"
    },
    "El Español": {
        "url": "https://www.elespanol.com/rss/espana/",
        "bias": "right"
    },
    "20 Minutos": {
        "url": "https://www.20minutos.es/rss/",
        "bias": "center"
    },
    "La Vanguardia": {
        "url": "https://www.lavanguardia.com/rss/home.xml",
        "bias": "center"
    },
    "The Objective": {
        "url": "https://www.theobjective.es/rss/espana/",
        "bias": "right"
    },
    "Público": {
        "url": "https://rss.app/feeds/H7MboPaDHQDwYKVw.xml",
        "bias": "left"
    },
    "El País": {
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/espana/portada",
        "bias": "left"
    },

}

def get_topic_hash(title: str) -> str:
    """Crea un hash a partir del título (para agrupar noticias similares)."""
    normalized = title.lower().strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]

def ingest():
    init_db()
    with Session(engine) as session:
        for name, meta in FEEDS.items():
            url = meta["url"]
            bias = meta["bias"]

            # Aseguramos que la fuente existe
            source = session.exec(select(Source).where(Source.name == name)).first()
            if not source:
                source = Source(name=name, url=url, bias=bias)
                session.add(source)
                session.commit()
                session.refresh(source)

            # Parsear feed
            parsed = feedparser.parse(url)
            for entry in parsed.entries[:10]:
                title = entry.title
                link = entry.link
                published = getattr(entry, "published", None)
                description = getattr(entry, "summary", None)

                # Convertir fecha si existe
                published_at = None
                if published:
                    try:
                        published_at = datetime(*entry.published_parsed[:6])
                    except Exception:
                        pass

                # Crear o buscar grupo
                topic_hash = get_topic_hash(title)
                group = session.exec(select(NewsGroup).where(NewsGroup.topic_hash == topic_hash)).first()
                if not group:
                    group = NewsGroup(topic_hash=topic_hash)
                    session.add(group)
                    session.commit()
                    session.refresh(group)

                # Evitar duplicados (por link)
                exists = session.exec(select(Article).where(Article.link == link)).first()
                if exists:
                    continue

                # Guardar artículo
                article = Article(
                    group_id=group.id,
                    source_id=source.id,
                    title=title,
                    description=description,
                    link=link,
                    published_at=published_at
                )
                session.add(article)

            session.commit()

if __name__ == "__main__":
    ingest()
    print("✅ Ingesta completada")
