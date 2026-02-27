# Sales Co-Pilot — Frontend

React + inline-CSS chat interface for the Sales Co-Pilot hackathon project.

## Quick Start

```bash
cd frontend
npm install
npm start          # → http://localhost:3000
```

Backend must be running at `http://localhost:8000`.

## Features

| Component | Description |
|---|---|
| ChatWindow | Scrollable conversation thread, auto-scroll, typing indicator |
| StarterQueries | 3 clickable starter prompts shown on empty chat |
| MessageBubble | Renders user/assistant messages; supports markdown in answers |
| ConfidenceBadge | 🟢 High / 🟡 Medium / 🔴 Low indicator with score % |
| CitationPanel | Expandable citation chips — shows chunk text, page, Drive link |
| GuardrailAlert | Orange alert banner when a guardrail fires |
| FeedbackButtons | Thumbs up/down per answer (stored locally) |
| AdminPanel | Pipeline stats table + Re-ingest button |

## Pages

- **Chat** (default) — main conversation interface
- **Admin** — pipeline stats, document index, re-ingest trigger

## API Endpoints Used

| Method | Path | Used for |
|---|---|---|
| POST | /session/create | On app load and "New Chat" |
| POST | /query | Every user message |
| GET | /session/{id}/history | (available if needed for reload) |
| GET | /admin/pipeline | Admin panel on load |
| POST | /ingest | Re-ingest button |
| GET | /health | (available for status check) |
