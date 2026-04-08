import json
import os
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import DailyDigest, Feedback, Substory
from mock_data import MOCK_DIGEST
from generator import generate_digest, summarize_single_article, score_and_rank
from database import (
    init_db, get_article, save_feedback, update_preference_vector,
    get_section_candidates, get_preference_vector, cosine_similarity,
    mark_selected,
)

load_dotenv()

app = FastAPI(title="AI Newsletter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init DB on startup
init_db()

# In-memory cache
cached_digest: DailyDigest | None = None
cached_date: str | None = None


@app.get("/digest/today", response_model=DailyDigest)
def get_today_digest():
    """Return today's digest. Generates with real APIs if keys are set, otherwise mock data."""
    global cached_digest, cached_date

    today = datetime.now().strftime("%Y-%m-%d")

    if cached_digest and cached_date == today:
        return cached_digest

    if os.environ.get("NEWS_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        try:
            cached_digest = generate_digest()
            cached_date = today
            return cached_digest
        except Exception as e:
            print(f"Generation failed, falling back to mock: {e}")

    return MOCK_DIGEST


@app.post("/feedback")
def post_feedback(feedback: Feedback):
    """Record feedback, update preferences. On dislike, swap in a replacement article."""
    global cached_digest

    article = get_article(feedback.article_id)
    if not article:
        return {"status": "error", "message": "article not found"}

    # Save feedback
    save_feedback(feedback.article_id, feedback.reaction, feedback.timestamp)

    # Update preference vector
    embedding = json.loads(article["embedding"]) if article["embedding"] else []
    if embedding:
        update_preference_vector(article["section"], embedding, feedback.reaction)

    # On dislike: find a replacement and update the cached digest
    replacement = None
    if feedback.reaction == "dislike" and cached_digest:
        section_name = article["section"]
        today = datetime.now().strftime("%Y-%m-%d")

        # Get IDs of currently shown articles in this section
        current_ids = []
        for sec in cached_digest.sections:
            if sec.section == section_name:
                current_ids = [s.id for s in sec.substories]
                break

        # Find candidates not currently shown
        candidates = get_section_candidates(section_name, today, current_ids)

        if candidates:
            # Score candidates against updated preference vector
            pref_vector = get_preference_vector(section_name)
            is_cold_start = all(x == 0.0 for x in pref_vector)

            for c in candidates:
                if is_cold_start or not c.get("embedding"):
                    c["score"] = 0.0
                else:
                    c["score"] = cosine_similarity(c["embedding"], pref_vector)

            candidates.sort(key=lambda c: -c["score"])
            best = candidates[0]

            # Summarize the replacement
            replacement = summarize_single_article(best)
            mark_selected([best["id"]])

            # Update cached digest — swap the disliked article for the replacement
            for sec in cached_digest.sections:
                if sec.section == section_name:
                    sec.substories = [
                        replacement if s.id == feedback.article_id else s
                        for s in sec.substories
                    ]
                    break

    return {
        "status": "ok",
        "section": article["section"],
        "replacement": replacement.model_dump() if replacement else None,
    }


@app.get("/feedback")
def get_all_feedback():
    """Debug: view all feedback."""
    from database import get_conn
    conn = get_conn()
    rows = conn.execute("SELECT * FROM feedback ORDER BY timestamp DESC LIMIT 50").fetchall()
    conn.close()
    return {"feedback": [dict(r) for r in rows]}


@app.get("/preferences")
def get_preferences():
    """Debug: view preference vector stats per section."""
    from database import get_conn
    conn = get_conn()
    rows = conn.execute("SELECT section, feedback_count, updated_at FROM preferences").fetchall()
    conn.close()
    return {"preferences": [dict(r) for r in rows]}
