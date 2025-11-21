"""Tests for Article entity."""
import pytest
from uuid import UUID
from libs.domain.entities.article import Article
from libs.domain.errors.domain_error import InvalidDomainError
from tests.factories.article_factory import ArticleFactory
from tests.factories.source_factory import SourceFactory


def test_new_creates_article_with_uuid(fake):
    title = fake.sentence()
    link = fake.url()
    source = SourceFactory.build()

    article = Article.new(title=title, link=link, source_id=source.id)

    assert isinstance(article.id, UUID)
    assert article.title == title
    assert article.link == link
    assert article.source_id == source.id
    assert article.group_id is None


def test_new_generates_uuid_if_not_provided(fake):
    source = SourceFactory.build()
    article1 = Article.new(title=fake.sentence(), link=fake.url(), source_id=source.id)
    article2 = Article.new(title=fake.sentence(), link=fake.url(), source_id=source.id)

    assert article1.id != article2.id


def test_assign_to_group_returns_new_instance_with_group_id(fake):
    article = ArticleFactory.build(group_id=None)
    new_group_id = fake.uuid4(cast_to=None)

    updated_article = article.assign_to_group(new_group_id)

    assert updated_article.group_id == new_group_id
    assert updated_article.id == article.id
    assert updated_article.title == article.title
    assert article.group_id is None


@pytest.mark.parametrize("invalid_id", ["not-a-uuid", 123, None])
def test_invalid_id_raises_error(invalid_id, fake):
    source = SourceFactory.build()
    with pytest.raises(InvalidDomainError, match="Article id must be a UUID"):
        Article.build(
            id=invalid_id,
            title=fake.sentence(),
            link=fake.url(),
            source_id=source.id,
            description=None,
            published_at=None,
            group_id=None,
        )


@pytest.mark.parametrize("invalid_title", ["", " " * 501, None])
def test_invalid_title_raises_error(invalid_title, fake):
    source = SourceFactory.build()
    with pytest.raises(InvalidDomainError, match="Article title must be between 1 and 500 characters"):
        Article.new(title=invalid_title, link=fake.url(), source_id=source.id)


@pytest.mark.parametrize("invalid_link", ["", "not-a-url", "ftp://example.com", " " * 1001])
def test_invalid_link_raises_error(invalid_link, fake):
    source = SourceFactory.build()
    with pytest.raises(InvalidDomainError):
        Article.new(title=fake.sentence(), link=invalid_link, source_id=source.id)


def test_article_is_immutable(fake):
    from dataclasses import FrozenInstanceError
    article = ArticleFactory.build()
    with pytest.raises(FrozenInstanceError):
        article.title = "New Title"

