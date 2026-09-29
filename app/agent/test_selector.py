from news_selector import rank_articles


test_articles = [
    {
        "source": "BBC",
        "title": "Major technology development announced",
        "published_datetime": "2026-09-29 12:00:00+00:00",
        "summary": (
            "A major technology company announced a significant "
            "new development that could affect the technology industry."
        ),
    },
    {
        "source": "BBC",
        "title": "Local community event opens this weekend",
        "published_datetime": "2026-09-29 11:00:00+00:00",
        "summary": (
            "A local community event featuring several activities "
            "will take place this weekend."
        ),
    },
    {
        "source": "BBC",
        "title": "Major international economic announcement",
        "published_datetime": "2026-09-29 10:00:00+00:00",
        "summary": (
            "Government officials announced a major economic policy "
            "change that could affect businesses and consumers."
        ),
    },
]


result = rank_articles(test_articles)

print("\nLLM ranking result:\n")

print(result)