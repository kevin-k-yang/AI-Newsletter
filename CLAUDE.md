# CLAUDE.md

## Project Overview

AI-powered daily news digest app with personalized article ranking via vector embeddings.

- **Frontend**: Expo (React Native) with expo-router, TypeScript
- **Backend**: Python FastAPI server with SQLite persistence
- **AI**: Google Gemini (embedding + summarization)
- **News Source**: NewsAPI.org

## Architecture

### Pipeline
```
NewsAPI (10 articles/category) → Gemini embeddings (3072-dim) → cosine similarity scoring against user preference vector → top 3 per section → Gemini Flash summarization → JSON API
```

### Personalization
- Each article is embedded with `gemini-embedding-001` (3072-dim vectors)
- Per-section preference vectors stored in SQLite `preferences` table
- Like: `pref += article_embedding`, normalized
- Dislike: `pref -= article_embedding`, normalized, article swapped out immediately
- Cold start: zero vector → falls back to NewsAPI ordering

### Sections
sports, tech, finance, world — 3 articles each, 12 total per digest

## Running Locally

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Add keys to .env: NEWS_API_KEY, GEMINI_API_KEY
uvicorn app:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npx expo start
```

## Key Files

### Backend (`backend/`)
- `app.py` — FastAPI server, endpoints, cache, feedback→swap logic
- `generator.py` — Full pipeline: fetch → embed → score → rank → summarize
- `database.py` — SQLite schema (articles, feedback, preferences), vector ops
- `models.py` — Pydantic models: DailyDigest, SectionSummary, Substory, Feedback
- `mock_data.py` — Fallback mock digest

### Frontend (`frontend/`)
- `app/index.tsx` — Home screen, fetches digest, handles feedback callbacks
- `app/story/[id].tsx` — Story detail with full summary + link
- `components/SectionCard.tsx` — Section header + substory list
- `components/SubstoryCard.tsx` — Article card with like/dislike, navigates to detail
- `constants/api.ts` — Shared API_URL (handles Android vs iOS)
- `constants/colors.ts` — Theme colors, section color map, icons
- `types.ts` — TypeScript interfaces matching backend models
- `data/mockDigest.ts` — Client-side fallback data

## API Endpoints
- `GET /digest/today` — Returns cached daily digest (generates on first call)
- `POST /feedback` — `{article_id, reaction, timestamp}` — updates preferences; on dislike returns replacement article
- `GET /feedback` — Debug: list all feedback
- `GET /preferences` — Debug: preference vector stats per section

## Conventions
- Article IDs are `md5(url)[:12]` — stable, deduped across sections
- Gemini SDK: uses `google-genai` (new SDK), NOT deprecated `google-generativeai`
- `.env` in `backend/` holds API keys — never commit
- `newsletter.db` is auto-created in `backend/` — gitignored
- Frontend reads from API on mount, falls back to mock data if backend unreachable
