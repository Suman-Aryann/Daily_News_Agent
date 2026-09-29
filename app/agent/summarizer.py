import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"


def summarize_article(article: dict) -> dict:
    """
    Generate a concise daily-news summary for one article.

    The model must only use information contained in the
    supplied article data.
    """

    prompt = f"""
You are a news briefing summarizer.

Summarize the following news article for a daily news briefing.

RULES:

1. Use ONLY the information provided below.
2. Do not invent facts, numbers, names, events, or explanations.
3. Do not add information from your own knowledge.
4. Keep the summary factual and neutral.
5. Write 2-3 concise sentences.
6. Explain why the story matters in one short sentence.
7. If the supplied information is insufficient to explain why it matters,
   simply state the main significance without speculation.

Return ONLY valid JSON:

{{
    "summary": "2-3 sentence factual summary.",
    "why_it_matters": "One concise sentence explaining its significance."
}}

ARTICLE:

Title:
{article.get("title", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published_datetime", "")}

Article Summary:
{article.get("summary", "")}
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


def summarize_articles(articles: list[dict]) -> list[dict]:
    """
    Summarize all selected articles.
    """

    summarized_articles = []

    for index, article in enumerate(articles, start=1):

        print(
            f"Summarizing article {index}/{len(articles)}..."
        )

        summary = summarize_article(article)

        summarized_article = article.copy()

        summarized_article["summary_ai"] = summary.get(
            "summary",
            ""
        )

        summarized_article["why_it_matters"] = summary.get(
            "why_it_matters",
            ""
        )

        summarized_articles.append(summarized_article)

    return summarized_articles