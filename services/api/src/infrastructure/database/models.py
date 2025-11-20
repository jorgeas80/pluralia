from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, ForeignKey
from typing import Optional
from datetime import datetime


class SourceModel(SQLModel, table=True):
    __tablename__ = "source"

    id: str = Field(sa_column=Column(String, primary_key=True))
    name: str
    url: Optional[str] = None
    bias: str


class NewsGroupModel(SQLModel, table=True):
    __tablename__ = "newsgroup"

    id: str = Field(sa_column=Column(String, primary_key=True))
    topic_hash: str
    summary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ArticleModel(SQLModel, table=True):
    __tablename__ = "article"

    id: str = Field(sa_column=Column(String, primary_key=True))
    group_id: Optional[str] = Field(default=None, sa_column=Column(String, ForeignKey("newsgroup.id")))
    source_id: Optional[str] = Field(default=None, sa_column=Column(String, ForeignKey("source.id")))
    title: str
    description: Optional[str] = None
    link: str
    published_at: Optional[datetime] = None

