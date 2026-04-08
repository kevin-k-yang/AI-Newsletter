"""
Digest generation pipeline with vector embedding personalization.

1. Fetch news from NewsAPI (10 per category)
2. Generate embeddings for all articles (Gemini gemini-embedding-001)
3. Score & rank by cosine similarity to user preference vector
4. Pick top 3 per section
5. Summarize with Gemini Flash
6. Store articles in DB
"""

import hashlib
import json
import os
from datetime import date

import requests
from google import genai

from models import DailyDigest, SectionSummary, Substory
from database import (
    save_article, mark_selected, get_preference_vector,
    cosine_similarity,
)

SECTIONS = ["sports", "tech", "finance", "world"]


def _news_api_key() -> str:
    return os.environ.get("NEWS_API_KEY", "")


def _gemini_api_key() -> str:
    return os.environ.get("GEMINI_API_KEY", "")


def _genai_client() -> genai.Client:
    return genai.Client(api_key=_gemini_api_key())


def _article_id(url: str, title: str) -> str:
    """Generate a stable ID from URL (or title as fallback)."""
    key = url if url else title
    return hashlib.md5(key.encode()).hexdigest()[:12]


# --- Step 1: Fetch ---

def fetch_articles() -> dict[str, list[dict]]:
    """Fetch top headlines from NewsAPI by category."""
    if not _news_api_key():
        print("WARNING: NEWS_API_KEY not set, returning empty results")
        return {s: [] for s in SECTIONS}

    categorized: dict[str, list[dict]] = {s: [] for s in SECTIONS}
    seen_ids: set[str] = set()  # Deduplicate across sections

    for news_category, our_section in [
        ("sports", "sports"),
        ("technology", "tech"),
        ("business", "finance"),
        ("general", "world"),
    ]:
        resp = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "category": news_category,
                "country": "us",
                "pageSize": 10,
                "apiKey": _news_api_key(),
            },
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"NewsAPI error for {news_category}: {resp.status_code}")
            continue

        for i, article in enumerate(resp.json().get("articles", [])):
            if article.get("title") and article["title"] != "[Removed]":
                url = article.get("url", "")
                aid = _article_id(url, article["title"])

                # Skip duplicates across sections
                if aid in seen_ids:
                    continue
                seen_ids.add(aid)

                # Clean truncated descriptions from NewsAPI
                desc = article.get("description") or ""
                content = article.get("content") or desc
                # NewsAPI truncates with "... [+N chars]" — strip that
                for field_val in [desc, content]:
                    if field_val.endswith("…") or "… [+" in field_val:
                        pass  # handled below
                desc = desc.split("… [+")[0].rstrip("…").rstrip()
                content = content.split("… [+")[0].rstrip("…").rstrip()

                art = {
                    "title": article["title"],
                    "description": desc,
                    "content": content,
                    "url": url,
                    "source": article.get("source", {}).get("name", ""),
                    "original_rank": i,
                    "id": aid,
                }
                categorized[our_section].append(art)

    return categorized


# --- Step 2: Embed ---

def embed_articles(articles: list[dict]) -> list[dict]:
    """Generate embeddings for all articles using Gemini embedding model."""
    if not _gemini_api_key() or not articles:
        return articles

    client = _genai_client()
    texts = [f"{a['title']} — {a.get('description', '')}" for a in articles]

    try:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts,
        )
        for article, embedding in zip(articles, result.embeddings):
            article["embedding"] = list(embedding.values)
    except Exception as e:
        print(f"Embedding error: {e}")

    return articles


# --- Step 3: Score & Rank ---

def score_and_rank(section: str, articles: list[dict]) -> list[dict]:
    """Score articles by cosine similarity to user's preference vector for this section."""
    pref_vector = get_preference_vector(section)

    is_cold_start = all(x == 0.0 for x in pref_vector)

    for article in articles:
        if is_cold_start or "embedding" not in article:
            article["score"] = 0.0
        else:
            article["score"] = cosine_similarity(article["embedding"], pref_vector)

    articles.sort(key=lambda a: (-a["score"], a.get("original_rank", 0)))
    return articles


# --- Step 4: Summarize ---

