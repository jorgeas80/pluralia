from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: Optional[str] = None
    bias: str
    conglomerate: Optional[str] = None

    articles: List["Article"] = Relationship(back_populates="source")

class NewsGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_hash: str
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    articles: List["Article"] = Relationship(back_populates="group")

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: Optional[int] = Field(default=None, foreign_key="newsgroup.id")
    source_id: Optional[int] = Field(default=None, foreign_key="source.id")
    title: str
    description: Optional[str] = None
    link: str
    published_at: Optional[datetime] = None

    group: Optional[NewsGroup] = Relationship(back_populates="articles")
    source: Optional[Source] = Relationship(back_populates="articles")
