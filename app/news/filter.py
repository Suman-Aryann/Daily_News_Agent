from datetime import datetime, timedelta, timezone


def filter_candidates(
    articles: list[dict],
    hours: int = 24,
) -> list[dict]:
    """
    Filter articles into a candidate pool for AI-based ranking.

    Criteria:
    - Article must have a title.
    - Article must have a URL.
    - Article must have a valid publication datetime.
    - Article must have been published within the specified time window.
    """

    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=hours)

    candidates = []

    for article in articles:
        title = article.get("title", "").strip()
        link = article.get("link", "").strip()
        published_datetime = article.get("published_datetime")

        # Require a usable title
        if not title:
            continue

        # Require a usable URL
        if not link:
            continue

        # Require a valid publication datetime
        if published_datetime is None:
            continue

        # Keep only recent articles
        if published_datetime < cutoff_time:
            continue

        candidates.append(article)

    return candidates