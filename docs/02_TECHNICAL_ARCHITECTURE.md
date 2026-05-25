# SENTINEL
## Technical Architecture Document
### Pre-Escalation Behavioral Intelligence System

---

**Author:** Aditya Sakhale | as18513@nyu.edu
**Version:** 2.0.0 | May 2026

---

## 1. System Overview

Sentinel is a multi-agent behavioral forecasting system that analyzes player session trajectories across time to predict behavioral spirals and recommend graduated, proportional interventions. The system operates as a five-agent pipeline with structured dependencies, SSE-streamed progressive results, and built-in effectiveness auditing.

### Design Principles
- **Prediction over detection**: Forecast behavioral spirals before they become reportable incidents
- **Minimum effective dose**: Always recommend the lightest intervention that changes the trajectory
- **Calibrated uncertainty**: Express and propagate uncertainty rather than suppressing it
- **Explainability by default**: Every recommendation carries a plain-English audit trail
- **Graceful degradation**: 3-tier data fallback ensures the system always produces a result

---

## 2. Agent Pipeline Architecture

```
  Player Multi-Session Trajectory Data
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
                      |
              +------------------+
              |  Intervention    |
              |    Agent         |
              | (minimum dose   |
              |  recommendation)|
              +--------+---------+
                       |
              +------------------+
              |  Effectiveness   |
              |    Agent         |
              | (false positive, |
              |  proportionality)|
              +--------+---------+
                       |
              +------------------+
              |  Orchestrator    |
              | (graduated       |
              |  decision with   |
              |  explainability) |
              +------------------+
```

### Phase Execution

| Phase | Agents | Execution | Rationale |
|-------|--------|-----------|-----------|
| 1 | Trajectory + Context | **Parallel** (asyncio) | Independent analyses that don't depend on each other |
| 2 | Intervention | **Sequential** | Requires both Trajectory and Context outputs to recommend proportional action |
| 3 | Effectiveness | **Sequential** | Audits Trajectory + Context + Intervention together for false-positive risk |
| 4 | Orchestrator | **Sequential** | Synthesizes all four outputs into final graduated decision |

Total LLM calls per review: **5** (2 parallel + 3 sequential)
Typical end-to-end latency: **8-15 seconds** via Groq inference

---

## 3. Agent Specifications

### 3.1 Trajectory Agent

**Purpose:** Forecast behavioral health direction and velocity across multi-session windows.

**Input signals extracted:**
- Health score timeline (per-session behavioral health, 0.0-1.0)
- Chat flag accumulation across sessions
- Report and honor totals
- Surrender vote frequency
- Time-of-day distribution shifts
- Champion/agent pool diversity (narrowing = stress indicator)
- KDA trends relative to player baseline

**Output schema:**
```json
{
  "current_health": 0.35,
  "baseline_health": 0.72,
  "predicted_health_3_sessions": 0.22,
  "trajectory_direction": "spiraling",
  "decline_velocity": 0.85,
  "tilt_indicators": ["Rapid KDA decline", "Champion pool narrowed to 2"],
  "confidence": 0.82,
  "reasoning": "Player's health has dropped 51% below baseline..."
}
```

**Calibration rules:**
- "Spiraling" reserved for accelerating decline with no stabilization signs
- Recent sessions weighted more heavily than older ones
- Short histories (<5 sessions) reduce confidence automatically

### 3.2 Context Agent

**Purpose:** Identify what is driving behavioral change. Context determines whether a decline is concerning or perfectly normal.

**Trigger taxonomy:**
- Ranked anxiety / promotion failure
- Temporal patterns (late-night fatigue, weekend vs. weekday)
- Social context (solo vs. duo performance delta)
- Role/champion experimentation (learning curve, not decline)
- External stressors (loss streak cascading across sessions)
- Meta/patch disruption affecting comfort picks

**Output schema:**
```json
{
  "primary_trigger": "Ranked promotion failure",
  "contributing_factors": ["Late-night play migration", "Solo queue without duo"],
  "temporal_pattern": "Decline accelerates after 11 PM sessions",
  "emotional_state_estimate": "Frustration cascading into resignation",
  "trigger_confidence": 0.78,
  "reasoning": "Failed Gold promos triggered tilt spiral..."
}
```