def summarize_with_gemini(section_name: str, articles: list[dict]) -> SectionSummary:
    """Use Gemini to generate section summary and substory summaries."""
    if not _gemini_api_key() or not articles:
        return _fallback_section(section_name, articles)

    client = _genai_client()

    articles_text = "\n\n".join(
        f"ARTICLE {i+1}:\nTitle: {a['title']}\nSource: {a.get('source', 'Unknown')}\n"
        f"Content: {a.get('content', a.get('description', ''))}"
        for i, a in enumerate(articles[:3])
    )

    prompt = f"""You are a news digest writer. Given these {section_name} articles, produce a JSON response with:
1. "section_summary": A 1-2 paragraph overview of today's top {section_name} news (combine themes across all articles)
2. "substories": An array of exactly {len(articles[:3])} objects, one per article, each with:
   - "title": A clean, concise headline (rewrite if needed)
   - "summary": A 1-paragraph summary of the article

Articles:
{articles_text}

Respond ONLY with valid JSON, no markdown fences:
{{"section_summary": "...", "substories": [{{"title": "...", "summary": "..."}}]}}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        parsed = json.loads(text)

        substories = []
        for i, (sub, article) in enumerate(zip(parsed["substories"], articles[:3])):
            substories.append(Substory(
                id=article["id"],
                title=sub["title"],
                summary=sub["summary"],
                url=article.get("url", ""),
            ))

        return SectionSummary(
            section=section_name,
            summary=parsed["section_summary"],
            substories=substories,
        )
    except Exception as e:
        print(f"Gemini summarization error for {section_name}: {e}")
        return _fallback_section(section_name, articles)


def summarize_single_article(article: dict) -> Substory:
    """Summarize a single replacement article with Gemini."""
    if not _gemini_api_key():
        return Substory(
            id=article["id"],
            title=article.get("title", "Untitled"),
            summary=article.get("description") or article.get("content", "No summary available."),
            url=article.get("url", ""),
        )

    client = _genai_client()
    prompt = f"""Summarize this news article in one paragraph. Also produce a clean, concise headline.

Title: {article.get('title', '')}
Content: {article.get('content', article.get('description', ''))}

Respond ONLY with valid JSON, no markdown fences:
{{"title": "...", "summary": "..."}}"""

    try:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        parsed = json.loads(text)
        return Substory(
            id=article["id"],
            title=parsed["title"],
            summary=parsed["summary"],
            url=article.get("url", ""),
        )
    except Exception as e:
        print(f"Single article summarization error: {e}")
        return Substory(
            id=article["id"],
            title=article.get("title", "Untitled"),
            summary=_clean_text(article.get("description") or "No summary available."),
            url=article.get("url", ""),
        )


def _clean_text(text: str) -> str:
    """Strip NewsAPI truncation artifacts from text."""
    if not text:
        return text
    # Remove "[+N chars]" suffix
    text = text.split("… [+")[0].split("... [+")[0]
    # Remove trailing ellipsis only if it looks like truncation (at end of text)
    text = text.rstrip()
    if text.endswith("..."):
        text = text[:-3].rstrip()
    if text.endswith("…"):
        text = text[:-1].rstrip()
    # End with a period if it doesn't already have terminal punctuation
    if text and text[-1] not in ".!?\"'":
        text += "."
    return text


def _fallback_section(section_name: str, articles: list[dict]) -> SectionSummary:
    """Fallback when Gemini is unavailable."""
    substories = []
    for a in articles[:3]:
        summary = a.get("description") or a.get("content", "No summary available.")
        substories.append(Substory(
            id=a.get("id", _article_id(a.get("url", ""), a.get("title", ""))),
            title=a.get("title", "Untitled"),
            summary=_clean_text(summary),
            url=a.get("url", ""),
        ))

    while len(substories) < 3:
        substories.append(Substory(
            id=f"{section_name}-placeholder-{len(substories)+1}",
            title="No additional stories",
            summary="Check back later for more stories in this section.",
            url="",
        ))

    return SectionSummary(
        section=section_name,
        summary=f"Today's top {section_name} headlines.",
        substories=substories[:3],
    )


# --- Full Pipeline ---

def generate_digest() -> DailyDigest:
    """Full pipeline: fetch → embed → score → pick top 3 → summarize."""
    today = date.today().isoformat()
    categorized = fetch_articles()

    sections = []
    selected_ids = []

    for section_name in SECTIONS:
        articles = categorized[section_name]

        # Embed all candidates
        articles = embed_articles(articles)

        # Save all articles to DB
        for a in articles:
            save_article(
                article_id=a["id"],
                title=a["title"],
                url=a.get("url", ""),
                source=a.get("source", ""),
                section=section_name,
                embedding=a.get("embedding", []),
                fetched_date=today,
            )

        # Score and rank by preference
        articles = score_and_rank(section_name, articles)

        # Pick top 3
        top = articles[:3]

        # Summarize
        section = summarize_with_gemini(section_name, top)
        sections.append(section)

        selected_ids.extend(a["id"] for a in top)

    # Mark selected articles
    mark_selected(selected_ids)

    return DailyDigest(date=today, sections=sections)


if __name__ == "__main__":
    from database import init_db
    init_db()
    digest = generate_digest()
    print(json.dumps(digest.model_dump(), indent=2))
