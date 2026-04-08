# Daily Digest AI

Daily Digest AI is an application that aggregates, filters, and summarizes the most important global news into a concise, structured format. It is designed to reduce information overload by delivering a high-signal daily briefing across key domains.

## Overview

The product provides a consistent daily digest composed of four core sections:

* Sports
* Technology
* Finance
* World

Each section includes:

* A 1–2 paragraph synthesized summary of the day’s developments
* Three curated substories, each with:

  * A short summary
  * A source link for deeper reading

In total, each digest contains 4 summaries and 12 substories, optimized for fast consumption.

## Problem

News consumption today is fragmented and inefficient. Users are forced to navigate multiple sources, encounter repeated content, and filter out low-quality information. This results in high time cost and low retention of meaningful insights.

## Solution

Daily Digest AI addresses this by:

* Aggregating content from multiple sources
* Deduplicating overlapping coverage
* Ranking stories by relevance and novelty
* Generating structured summaries using large language models

The result is a single, coherent daily briefing that prioritizes clarity and relevance.

## Product Features

* Fixed, high-signal format (4 sections, 12 stories)
* AI-generated summaries for rapid comprehension
* Source attribution with outbound links
* User feedback via like/dislike signals
* Iterative personalization based on interaction data

## Architecture

### Frontend

* Built with Expo (React Native)
* Core screens:

  * Home (daily digest)
  * Story detail
  * Preferences
  * History (planned)

### Backend

* Python-based pipeline
* Responsibilities:

  * News ingestion (APIs, RSS, email sources)
  * Content parsing and normalization
  * Story classification into sections
  * Deduplication and clustering
  * Ranking and selection (top 3 per section)
  * LLM-based summarization
  * JSON API delivery

### API

* `GET /digest/today`
* `GET /digest/:date`
* `POST /feedback`

## Data Model

* **DailyDigest**: date, sections
* **SectionSummary**: section, summary, substories
* **Substory**: id, title, summary, url, source, timestamp
* **Feedback**: substoryId, vote, timestamp

## Personalization

The system incorporates user feedback to improve relevance over time:

* Short term: adjusts section and story weighting based on likes/dislikes
* Long term: ranks stories using similarity to previously preferred content

## Roadmap

* Personalized ranking using embeddings
* Push notifications for daily delivery
* Expanded source coverage
* Web client
* Multi-user support and accounts

## Getting Started

```bash
git clone https://github.com/yourusername/daily-digest-ai
cd daily-digest-ai
npm install
npx expo start
```

## Vision

Daily Digest AI aims to become the default interface for consuming daily information: a system that replaces fragmented browsing with a single, reliable, and continuously improving source of truth.

## License

MIT
