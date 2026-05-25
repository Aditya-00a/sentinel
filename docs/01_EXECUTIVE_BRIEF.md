# SENTINEL
## Pre-Escalation Behavioral Intelligence System
### Executive Brief

---

**Author:** Aditya Sakhale | MS Management & Analytics, NYU Stern 2026
**Contact:** as18513@nyu.edu | linkedin.com/in/adityasakhale
**Live Demo:** [sentinel demo link]
**Source:** github.com/Aditya-00a/sentinel

---

## The Problem

The gaming industry's moderation systems are reactive. They wait for a report, review it, and punish. This pipeline has gotten remarkably good at detection, yet players still don't feel safer despite more bans than ever. The issue is timing: by the time a report is filed, the damage to community health is already done. The teammate already tilted. The lobby already collapsed. The player who might have been saved already escalated.

The unsolved problem isn't better detection. It's earlier intervention.

## What Sentinel Does

Sentinel is a working prototype of a pre-escalation intelligence system. It treats player behavior as a public health problem, not a criminal justice one.

Instead of asking *"did this player break a rule?"*, Sentinel asks:

> *"Is this player on a trajectory toward breaking a rule, and what is the minimum intervention that can change their course?"*

The system analyzes multi-session behavioral trajectories (not single-game snapshots) to forecast behavioral spirals before they manifest as reportable incidents, then recommends graduated, proportional interventions calibrated by an effectiveness auditor that explicitly penalizes overreaction.

## How It Works

Five specialized AI agents run in a structured pipeline:

| Phase | Agent | Function |
|-------|-------|----------|
| 1 (parallel) | **Trajectory** | Forecasts behavioral health direction, velocity, and 3-session prediction |
| 1 (parallel) | **Context** | Identifies behavioral drivers (promo tilt, fatigue, duo dependency, role swap) |
| 2 (sequential) | **Intervention** | Recommends minimum effective dose (nudge, adjust, monitor, escalate) |
| 3 (sequential) | **Effectiveness** | Audits false-positive risk, proportionality, and harm-if-wrong |
| 4 (synthesis) | **Orchestrator** | Produces final graduated decision with explainability trail |

## Five Graduated Response Levels

| Decision | When It Applies |
|----------|----------------|
| **NO_ACTION** | Healthy or recovering. No intervention needed. |
| **NUDGE** | Minor drift. Cooldown suggestion, positive reinforcement. |
| **ADJUST** | Environmental fix. Matchmaking tuning, time-of-day recommendations. |
| **MONITOR** | Ambiguous signal. Watch list with auto re-evaluation. |
| **ESCALATE** | Confirmed spiral. Flag for immediate human review. |

## What Makes This Different

| Traditional Moderation | Sentinel |
|----------------------|----------|
| Reactive (post-report) | Proactive (pre-escalation) |
| Punishment-oriented | Intervention-oriented |
| Binary (ban or don't) | Five graduated response levels |
| Single-game snapshot | Multi-session trajectory analysis |
| Opaque decisions | Explainable audit trail on every recommendation |
| Confidence-blind | Calibrated uncertainty with false-positive auditing |

## Built-In Safety Rails

Sentinel's architecture embeds model risk governance principles (aligned with SR 11-7):

- **Effectiveness Agent as system conscience**: Every recommendation is audited for false-positive risk before the Orchestrator sees it. The system explicitly penalizes overreaction.
- **Decision rules prevent runaway escalation**: ESCALATE is blocked when false-positive risk exceeds 0.4 or when harm-if-wrong is HIGH with insufficient evidence.
- **Explainability trail**: Every recommendation includes a plain-English audit trail a behavioral health specialist can follow.
- **Dissent surfacing**: When agents disagree, the Orchestrator documents the disagreement rather than suppressing it.

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.13, FastAPI, SSE streaming |
| LLM Engine | Groq (Llama 3.3 70B) with structured JSON output |
| Game Data | Riot Games API (Match-V5, Account-V1) with 3-tier fallback |
| Frontend | React 18, Vite, Tailwind CSS |
| Storage | SQLite (7-day cache TTL) |

## Demo Profiles

Eight curated behavioral trajectories covering the full decision spectrum:

- **Cascade Spiral** (ESCALATE) - One bad game triggers 72h of escalating toxicity
- **Steady Decline** (MONITOR) - 3-week progressive tilt, KDA dropping, chat flags rising
- **Slow Burn Griefing** (MONITOR) - Never triggers chat detection, pattern clear in aggregate
- **Night Tilter** (ADJUST) - Fine during daytime, toxic in late-night sessions
- **Promo Tilt** (NUDGE) - Stable normally, spirals hard after failed promos
- **Duo Dependent** (NUDGE) - Great teammate when duo'd, progressively toxic solo
- **False Alarm** (NO_ACTION) - Stats look like decline, actually learning a new role
- **Comeback Kid** (NO_ACTION) - Was declining, received nudge, behavior recovered

## Why This Matters for Riot

This architecture addresses the gap between Riot's existing detection excellence and the player experience problem that detection alone cannot solve. The prediction-first approach creates an intervention window that doesn't exist in reactive systems. It's designed to complement existing systems (behavioral detection, reporting infrastructure, tribunal frameworks), not replace them.

The minimum-effective-dose philosophy aligns with Riot's player-first values: the lightest intervention that changes a trajectory is always preferred over the heaviest punishment that a violation technically justifies.

---

*Independent concept demo built using the public Riot Games API. Not affiliated with, endorsed by, or sponsored by Riot Games. League of Legends, Valorant, and Riot Games are trademarks of Riot Games, Inc.*
