from app.news.rss_reader import fetch_news
from app.news.sources import NEWS_SOURCES
from app.news.deduplicator import deduplicate_articles
from app.news.normalizer import normalize_articles
from app.news.filter import filter_candidates

from app.agent.news_selector import rank_all_articles
from app.agent.final_selector import select_final_articles
from app.agent.summarizer import summarize_articles


# ============================================================
# 1. COLLECT NEWS
# ============================================================

all_articles = []

for source, url in NEWS_SOURCES.items():

    print(f"Fetching: {source}")

    articles = fetch_news(url, source)

    all_articles.extend(articles)


# ============================================================
# 2. REMOVE DUPLICATES
# ============================================================

unique_articles = deduplicate_articles(all_articles)


# ============================================================
# 3. NORMALIZE PUBLICATION DATES
# ============================================================

normalized_articles = normalize_articles(unique_articles)


# ============================================================
# 4. FILTER CANDIDATES
# ============================================================

candidate_articles = filter_candidates(normalized_articles)


print("\n" + "=" * 60)
print("NEWS PIPELINE")
print("=" * 60)

print(f"Collected: {len(all_articles)}")
print(f"Unique: {len(unique_articles)}")
print(f"Candidates: {len(candidate_articles)}")


# ============================================================
# 5. AI RANKING
# ============================================================

ranked_articles = rank_all_articles(candidate_articles)


# ============================================================
# 6. TOP 10 AI-RANKED ARTICLES
# ============================================================

top_articles = ranked_articles[:10]


print("\n" + "=" * 60)
print("TOP 10 AI-RANKED ARTICLES")
print("=" * 60)

for index, article in enumerate(top_articles, start=1):

    print(f"\n{index}. {article['title']}")
    print(f"Source: {article['source']}")
    print(f"Score: {article['score']}/10")
    print(f"Reason: {article['reason']}")


# ============================================================
# 7. FINAL AI SELECTION
# ============================================================

print("\n" + "=" * 60)
print("FINAL SELECTION AGENT")
print("=" * 60)

selection_result = select_final_articles(
    top_articles,
    count=5
)


# ============================================================
# 8. PREPARE FINAL 5 ARTICLES
# ============================================================

final_articles = []

for index, selected in enumerate(
    selection_result["selected_articles"],
    start=1
):

    candidate_number = selected["candidate_number"]

    article = top_articles[candidate_number - 1].copy()

    article["selection_reason"] = selected["reason"]

    final_articles.append(article)

    print(f"\n{index}. {article['title']}")
    print(f"Source: {article['source']}")
    print(f"Score: {article['score']}/10")
    print(f"Selection reason: {selected['reason']}")
    print(f"Link: {article['link']}")


# ============================================================
# 9. AI SUMMARIZATION
# ============================================================

print("\n" + "=" * 60)
print("AI SUMMARIZATION")
print("=" * 60)

summarized_articles = summarize_articles(final_articles)


# ============================================================
# 10. FINAL DAILY NEWS BRIEFING
# ============================================================

print("\n" + "=" * 60)
print("DAILY NEWS BRIEFING")
print("=" * 60)

for index, article in enumerate(
    summarized_articles,
    start=1
):

    print(f"\n{index}. {article['title']}")

    print("\nSummary:")
    print(article["summary_ai"])

    print("\nWhy it matters:")
    print(article["why_it_matters"])

    print(f"\nSource: {article['source']}")
    print(f"Link: {article['link']}")

    print("-" * 60)