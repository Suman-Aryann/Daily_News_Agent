import json
import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"


def select_final_articles(
    articles: list[dict],
    count: int = 5
) -> dict:
    """
    Use the local LLM to select the final news articles.

    Python validates the LLM output and ensures that exactly
    `count` unique articles are returned.
    """

    article_text = []

    for index, article in enumerate(articles, start=1):
        article_text.append(
            f"""
CANDIDATE {index}

Title:
{article.get("title", "")}

Source:
{article.get("source", "")}

Published:
{article.get("published_datetime", "")}

AI Score:
{article.get("score", "")}/10

AI Ranking Reason:
{article.get("reason", "")}

Summary:
{article.get("summary", "")}
"""
        )

    prompt = f"""
You are the final decision-making component of a daily news briefing agent.

You have {len(articles)} candidate articles.

Select EXACTLY {count} DIFFERENT candidates for the final daily
news briefing.

The final briefing should contain the most useful and important
stories for a general audience.

Consider:

- Overall significance
- Real-world impact
- Recency
- General public relevance
- Topic diversity
- Avoiding redundant stories
- Overall usefulness of the complete briefing

Do not select based on political preference.

Do not select an article merely because it is emotionally shocking.

IMPORTANT:
You MUST return exactly {count} candidates.
You MUST return different candidate numbers.
Do not return fewer than {count}.
Do not return more than {count}.

Return ONLY this JSON structure:

{{
    "selected_articles": [
        {{
            "candidate_number": 1,
            "reason": "Short factual reason"
        }},
        {{
            "candidate_number": 2,
            "reason": "Short factual reason"
        }},
        {{
            "candidate_number": 3,
            "reason": "Short factual reason"
        }},
        {{
            "candidate_number": 4,
            "reason": "Short factual reason"
        }},
        {{
            "candidate_number": 5,
            "reason": "Short factual reason"
        }}
    ]
}}

Candidates:

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

    raw_result = json.loads(result["message"]["content"])

    selected = raw_result.get("selected_articles", [])

    # ========================================================
    # VALIDATE LLM OUTPUT
    # ========================================================

    valid_selections = []
    used_candidates = set()

    for item in selected:

        candidate_number = item.get("candidate_number")

        if not isinstance(candidate_number, int):
            continue

        if not 1 <= candidate_number <= len(articles):
            continue

        if candidate_number in used_candidates:
            continue

        valid_selections.append(item)
        used_candidates.add(candidate_number)

    # ========================================================
    # FALLBACK
    # ========================================================
    # If the LLM returned fewer than the requested number,
    # fill the remaining slots using the highest-ranked
    # articles that were not already selected.
    # ========================================================

    if len(valid_selections) < count:

        for index in range(len(articles)):

            candidate_number = index + 1

            if candidate_number in used_candidates:
                continue

            valid_selections.append(
                {
                    "candidate_number": candidate_number,
                    "reason": (
                        "Added by deterministic fallback because "
                        "the AI returned fewer selections than required."
                    )
                }
            )

            used_candidates.add(candidate_number)

            if len(valid_selections) == count:
                break

    # Safety check
    valid_selections = valid_selections[:count]

    return {
        "selected_articles": valid_selections
    }