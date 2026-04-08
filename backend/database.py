"""SQLite database layer for articles, feedback, and preference vectors."""

import json
import math
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "newsletter.db")
EMBEDDING_DIM = 3072


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT,
            source TEXT,
            section TEXT NOT NULL,
            embedding TEXT,
            fetched_date TEXT NOT NULL,
            was_selected INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT NOT NULL,
            reaction TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (article_id) REFERENCES articles(id)
        );

        CREATE TABLE IF NOT EXISTS preferences (
            section TEXT PRIMARY KEY,
            vector TEXT NOT NULL,
            feedback_count INTEGER DEFAULT 0,
            updated_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# --- Articles ---

def save_article(article_id: str, title: str, url: str, source: str,
                 section: str, embedding: list[float], fetched_date: str):
    conn = get_conn()
    conn.execute(
        """INSERT OR IGNORE INTO articles (id, title, url, source, section, embedding, fetched_date, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (article_id, title, url, source, section,
         json.dumps(embedding), fetched_date, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def mark_selected(article_ids: list[str]):
    if not article_ids:
        return
    conn = get_conn()
    placeholders = ",".join("?" * len(article_ids))
    conn.execute(
        f"UPDATE articles SET was_selected = 1 WHERE id IN ({placeholders})",
        article_ids,
    )
    conn.commit()
    conn.close()


def get_article(article_id: str) -> dict | None:
    conn = get_conn()
    row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


# --- Feedback ---

def save_feedback(article_id: str, reaction: str, timestamp: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO feedback (article_id, reaction, timestamp) VALUES (?, ?, ?)",
        (article_id, reaction, timestamp),
    )
    conn.commit()
    conn.close()


# --- Preference Vectors ---

def _zero_vector() -> list[float]:
    return [0.0] * EMBEDDING_DIM


def get_preference_vector(section: str) -> list[float]:
    conn = get_conn()
    row = conn.execute("SELECT vector FROM preferences WHERE section = ?", (section,)).fetchone()
    conn.close()
    if row:
        return json.loads(row["vector"])
    return _zero_vector()


def update_preference_vector(section: str, article_embedding: list[float], reaction: str):
    """Add (like) or subtract (dislike) the article embedding from the section preference vector."""
    pref = get_preference_vector(section)
    sign = 1.0 if reaction == "like" else -1.0

    # Update: pref += sign * embedding
    for i in range(len(pref)):
        pref[i] += sign * article_embedding[i]

    # Normalize
    magnitude = math.sqrt(sum(x * x for x in pref))
    if magnitude > 0:
        pref = [x / magnitude for x in pref]

    conn = get_conn()
    conn.execute(
        """INSERT INTO preferences (section, vector, feedback_count, updated_at)
           VALUES (?, ?, 1, ?)
           ON CONFLICT(section) DO UPDATE SET
             vector = excluded.vector,
             feedback_count = feedback_count + 1,
             updated_at = excluded.updated_at""",
        (section, json.dumps(pref), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


# --- Queries ---

def get_section_candidates(section: str, fetched_date: str, exclude_ids: list[str]) -> list[dict]:
    """Get all articles for a section/date, excluding specific IDs. Returns with parsed embeddings."""
    conn = get_conn()
    placeholders = ",".join("?" * len(exclude_ids)) if exclude_ids else "''"
    rows = conn.execute(
        f"""SELECT id, title, url, source, section, embedding
            FROM articles
            WHERE section = ? AND fetched_date = ? AND id NOT IN ({placeholders})
            ORDER BY created_at""",
        [section, fetched_date] + exclude_ids,
    ).fetchall()
    conn.close()

    candidates = []
    for row in rows:
        d = dict(row)
        d["embedding"] = json.loads(d["embedding"]) if d["embedding"] else []
        candidates.append(d)
    return candidates


# --- Scoring ---

def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
