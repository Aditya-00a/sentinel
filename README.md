# SENTINEL

**Pre-Escalation Behavioral Intelligence System**

> Predict the spiral. Intervene before it happens. Four agents forecast player behavioral trajectories and recommend proportional interventions — treating community health like public health, not policing.

[![Run on Replit](https://replit.com/badge/github/adityasakhale/sentinel)](https://replit.com)

---

## Why This Matters

The gaming industry has gotten very good at detecting toxicity after it happens. Players still don't feel safer despite more bans than ever. The unsolved problem isn't better detection — it's earlier intervention. Sentinel demonstrates a prediction-first architecture: forecast behavioral spirals across multi-session trajectories, recommend the minimum effective intervention, and audit every recommendation for false-positive risk and proportionality. This is aligned with SR 11-7 model risk governance: explainability and calibrated uncertainty built into the architecture, not bolted on after.

---

## Architecture

```
  Player Session History (multi-session trajectory data)
          |
          +---------------------------+
          v                           v
  +------------------+    +------------------+
  |   Trajectory     |    |    Context       |
  |    Agent         |    |    Agent         |
  | (health score    |    | (triggers,       |
  |  forecasting,    |    |  temporal        |
  |  trend analysis) |    |  patterns)       |
  +--------+---------+    +--------+---------+
           |                       |
           +----------+------------+
                      v
              +------------------+
              |  Intervention    |
              |    Agent         |
              | (minimum dose   |
              |  recommendation)|
              +--------+---------+
                       v
              +------------------+
              |  Effectiveness   |
              |    Agent         |
              | (false positive, |
              |  proportionality)|
              +--------+---------+
                       v
              +------------------+
              |  Orchestrator    |
              | (NO_ACTION /     |
              |  NUDGE / ADJUST /|
              |  MONITOR /       |
              |  ESCALATE)       |
              +------------------+
```

Trajectory + Context run in parallel. Intervention uses both results. Effectiveness audits everything. Orchestrator synthesizes the final graduated decision.

---

## Agents

| Agent | Role |
|-------|------|
| **Trajectory** | Forecasts behavioral health across sessions. Current vs baseline health, predicted health in 3 sessions, decline velocity, trajectory direction (stable/declining/recovering/spiraling). |
| **Context** | Identifies what's driving behavioral change. Failed promos? Late-night fatigue? Solo queue without duo? Role swap? Context determines whether a decline is concerning or perfectly normal. |
| **Intervention** | Recommends the minimum effective intervention. Cooldown suggestions, matchmaking adjustments, positive reinforcement, social nudges, or proactive outreach — graduated by severity. |
| **Effectiveness** | The system's conscience. Evaluates false-positive risk, intervention appropriateness, harm-if-wrong, and alternative explanations. Explicitly penalizes overreaction. |
| **Orchestrator** | Synthesizes all four into a final decision with a plain-English explainability trail. Surfaces agent disagreements. |

---

## Decisions

Five graduated response levels instead of binary ban/don't-ban:

| Decision | Color | Meaning |
|----------|-------|---------|
| **NO_ACTION** | Green | Player is healthy or recovering. No intervention needed. |
| **NUDGE** | Blue | Gentle behavioral nudge. Cooldown suggestion, positive reinforcement. |
| **ADJUST** | Amber | Environmental adjustment. Matchmaking tuning, time-of-day recommendations. |
| **MONITOR** | Orange | Increased observation. Flag for behavioral health team review. |
| **ESCALATE** | Red | Active spiral detected. Proactive outreach or restrictive intervention. |

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, FastAPI, uvicorn |
| LLM | Groq (llama-3.3-70b-versatile) |
| Game Data | Riot Games API (Match-V5, Account-V1) |
| Frontend | React 18, Vite, Tailwind CSS |
| Storage | SQLite (cache) |
| Deploy | Replit / Docker / Render |

---

## Smart API Fallback

Riot dev API keys expire every 24 hours. Sentinel handles this with a three-tier fallback:

1. **Live mode** (green badge) — Real Riot API data, converted to session trajectories
2. **Cached mode** (amber badge) — Cached data from SQLite (7-day TTL)
3. **Demo mode** (blue badge) — 8 curated behavioral trajectories covering every decision type

The demo always works, even without a Riot API key.

---

## Demo Profiles

| Profile | Pattern | Expected Decision |
|---------|---------|-------------------|
| Steady Decline | 3-week progressive tilt, KDA dropping, chat flags rising | MONITOR |
| Promo Tilt | Stable normally, spirals hard after failed promos | NUDGE |
| Night Tilter | Fine during daytime, toxic in late-night sessions | ADJUST |
| Duo Dependent | Great teammate when duo'd, progressively toxic solo | NUDGE |
| Comeback Kid | Was declining, received nudge, behavior recovered | NO_ACTION |
| False Alarm | Stats look like decline, actually learning new role | NO_ACTION |
| Slow Burn Griefing | Never triggers chat detection, pattern clear in aggregate | MONITOR |
| Cascade Spiral | One bad game triggered 72 hours of escalating toxicity | ESCALATE |

---

## Setup

### Local Development

```bash
# Clone
git clone <repo-url> && cd sentinel

# Backend
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && npm run build && cd ..

# Environment
cp .env.example .env
# Edit .env with your GROQ_API_KEY and optional RIOT_API_KEY

# Run
PYTHONPATH=. uvicorn backend.main:app --reload
```

### Replit

1. Fork this repl
2. Add `GROQ_API_KEY` to Secrets
3. Optionally add `RIOT_API_KEY` (demo works without it)
4. Click Run

### Docker

```bash
docker build -t sentinel .
docker run -p 8000:8000 -e GROQ_API_KEY=... -e RIOT_API_KEY=... sentinel
```

---

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/review` | POST | Forecast a player (SSE stream) |
| `/api/review-demo/{id}` | POST | Forecast a demo profile (SSE stream) |
| `/api/demo-profiles` | GET | List demo profiles |
| `/api/data-mode` | GET | Current data source status |
| `/health` | GET | Liveness check |

---

## Disclaimer

Independent concept demo by Aditya Sakhale, built using the public Riot Games API. Not affiliated with, endorsed by, or sponsored by Riot Games. League of Legends, Valorant, and Riot Games are trademarks of Riot Games, Inc.
