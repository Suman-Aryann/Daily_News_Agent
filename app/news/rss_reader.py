import feedparser


def fetch_news(feed_url: str, source: str) -> list[dict]:
    """Fetch and normalize articles from an RSS feed."""

    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries:
        articles.append({
            "source": source,
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
        })

    return articles