from rss_reader import fetch_news
from sources import NEWS_SOURCES
from deduplicator import deduplicate_articles
from normalizer import normalize_articles
from filter import filter_candidates


# ============================================================
# 1. COLLECT NEWS
# ============================================================

all_articles = []

for source, url in NEWS_SOURCES.items():
    print(f"Fetching: {source}")

    articles = fetch_news(url, source)
    all_articles.extend(articles)


print("\n" + "=" * 60)
print("NEWS COLLECTION")
print("=" * 60)

print(f"Articles collected: {len(all_articles)}")


# ============================================================
# 2. REMOVE DUPLICATES
# ============================================================

unique_articles = deduplicate_articles(all_articles)

print("\n" + "=" * 60)
print("DEDUPLICATION")
print("=" * 60)

print(f"Unique articles: {len(unique_articles)}")
print(f"Duplicates removed: {len(all_articles) - len(unique_articles)}")


# ============================================================
# 3. NORMALIZE PUBLICATION DATES
# ============================================================

normalized_articles = normalize_articles(unique_articles)

print("\n" + "=" * 60)
print("DATE NORMALIZATION")
print("=" * 60)

print("Publication dates converted to UTC datetime objects.")


# ============================================================
# 4. FILTER CANDIDATE ARTICLES
# ============================================================

candidate_articles = filter_candidates(normalized_articles)

print("\n" + "=" * 60)
print("CANDIDATE FILTERING")
print("=" * 60)

print(f"Candidate articles: {len(candidate_articles)}")
print(f"Articles removed by filter: "
      f"{len(normalized_articles) - len(candidate_articles)}")


# ============================================================
# 5. DISPLAY CANDIDATE ARTICLES
# ============================================================

print("\n" + "=" * 60)
print("CANDIDATE ARTICLES")
print("=" * 60)

for index, article in enumerate(candidate_articles, start=1):

    print(f"\n{index}. [{article['source']}]")
    print(f"Title: {article['title']}")
    print(f"Published: {article['published_datetime']}")
    print(f"Link: {article['link']}")
    print("-" * 60)