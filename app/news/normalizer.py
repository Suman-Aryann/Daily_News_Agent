from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def parse_published_date(date_string: str) -> datetime | None:
    """Convert an RSS publication date into a UTC datetime."""

    if not date_string:
        return None

    try:
        dt = parsedate_to_datetime(date_string)

        # If the RSS feed gives a datetime without timezone,
        # treat it as UTC.
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    except (TypeError, ValueError):
        return None


def normalize_articles(articles: list[dict]) -> list[dict]:
    """Normalize article metadata and add a UTC datetime."""

    normalized_articles = []

    for article in articles:
        normalized_article = article.copy()

        published_datetime = parse_published_date(
            article.get("published", "")
        )

        normalized_article["published_datetime"] = published_datetime

        normalized_articles.append(normalized_article)

    return normalized_articles