### 3.3 Intervention Agent

**Purpose:** Recommend the minimum effective intervention. The lightest touch that changes the trajectory.

**Intervention taxonomy (graduated):**

| Level | Type | Examples |
|-------|------|----------|
| Passive | No direct contact | Matchmaking adjustment, queue delay suggestion |
| Nudge | Light contact | Cooldown reminder, positive reinforcement message |
| Active | Direct engagement | Proactive outreach, guided self-assessment |
| Restrictive | Behavioral constraint | Monitored play, temporary queue restriction |

**Output schema:**
```json
{
  "recommended_intervention": "Cooldown nudge after 3+ consecutive losses",
  "intervention_type": "NUDGE",
  "urgency": "MEDIUM",
  "specific_actions": ["Display break suggestion", "Show session stats"],
  "expected_effectiveness": 0.65,
  "reasoning": "Pattern shows loss-chasing behavior..."
}
```

### 3.4 Effectiveness Agent

**Purpose:** The system's conscience. Audits every recommendation for false-positive risk and proportionality before the Orchestrator sees it.

**Evaluation dimensions:**
1. **False positive risk** - How likely is an innocent explanation?
2. **Intervention proportionality** - Is the response proportionate to evidence strength?
3. **Harm-if-wrong** - What happens if we intervene on a healthy player?
4. **Historical effectiveness** - Does this intervention type work for this pattern?
5. **Alternative explanations** - At least one must always be generated (intellectual honesty)

**Output schema:**
```json
{
  "false_positive_risk": 0.15,
  "intervention_appropriateness": 0.88,
  "harm_if_wrong": "LOW",
  "historical_success_rate": 0.72,
  "alternative_explanations": ["Could be experimenting with off-role"],
  "reasoning": "Strong evidence supports declining trajectory..."
}
```

**Safety rail:** If false_positive_risk > 0.4, the Orchestrator is blocked from issuing ESCALATE.

### 3.5 Orchestrator Agent

**Purpose:** Synthesize all four agents into a final graduated decision with explainability.

**Decision framework:**

| Decision | Criteria |
|----------|----------|
| NO_ACTION | Stable/recovering trajectory, OR high false-positive risk from Effectiveness |
| NUDGE | Minor drift + low-risk intervention available |
| ADJUST | Environmental/temporal pattern identified + system-level fix available |
| MONITOR | Ambiguous signal, too consistent to ignore, too weak to act on |
| ESCALATE | Spiraling trajectory + low false-positive risk + Effectiveness confirms proportionality |

**Hard-coded safety rules:**
1. ESCALATE blocked when `false_positive_risk > 0.4`
2. ESCALATE blocked when `harm_if_wrong == HIGH` AND `intervention_appropriateness < 0.7`
3. Stable/recovering trajectory defaults to NO_ACTION
4. Orchestrator confidence must be lower than any individual agent's confidence (synthesizing uncertainty)
5. Dissent notes required whenever Effectiveness raised alternative explanations

**Output schema:**
```json
{
  "decision": "MONITOR",
  "severity": "MEDIUM",
  "confidence": 0.71,
  "executive_summary": "Player shows 3-week declining trajectory...",
  "recommended_actions": ["Add to behavioral watch list", "Re-evaluate in 3 sessions"],
  "dissent_notes": "Effectiveness Agent notes possible role experimentation",
  "explainability_trail": [
    "Trajectory Agent detected declining health (0.72 -> 0.45)",
    "Context Agent identified ranked anxiety as primary driver",
    "Intervention Agent recommended monitoring over nudge",
    "Effectiveness Agent flagged 22% false-positive risk",
    "Decision: MONITOR due to sustained pattern with moderate uncertainty"
  ]
}
```

---

## 4. Data Pipeline

### 4.1 Three-Tier Fallback

```
Riot Games API (live)
    |
    +--> Success? --> Live mode (green)
    |
    +--> Fail? --> Check SQLite cache (7-day TTL)
              |
              +--> Hit? --> Cached mode (amber)
              |
              +--> Miss? --> Demo profiles (blue)
```

