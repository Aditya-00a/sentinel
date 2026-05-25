import React from 'react';

export default function HowItWorks({ onBack }) {
  return (
    <div className="relative min-h-screen py-12 px-6">
      <div className="absolute inset-0 grid-dots opacity-15"></div>
      <div className="absolute top-8 right-8 text-val-border text-xl font-mono select-none hidden lg:block">+</div>
      <div className="absolute bottom-12 left-12 text-val-border text-xl font-mono select-none hidden lg:block">+</div>

      <div className="max-w-3xl mx-auto relative">
        <button onClick={onBack} className="text-val-dim hover:text-white text-[10px] font-mono uppercase tracking-widest-xl mb-10 flex items-center gap-2 transition-colors">
          <span className="text-val-red">&lt;-</span> Back
        </button>

        <div className="section-num mb-4">// SYSTEM ARCHITECTURE</div>
        <h1 className="text-4xl font-extrabold text-white mb-2 uppercase tracking-tight">How Sentinel</h1>
        <h1 className="text-4xl font-extrabold text-val-red mb-10 uppercase tracking-tight">Works</h1>

        <section className="mb-14">
          <div className="flex items-center gap-3 mb-4">
            <div className="accent-bar h-5"></div>
            <span className="section-num">01 // The Problem</span>
          </div>
          <p className="text-sm text-val-gray leading-relaxed">
            Current moderation systems are reactive — they wait for a report, review it, and punish.
            This works for catching bad actors, but it fails at the deeper problem: players don't feel safer
            despite more bans than ever. The issue isn't detection — it's that intervention happens too late.
            By the time a report is filed, the damage to the community is already done. What if we could
            predict behavioral spirals and intervene before they happen?
          </p>
        </section>

        <section className="mb-14">
          <div className="flex items-center gap-3 mb-4">
            <div className="accent-bar h-5"></div>
            <span className="section-num">02 // The Approach</span>
          </div>
          <h2 className="text-lg font-bold text-white mb-4 uppercase tracking-wide">Public Health, Not Policing</h2>
          <p className="text-sm text-val-gray leading-relaxed mb-8">
            Sentinel treats player behavior as a public health problem, not a criminal justice one.
            Instead of asking "did this player break a rule?" it asks "is this player on a trajectory
            toward breaking a rule, and what's the minimum intervention that can change their course?"
          </p>
          <div className="bg-val-card border border-val-border rounded overflow-hidden">
            <div className="h-0.5 bg-val-red"></div>
            <pre className="p-6 font-mono text-[10px] text-val-dim leading-relaxed whitespace-pre-wrap">{`  Player Session History (multi-session trajectory data)
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
              +------------------+`}</pre>
          </div>
        </section>

        <section className="mb-14">
          <div className="flex items-center gap-3 mb-6">
            <div className="accent-bar h-5"></div>
            <span className="section-num">03 // The Agents</span>
          </div>
          <div className="space-y-3">
            {[
              { num: '01', title: 'Trajectory Agent', desc: 'Analyzes behavioral health scores across multiple sessions to detect trends. Is the player stable, declining, recovering, or spiraling? How fast? Where will they be in 3 more sessions?' },
              { num: '02', title: 'Context Agent', desc: 'Identifies what\'s driving the behavioral change. Failed promos? Late-night fatigue? Solo queue without their duo partner? Context determines whether a decline is concerning or perfectly normal.' },
              { num: '03', title: 'Intervention Agent', desc: 'Recommends the minimum effective intervention. A cooldown suggestion for a loss streak. Matchmaking adjustments for time-of-day patterns. Proactive outreach only for severe spirals.' },
              { num: '04', title: 'Effectiveness Agent', desc: 'The system\'s conscience. Evaluates false-positive risk, intervention proportionality, and what happens if we\'re wrong. Explicitly penalizes overreaction.' },
              { num: '05', title: 'Orchestrator', desc: 'Synthesizes all four outputs into a final recommendation: NO_ACTION, NUDGE, ADJUST, MONITOR, or ESCALATE. Produces a plain-English explainability trail.' },
            ].map((agent) => (
              <div key={agent.title} className="bg-val-card border border-val-border rounded overflow-hidden">
                <div className="h-0.5 bg-val-border"></div>
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-val-red font-mono text-[10px] font-bold">{agent.num}</span>
                    <span className="text-val-border font-mono text-[10px]">//</span>
                    <h3 className="text-xs font-bold text-white uppercase tracking-wide">{agent.title}</h3>
                  </div>
                  <p className="text-[11px] text-val-gray leading-relaxed">{agent.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-14">
          <div className="flex items-center gap-3 mb-6">
            <div className="accent-bar h-5"></div>
            <span className="section-num">04 // Why This Is Different</span>
          </div>
          <div className="space-y-4">
            {[
              ['Reactive', 'Proactive', 'Current systems wait for reports. Sentinel forecasts before reports happen.'],
              ['Punishment', 'Intervention', 'Instead of "what punishment fits?" it asks "what intervention prevents?"'],
              ['Binary', 'Graduated', 'Five response levels from NO_ACTION to ESCALATE, not just "ban or don\'t ban."'],
              ['Opaque', 'Explainable', 'Every recommendation comes with a plain-English audit trail.'],
              ['Confident', 'Calibrated', 'The Effectiveness Agent explicitly penalizes overconfident escalation.'],
            ].map(([from, to, desc]) => (
              <div key={from} className="flex gap-4 items-start">
                <div className="shrink-0 w-44 text-right">
                  <span className="text-val-dim text-xs font-mono line-through">{from}</span>
                  <span className="text-val-red text-xs font-bold ml-2">{to}</span>
                </div>
                <span className="text-[11px] text-val-gray leading-relaxed">{desc}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-14">
          <div className="flex items-center gap-3 mb-4">
            <div className="accent-bar h-5"></div>
            <span className="section-num">05 // Limitations</span>
          </div>
          <p className="text-sm text-val-gray leading-relaxed">
            This is a concept demo. A production system would use fine-tuned models trained on historical
            behavioral trajectories, have access to actual in-game telemetry and chat logs, incorporate
            intervention outcome data as feedback signals, and operate at sub-second latency. The demo
            illustrates the architecture — that prediction-first, intervention-oriented thinking with
            built-in effectiveness auditing is a fundamentally different approach to community health
            than the reactive detect-and-punish paradigm.
          </p>
        </section>
      </div>
    </div>
  );
}
