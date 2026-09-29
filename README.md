# Daily News AI Agent

A local AI-powered daily news briefing agent that collects recent news from RSS feeds, filters and deduplicates articles, uses a local **Qwen3 4B** model through **Ollama** to rank and select important stories, and generates concise summaries.

The project is designed as an **Agentic AI portfolio project**, with deterministic Python components handling data processing and a local LLM handling subjective news-selection and summarization decisions.

## Current Pipeline

```text
RSS News Sources
       ↓
News Collection
       ↓
Deduplication
       ↓
Date Normalization
       ↓
Candidate Filtering
       ↓
Qwen3 4B — AI Ranking
       ↓
Top 10 Articles
       ↓
Qwen3 4B — Final Selection
       ↓
Final 5 Articles
       ↓
Qwen3 4B — Summarization
       ↓
Daily News Briefing
```

## Current Capabilities

- Collect news from multiple RSS feeds
- Remove duplicate articles
- Normalize publication dates to UTC
- Filter articles by recency and metadata quality
- Rank articles using a local LLM
- Select the final five articles using a second AI decision stage
- Generate concise summaries and "why it matters" explanations
- Run LLM inference locally through Ollama
- No paid LLM API required

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| LLM Runtime | Ollama |
| Local Model | Qwen3 4B |
| News Collection | RSS |
| RSS Parser | Feedparser |
| HTTP Communication | Requests |
| Environment Variables | python-dotenv |
| LLM Hardware | NVIDIA GPU |

## Project Structure

```text
daily-news-agent/
│
├── app/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── news_selector.py
│   │   ├── final_selector.py
│   │   ├── summarizer.py
│   │   ├── test_selector.py
│   │   └── test_full.py
│   │
│   ├── news/
│   │   ├── __init__.py
│   │   ├── rss_reader.py
│   │   ├── sources.py
│   │   ├── deduplicator.py
│   │   ├── normalizer.py
│   │   ├── filter.py
│   │   └── test_rss.py
│   │
│   └── ollama_test.py
│
├── config/
├── data/
├── docs/
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Ollama Setup

The project uses **Ollama** to run the LLM locally instead of using a paid cloud API.

### 1. Install Ollama

Download and install Ollama from:

https://ollama.com/

Verify the installation:

```powershell
ollama --version
```

### 2. Download Qwen3 4B

Pull the model:

```powershell
ollama pull qwen3:4b
```

Verify that it is installed:

```powershell
ollama list
```

You should see `qwen3:4b` in the installed models.

### 3. Test the model

Run:

```powershell
ollama run qwen3:4b
```

Try a simple prompt:

```text
Explain what an AI agent is in two sentences.
```

To exit the model:

```text
/bye
```

### 4. Ollama API

Ollama provides a local API at:

```text
http://localhost:11434
```

The project communicates with Qwen3 through:

```text
http://localhost:11434/api/chat
```

The Python application sends requests to the local Ollama server rather than to an external LLM provider.

## Python Environment Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the News Agent

From the project root:

```powershell
python -m app.agent.test_full
```

The application will:

1. Fetch articles from the configured RSS sources.
2. Remove duplicate articles.
3. Normalize publication dates.
4. Filter recent candidates.
5. Send candidate batches to Qwen3 for ranking.
6. Select the top 10 candidates.
7. Ask Qwen3 to select the final 5.
8. Generate summaries for the final five.
9. Display the resulting daily news briefing.

Example pipeline output:

```text
NEWS PIPELINE
============================================================
Collected: 107
Unique: 90
Candidates: 42

Ranking articles 1-5 of 42...
Ranking articles 6-10 of 42...
...

TOP 10 AI-RANKED ARTICLES
============================================================

1. ...
Score: 9/10

2. ...
Score: 9/10

...

FINAL 5 NEWS ARTICLES
============================================================

1. ...
2. ...
3. ...
4. ...
5. ...

AI SUMMARIZATION
============================================================

Summarizing article 1/5...
Summarizing article 2/5...
...

DAILY NEWS BRIEFING
============================================================
```

## News Sources

The current implementation uses BBC RSS feeds:

- BBC News
- BBC Technology
- BBC Business

Additional RSS sources can be configured in:

```text
app/news/sources.py
```

## Design Philosophy

The system separates **deterministic processing** from **AI decision-making**.

### Python handles

- RSS retrieval
- Deduplication
- Date parsing
- Recency filtering
- Data validation
- Batch processing
- LLM output validation

### Qwen3 handles

- News importance assessment
- Article ranking
- Final story selection
- News summarization
- Explaining why selected stories matter

This keeps predictable operations deterministic while using the LLM where contextual judgment is useful.

## Local LLM Architecture

```text
Python Application
       │
       │ HTTP
       ▼
Local Ollama Server
       │
       ▼
Qwen3 4B
       │
       ▼
Local GPU
```

The project does not require an OpenAI or Anthropic API key for its current LLM functionality.

## Current Status

### Completed

- [x] RSS news collection
- [x] Multiple news sources
- [x] Article deduplication
- [x] Date normalization
- [x] Candidate filtering
- [x] Local Ollama integration
- [x] AI article ranking
- [x] AI final selection
- [x] AI summarization

### Planned

- [ ] Fetch full article content for better summaries
- [ ] News verification stage
- [ ] HTML email generation
- [ ] Gmail SMTP delivery
- [ ] Daily automated execution
- [ ] Improved agent decision loop
- [ ] Logging and error handling
- [ ] Production-ready configuration

## Dependencies

The current Python dependencies are intentionally minimal:

```text
feedparser
requests
```

Ollama and the Qwen3 model are installed separately from Python.

## Security

Environment variables and secrets should never be committed to Git.

The project `.gitignore` excludes:

```text
.env
.env.*
```

When email functionality is added, credentials will be stored in environment variables rather than directly in source code.

## License

This project is intended as a personal learning and portfolio project.
