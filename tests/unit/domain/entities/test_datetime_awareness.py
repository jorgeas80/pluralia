from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from libs.domain.entities.article import Article
from libs.domain.entities.news_group import NewsGroup
from libs.domain.errors.domain_error import InvalidDomainError
from libs.domain.value_objects.topic_hash import TopicHash


def test_new_groups_have_utc_creation_time():
    before = datetime.now(timezone.utc)
    group = NewsGroup.new(TopicHash.from_title("A new story"))
    assert group.created_at.utcoffset() == timedelta(0)
    assert before <= group.created_at <= datetime.now(timezone.utc)


@pytest.mark.parametrize("entity", ["article", "group"])
def test_domain_rejects_dates_without_timezone(entity):
    with pytest.raises(InvalidDomainError, match="timezone"):
        if entity == "article":
            Article.new("Story", "https://example.com/story", uuid4(),
                        published_at=datetime(2026, 9, 27, 10))
        else:
            NewsGroup(uuid4(), TopicHash.from_title("Story"),
                      created_at=datetime(2026, 9, 27, 10))


@pytest.mark.parametrize("entity", ["article", "group"])
def test_domain_normalizes_offset_to_utc_without_changing_instant(entity):
    date = datetime(2026, 9, 27, 10, tzinfo=timezone(timedelta(hours=2)))
    if entity == "article":
        value = Article.new("Story", "https://example.com/story", uuid4(),
                            published_at=date).published_at
    else:
        value = NewsGroup(uuid4(), TopicHash.from_title("Story"), created_at=date).created_at
    assert value.isoformat() == "2026-09-27T08:00:00+00:00"
