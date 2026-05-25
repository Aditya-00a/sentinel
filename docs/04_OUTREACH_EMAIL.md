# Outreach Email Drafts
## For Riot Games Trust & Safety / Player Dynamics Team

---

### VERSION A: Direct to Hiring Manager / T&S Lead

**Subject:** Built a pre-escalation behavioral intelligence prototype for Riot — would love your feedback

Hi [Name],

I'm Aditya Sakhale, an MS student at NYU Stern (Management & Analytics, 2026) and the Trust & Safety Lab coordinator at NYU. I built something I think your team would find interesting.

Sentinel is a working prototype of a pre-escalation intelligence system for player behavior. Instead of reviewing reports after the fact, it uses a five-agent AI pipeline to forecast behavioral spirals across multi-session trajectories and recommend graduated interventions — treating community health like public health rather than policing.

The key idea: the system has a built-in Effectiveness Agent that audits every recommendation for false-positive risk before the final decision is made. It explicitly penalizes overreaction. A player learning a new role looks like a player in decline on the numbers, but the system catches the difference.

Here's a 30-second demo path:
1. [Live demo URL]
2. Click "Cascade Spiral" (ESCALATE case) to see the full pipeline
3. Then click "False Alarm" (NO_ACTION case) — same declining stats, opposite conclusion

I built this using the public Riot API, Groq for inference, and React/FastAPI. The architecture doc and source are attached/linked.

I'd love to get 15 minutes of your time to hear what resonates and what doesn't. I'm specifically interested in where this kind of prediction-first thinking fits (or doesn't fit) in Riot's existing moderation infrastructure.

Best,
Aditya Sakhale
MS Management & Analytics, NYU Stern 2026
Trust & Safety Lab Coordinator, NYU
as18513@nyu.edu | linkedin.com/in/adityasakhale

---

### VERSION B: Warm Intro / Referral Request

**Subject:** Quick ask — know anyone on Riot's Trust & Safety team?

Hi [Name],

Hope you're doing well! I wanted to reach out because I just finished building a project that sits right at the intersection of AI and player safety, and I'm trying to get it in front of the right people at Riot Games.

It's called Sentinel — a pre-escalation behavioral intelligence system. Five AI agents analyze player trajectories across sessions and recommend graduated interventions (from "do nothing" to "flag for human review"), with a built-in false-positive auditor that prevents the system from overreacting. The whole thing is live with a working demo.

I'm specifically looking to connect with someone on Riot's Trust & Safety, Player Dynamics, or Social Systems team. If anyone comes to mind, I'd really appreciate an intro — even a "you should check this out" forward would mean a lot.

Happy to send you the demo link or a one-pager if you want to see what I built first.

Thanks!
Aditya

---

### VERSION C: LinkedIn Connection Request Note (300 char limit)

Hi [Name] — I'm an NYU Stern MS student who built a pre-escalation behavioral intelligence prototype for player safety using Riot's API. Would love to share it and hear your perspective on prediction-first moderation. Happy to send a demo link!

---

### VERSION D: Follow-Up Email (if no response after 5-7 days)

**Subject:** Re: Built a pre-escalation behavioral intelligence prototype for Riot — would love your feedback

Hi [Name],

Just bumping this in case it got buried. I know T&S teams are always slammed.

The quick pitch: I built a working prototype that forecasts player behavioral spirals before they become reportable incidents, using five specialized AI agents with a built-in false-positive auditor. The demo takes 30 seconds to evaluate.

[Demo URL] — click "Cascade Spiral" then "False Alarm" to see the system reach opposite conclusions on similar-looking data.

If this isn't your area, I'd also appreciate being pointed to the right person.

Best,
Aditya

---

## Target Roles at Riot Games

| Priority | Title / Team | Why |
|----------|-------------|-----|
| 1 | Trust & Safety Lead / Manager | Direct decision-maker for behavioral systems |
| 2 | Player Dynamics team | Research-oriented, would appreciate the architecture |
| 3 | Social Systems & Anti-Cheat Engineering | Technical counterparts who build these systems |
| 4 | Data Science - Player Behavior | Would evaluate the modeling approach |
| 5 | Central Game Design (behavioral systems) | Cross-game behavioral design |

## Key People to Research

Search LinkedIn for:
- "Trust and Safety" + "Riot Games"
- "Player Dynamics" + "Riot Games"
- "Social Systems" + "Riot Games"
- "Anti-Cheat" OR "Player Behavior" + "Riot Games"
- "Community Health" + "Riot Games"

---

## Talking Points (for calls / interviews)

### Why prediction over detection?
"Detection has gotten very good. The problem is that by the time you detect and punish, the damage to community health is already done. The teammate already tilted, the lobby already collapsed. Prediction creates an intervention window that doesn't exist in reactive systems."

### Why minimum effective dose?
"The biggest risk in proactive moderation isn't missing a toxic player — it's false-positiving an innocent one. A wrong intervention on a healthy player damages trust more than a missed opportunity to intervene. That's why the Effectiveness Agent exists — it's the system's conscience."

### Why five agents instead of one?
"Separation of concerns. The Trajectory Agent shouldn't decide interventions. The Intervention Agent shouldn't audit its own recommendations. And the Effectiveness Agent's sole purpose is to find reasons NOT to escalate. You need adversarial structure for calibrated decisions."

### How does this complement existing systems?
"This sits upstream of existing moderation. It doesn't replace the reporting pipeline or the tribunal — it creates an early warning layer that flags trajectories before they reach the reporting threshold. Think of it as the triage nurse before the ER."

### What would production look like?
"Fine-tuned models instead of general LLMs. Real-time telemetry instead of API polling. Intervention outcome data feeding back as training signal. A/B testing intervention types. And proper fairness auditing across player segments."

---

## Attachments to Include

1. **01_EXECUTIVE_BRIEF.md** (or PDF conversion) — The one-pager
2. **02_TECHNICAL_ARCHITECTURE.md** (or PDF) — For technical evaluators
3. **Demo link** — Always include the live URL
4. **GitHub link** — Source code for credibility
5. **Resume** — Standard attachment

Do NOT attach the demo walkthrough guide unless specifically asked for a longer read — keep the initial email lean.
