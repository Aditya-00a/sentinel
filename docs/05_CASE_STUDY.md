# SENTINEL
## Case Study: Cascade Spiral vs. False Alarm
### How the System Distinguishes Real Spirals from Noise

---

**Purpose:** This case study demonstrates Sentinel's core differentiator — the ability to distinguish genuine behavioral spirals from statistical noise that looks identical on surface metrics. This is the false-positive problem that prevents most proactive moderation systems from shipping.

---

## The False-Positive Problem

Any system that flags declining player metrics will produce enormous numbers of false positives:

- Players learning new champions/agents have declining KDAs
- Players experimenting with off-roles perform worse temporarily
- Players returning after a break have a natural re-adjustment period
- Casual play sessions produce worse stats than tryhard sessions

A naive prediction system that flags all statistical declines would overwhelm behavioral health teams with false alarms and, worse, intervene on players who are doing nothing wrong — destroying trust in the system.

Sentinel solves this with its **Effectiveness Agent**, which audits every recommendation for false-positive risk before the Orchestrator issues a decision.

---

## Profile 1: Cascade Spiral

**Setup:** A Valorant player, Iron 2, 45-day-old account. One AFK game triggered a 72-hour escalation across 10 sessions.

**Session trajectory:**
```
Session 1:  Health 0.70 | Normal play, slightly below average
Session 2:  Health 0.65 | Minor frustration, one chat flag
Session 3:  Health 0.58 | AFK INCIDENT — teammate went AFK, lost patience
Session 4:  Health 0.45 | Tilt response — aggressive play, 2 reports received
Session 5:  Health 0.38 | "Revenge queue" — immediate re-queue while tilted
Session 6:  Health 0.30 | Performance collapse, 3 reports, 2 chat flags
Session 7:  Health 0.25 | Late-night session, surrender spam
Session 8:  Health 0.20 | Abusive chat, multiple flags
Session 9:  Health 0.15 | Intentional feeding detected
Session 10: Health 0.12 | Account at behavioral risk threshold
```

**Key data points:**
- Health dropped from 0.70 to 0.12 (83% decline)
- 8 reports received in final 7 sessions
- Chat flags escalating: passive-aggressive -> hostile -> abusive
- Play pattern shifted to late-night sessions (fatigue amplifier)
- Champion pool collapsed to a single comfort pick

### What the Agents See

**Trajectory Agent:** Detects "spiraling" direction with high decline velocity (~0.85). Predicts health will reach 0.05-0.10 in 3 more sessions. High confidence (0.80+).

**Context Agent:** Identifies the AFK incident in Session 3 as the cascade trigger. Contributing factors include late-night migration, loss-chasing behavior, and no social support (solo queue only). Emotional state: frustration cascading into hopelessness.

**Intervention Agent:** Recommends proactive outreach (not just a nudge). This is beyond a cooldown suggestion — the spiral has momentum. Urgency: HIGH.

**Effectiveness Agent:** Confirms LOW false-positive risk. The pattern is unambiguous — consistent decline across 10 sessions with escalating severity markers. Historical success rate for proactive outreach at this stage: moderate (some players are reachable, some are past the intervention window).

**Orchestrator Decision: ESCALATE**
- Severity: CRITICAL
- Confidence: 0.80+
- Explainability: Clear cascade trigger, sustained decline, no alternative explanations, Effectiveness confirms proportionality

---

## Profile 2: False Alarm

**Setup:** A League of Legends player, Gold 2, 800-day veteran account. Stats look like decline. Actually learning a new role.

**Session trajectory:**
```
Session 1:  Health 0.72 | Normal — main role, comfort champions
Session 2:  Health 0.75 | Normal — strong performance
Session 3:  Health 0.68 | Slightly worse — started playing new role
Session 4:  Health 0.55 | Notable drop — new role, unfamiliar matchups
Session 5:  Health 0.48 | Continued struggle — learning curve
Session 6:  Health 0.52 | Slight recovery — improving at new role
Session 7:  Health 0.50 | Stabilized — no longer declining
Session 8:  Health 0.55 | Upward tick — new role becoming comfortable
```

**Key data points:**
- Health dropped from 0.75 to 0.48 (36% decline) before stabilizing
- 0 reports received across all sessions
- 0 chat flags
- Champion pool EXPANDED (not narrowed — opposite of tilt)
- Honor received consistently (teammates aren't reporting problems)
- No time-of-day shift (playing normal hours)
- KDA lower, but death patterns are "learning deaths" not "tilt deaths"

### What the Agents See

**Trajectory Agent:** May detect "declining" direction based on health scores alone. The numbers genuinely look like a decline. Moderate confidence.

**Context Agent:** THIS IS THE KEY — identifies champion pool expansion and role swap as the primary factor. No social conflict indicators. No temporal disruption. The "decline" is localized to mechanical performance in an unfamiliar role.

**Intervention Agent:** May suggest a light nudge or no action, recognizing the low severity.

**Effectiveness Agent:** FLAGS HIGH FALSE-POSITIVE RISK (0.70+). Alternative explanations are strong:
- Player is voluntarily expanding their champion pool
- Zero social friction indicators (no reports, no chat flags, honor maintained)
- Health is stabilizing and beginning to recover
- Champion diversity increasing = growth, not stress

**Orchestrator Decision: NO_ACTION**
- Severity: NONE
- Confidence: 0.75+
- Explainability: "While health metrics show a 36% decline, the Effectiveness Agent identified champion pool expansion and zero social friction markers as strong evidence of voluntary skill development rather than behavioral decline. No intervention warranted."
- Dissent: "Trajectory Agent flagged declining health. Overridden by Effectiveness assessment of high false-positive risk."

---

## The Comparison

| Dimension | Cascade Spiral | False Alarm |
|-----------|---------------|-------------|
| Health decline | 83% (0.70 -> 0.12) | 36% (0.75 -> 0.48) |
| Reports received | 8 | 0 |
| Chat flags | Escalating | None |
| Champion pool | Narrowing (stress) | Expanding (growth) |
| Time-of-day shift | Yes (late-night) | No |
| Honor received | Declining | Consistent |
| Trajectory after decline | Accelerating downward | Stabilizing + recovering |
| **Sentinel decision** | **ESCALATE** | **NO_ACTION** |

A naive system looking only at health score trends might flag both players. Sentinel's multi-agent architecture — specifically the Context Agent identifying behavioral drivers and the Effectiveness Agent auditing false-positive risk — produces the correct opposite conclusions.

---

## Why This Matters

The false-positive problem is why most proactive moderation systems don't ship. The cost of wrongly intervening on a healthy player (damaged trust, player frustration, support ticket volume) is high enough that teams default to reactive approaches despite knowing that earlier intervention would be more effective.

Sentinel's architecture addresses this by:

1. **Separating trajectory analysis from context analysis** — the numbers can decline while the behavior is healthy
2. **Making false-positive auditing a first-class agent** — not a post-hoc check, but a required pipeline stage
3. **Hard-coding safety rails** — ESCALATE is literally blocked when false-positive risk exceeds the threshold
4. **Requiring alternative explanations** — the Effectiveness Agent must always generate at least one innocent explanation, even for clear cases

This is the difference between a prediction system that's technically accurate and one that's operationally deployable.

---

*Independent concept demo built using the public Riot Games API. Not affiliated with, endorsed by, or sponsored by Riot Games.*