| Tier | Source | Badge | Behavior |
|------|--------|-------|----------|
| Live | Riot API (Match-V5, Account-V1) | Green | Real match data converted to session trajectories |
| Cached | SQLite with 7-day TTL | Amber | Previously fetched data served from local cache |
| Demo | 8 curated profiles | Blue | Pre-built behavioral trajectories, always available |

### 4.2 Match-to-Session Conversion

Raw Riot API match data is converted to behavioral session records:

```
Match Data (per game):
  - KDA, CS/min, champion played
  - Game duration, outcome
  - Player PUUID for identification

    --> Converted to Session Record:
        - behavioral_health: normalized 0.0-1.0
        - chat_flags, reports, honor
        - time_of_day, champions_played
        - surrender votes, KDA
```

In demo mode, sessions are pre-built with realistic behavioral arcs (8 profiles covering every decision type).

---

## 5. API & Streaming

### 5.1 Server-Sent Events (SSE)

Reviews stream progressively via SSE. The client receives agent results as they complete, enabling real-time UI updates:

```
Event: status    -> { stage: "agents_running" }
Event: agent_result -> { agent: "trajectory", result: {...} }
Event: agent_result -> { agent: "context", result: {...} }
Event: status    -> { stage: "intervention_running" }
Event: agent_result -> { agent: "intervention", result: {...} }
Event: status    -> { stage: "effectiveness_running" }
Event: agent_result -> { agent: "effectiveness", result: {...} }
Event: status    -> { stage: "orchestrator_running" }
Event: agent_result -> { agent: "orchestrator", result: {...} }
Event: complete  -> { full review object }
```

### 5.2 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/review` | POST | Forecast a player (SSE stream) |
| `/api/review-demo/{id}` | POST | Forecast a demo profile (SSE stream) |
| `/api/demo-profiles` | GET | List available demo profiles |
| `/api/data-mode` | GET | Current data source status |
| `/api/history` | GET | Recent review history |
| `/api/review/{id}` | GET | Retrieve a specific review |
| `/health` | GET | Liveness check |

### 5.3 Rate Limiting

IP-based rate limiting: 20 requests per 60-second window per client IP.

---

## 6. Frontend Architecture

### 6.1 Component Tree
```
App
  +-- TopNav (game toggle, data mode badge, navigation)
  +-- PlayerInput (Riot ID form + demo profile grid)
  |     +-- DemoProfileChips (8 trajectory profiles)
  +-- AgentGrid (4 agent cards with live status)
  |     +-- AgentCard x4 (thinking -> done transitions)
  +-- DecisionPanel (orchestrator result + explainability)
  +-- HowItWorks (system architecture explainer)
  +-- AboutModal (project context)
  +-- Footer (disclaimer)
```

### 6.2 State Management

React useState + useCallback hooks. SSE events drive progressive state updates:

- `agentStates` object tracks each agent's status (idle -> thinking -> done)
- Agent results populate cards in real-time as SSE events arrive
- Orchestrator result triggers the DecisionPanel render
- Full review object stored for JSON export/audit download

---

## 7. LLM Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Model | llama-3.3-70b-versatile | Balance of capability and speed on Groq |
| Temperature | 0.1-0.3 | Low temperature for consistent, calibrated outputs |
| Max tokens | 800 | Sufficient for structured JSON responses |
| Response format | JSON object (enforced) | Eliminates parsing failures |
| Retry strategy | 1 automatic retry with lower temperature | Handles occasional JSON malformation |
| Fallback | Graceful degradation with default values | Never crashes; flags errors for manual review |

---

## 8. Production Considerations

This is a concept demo. A production deployment would add:

| Capability | Production Requirement |
|------------|----------------------|
| Model training | Fine-tuned models on historical behavioral trajectories (not general LLM) |
| Data access | Real-time in-game telemetry, chat logs, social graph data |
| Feedback loop | Intervention outcome data as training signal (did the nudge work?) |
| Latency | Sub-second inference for real-time integration |
| Scale | Batch processing for proactive screening of active player populations |
| A/B testing | Randomized controlled trials of intervention types |
| Fairness audit | Bias testing across demographic and playstyle segments |
| Model governance | SR 11-7 aligned model risk management with challenger models |

---

*Independent concept demo built using the public Riot Games API. Not affiliated with, endorsed by, or sponsored by Riot Games.*
