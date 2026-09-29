import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"

BATCH_SIZE = 5


def rank_articles(articles: list[dict]) -> dict:
    """
    Ask the local LLM to rank a small batch of news articles.
    """

    article_text = []

    for index, article in enumerate(articles, start=1):
        article_text.append(
            f"""
ARTICLE {index}

Title:
{article.get("title", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published_datetime", "")}

Summary:
{article.get("summary", "")}
"""
        )

    prompt = f"""
You are the ranking component of a daily news selection agent.

Evaluate these news articles for a general daily news briefing.

Score each article from 1 to 10 based on:

1. Significance
2. Potential impact
3. Novelty
4. Recency
5. General relevance

Use factual reasoning.

Do not rank according to political preference or personal opinion.

Every article must receive a score.

Return ONLY valid JSON:

{{
    "rankings": [
        {{
            "article_number": 1,
            "score": 8,
            "reason": "Short factual reason"
        }}
    ]
}}

Articles:

{"".join(article_text)}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": "json",
        "think": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(result["message"]["content"])


def rank_all_articles(articles: list[dict]) -> list[dict]:
    """
    Rank all articles in small batches and combine the results.
    """

    all_rankings = []

    for start in range(0, len(articles), BATCH_SIZE):

        batch = articles[start:start + BATCH_SIZE]

        print(
            f"Ranking articles "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(articles)}..."
        )

        result = rank_articles(batch)

        for ranking in result["rankings"]:

            article_number = ranking["article_number"]

            article = batch[article_number - 1]

            ranked_article = article.copy()

            ranked_article["score"] = ranking["score"]
            ranked_article["reason"] = ranking["reason"]

            all_rankings.append(ranked_article)

    all_rankings.sort(
        key=lambda article: article["score"],
        reverse=True
    )

    return all_rankings