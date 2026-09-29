import re


def normalize_title(title: str) -> str:
    """Normalize a title for duplicate detection."""

    title = title.lower()
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()

    return title


def deduplicate_articles(articles: list[dict]) -> list[dict]:
    """Remove duplicate articles based on URL and normalized title."""

    seen_urls = set()
    seen_titles = set()

    unique_articles = []

    for article in articles:
        url = article.get("link", "").strip()
        title = article.get("title", "").strip()

        normalized_title = normalize_title(title)

        # Skip duplicate URL
        if url and url in seen_urls:
            continue

        # Skip duplicate title
        if normalized_title and normalized_title in seen_titles:
            continue

        if url:
            seen_urls.add(url)

        if normalized_title:
            seen_titles.add(normalized_title)

        unique_articles.append(article)

    return unique_articles