# SENTINEL
## Demo Walkthrough Guide
### How to Run and Evaluate the System

---

## Quick Start (30 seconds)

1. Open the demo at **[live URL]**
2. Click any trajectory profile (e.g., **"Cascade Spiral"** for the most dramatic result)
3. Watch the four agents analyze in real-time (8-15 seconds)
4. Review the graduated decision, explainability trail, and recommended actions
5. Click **"Download Audit JSON"** to inspect the full structured output

---

## What You're Looking At

### The Homepage

The main interface presents two ways to analyze a player:

- **Riot ID input** (top): Enter a real Riot ID (e.g., `Player#NA1`) to fetch live match data from the Riot API and run the full prediction pipeline against real behavioral data
- **Trajectory profiles** (bottom): Eight pre-built behavioral scenarios covering every decision level. These are the recommended starting point for evaluation.

The **data mode badge** (top-right) shows which data tier is active:
- **LIVE** (green): Real Riot API data
- **CACHED** (amber): Previously fetched data from local cache
- **DEMO** (blue): Curated trajectory profiles

### The Agent Grid

After selecting a profile, four agent cards appear and transition from "thinking" to "done" as SSE events stream in:

| Card | What It Shows |
|------|--------------|
| **Trajectory** | Current health, baseline comparison, 3-session prediction, trajectory direction, decline velocity |
| **Context** | Primary behavioral trigger, contributing factors, temporal patterns, emotional state estimate |
| **Intervention** | Recommended intervention type, specific actions, urgency level, expected effectiveness |
| **Effectiveness** | False-positive risk, intervention appropriateness, harm-if-wrong assessment, alternative explanations |

Each card includes a raw JSON toggle for the complete structured output.

### The Decision Panel

The Orchestrator's final recommendation appears with:

- **Decision badge** (color-coded): NO_ACTION / NUDGE / ADJUST / MONITOR / ESCALATE
- **Severity and confidence** scores
- **Executive summary** (2-sentence human-readable assessment)
- **Recommended actions** (checkable list for behavioral health team workflow)
- **Dissent notes** (surfaced when agents disagreed)
- **Explainability trail** (numbered plain-English audit bullets)

---

## Recommended Evaluation Path

### Demo 1: "Cascade Spiral" (Expected: ESCALATE)

**What it shows:** The most severe case. One bad game with an AFK triggered 72 hours of escalating toxicity. Health dropped from 0.70 to 0.12 across 10 sessions.

**What to look for:**
- Trajectory Agent should detect "spiraling" direction with high decline velocity
- Context Agent should identify the AFK incident as the cascade trigger
- Intervention Agent should recommend proactive outreach (not just a nudge)
- Effectiveness Agent should confirm low false-positive risk
- Orchestrator should issue ESCALATE with high confidence

### Demo 2: "False Alarm" (Expected: NO_ACTION)

**What it shows:** A player whose stats look like decline but is actually learning a new role. The Effectiveness Agent should catch this.

**What to look for:**
- Trajectory Agent may flag declining health (the stats genuinely look bad)
- Context Agent should identify role/champion experimentation
- Effectiveness Agent should flag HIGH false-positive risk
- Orchestrator should override to NO_ACTION despite the declining numbers

**Why this matters:** This demonstrates the system's built-in restraint. A naive system would escalate this player. Sentinel's effectiveness auditing prevents it.

### Demo 3: "Night Tilter" (Expected: ADJUST)

**What it shows:** A player who performs normally during daytime but becomes toxic in late-night sessions. The fix is environmental (time-of-day), not behavioral (punishment).

**What to look for:**
- Context Agent should identify the temporal pattern
- Intervention Agent should recommend matchmaking/queue adjustments, not punitive action
- Orchestrator should issue ADJUST (system-level fix, no player contact needed)

### Demo 4: "Comeback Kid" (Expected: NO_ACTION)

**What it shows:** A previously declining player who received a cooldown nudge and recovered. Behavioral health is now trending upward.

**What to look for:**
- Trajectory Agent should detect "recovering" direction
- Intervention history shows a previous nudge that worked
- Orchestrator should issue NO_ACTION (the system worked; don't over-intervene)

**Why this matters:** Demonstrates the feedback loop concept. Interventions should have measurable outcomes.

---

## Comparing Two Profiles Side-by-Side

For a compelling evaluation, run **"Cascade Spiral"** and **"False Alarm"** back-to-back. Both show declining health metrics, but the system reaches opposite conclusions. The difference is the Effectiveness Agent's false-positive risk assessment, which demonstrates that the architecture can distinguish genuine spirals from noise.

---

## Downloading the Audit JSON

Click **"Download Audit JSON"** on any result to get the complete structured output:

```json
{
  "id": "uuid",
  "timestamp": "ISO-8601",
  "game": "lol",
  "riot_id": "PlayerName#Tag",
  "data_mode": "demo",
  "trajectory": { ... },
  "context": { ... },
  "intervention": { ... },
  "effectiveness": { ... },
  "orchestrator": {
    "decision": "MONITOR",
    "severity": "MEDIUM",
    "confidence": 0.71,
    "executive_summary": "...",
    "recommended_actions": [...],
    "dissent_notes": "...",
    "explainability_trail": [...]
  }
}
```

This is the artifact a behavioral health team would receive. Every field is structured, queryable, and auditable.

---

## Architecture Page

Click **"SYSTEM"** in the top navigation to view the How It Works page, which explains:
- The problem framing (public health vs. policing)
- Agent pipeline architecture with flow diagram
- Each agent's role and responsibilities
- Five graduated decision levels
- Current limitations and production requirements

---

## Notes for Evaluators

1. **The demo always works** even without a Riot API key. Demo mode provides curated trajectories that showcase every decision level.

2. **Each review makes 5 LLM calls** (Trajectory + Context in parallel, then Intervention, Effectiveness, Orchestrator sequentially). Total latency is typically 8-15 seconds.

3. **Results may vary slightly** between runs because LLM inference is non-deterministic. The expected decisions are calibrated but not hard-coded; the agents genuinely analyze the data each time.

4. **The Download Audit JSON** button exports the exact structured output that would feed into a production behavioral health dashboard.

---

*Independent concept demo built using the public Riot Games API. Not affiliated with, endorsed by, or sponsored by Riot Games.*
