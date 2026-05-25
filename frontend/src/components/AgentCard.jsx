import React, { useState } from 'react';

function ScoreBar({ label, value, color = 'bg-val-red', reverse = false }) {
  const pct = Math.round(value * 100);
  const barColor = reverse
    ? (value > 0.6 ? 'bg-emerald-500' : value > 0.3 ? 'bg-amber-500' : 'bg-val-red')
    : (value > 0.7 ? 'bg-val-red' : value > 0.4 ? 'bg-amber-500' : 'bg-emerald-500');
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="text-val-dim w-32 text-right shrink-0 text-[10px] font-mono uppercase tracking-wide">{label}</span>
      <div className="flex-1 h-1.5 bg-val-dark rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-700 ${color || barColor}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="font-mono text-val-gray w-10 text-right text-[11px]">{pct}%</span>
    </div>
  );
}

function HealthGauge({ value, label, predicted }) {
  const pct = Math.round(value * 100);
  const predPct = predicted !== undefined ? Math.round(predicted * 100) : null;
  const color = value > 0.7 ? '#10B981' : value > 0.4 ? '#F59E0B' : '#FF4655';
  const predColor = predicted > 0.7 ? '#10B981' : predicted > 0.4 ? '#F59E0B' : '#FF4655';
  const size = 64;
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value * circumference);

  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative">
        <svg width={size} height={size} className="transform -rotate-90">
          <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="#1F2937" strokeWidth="3" />
          <circle cx={size/2} cy={size/2} r={radius} fill="none"
            stroke={color} strokeWidth="3" strokeLinecap="round"
            strokeDasharray={circumference} strokeDashoffset={offset}
            className="transition-all duration-1000" />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center font-mono text-xs text-white font-bold">{pct}%</span>
      </div>
      <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide">{label}</span>
      {predPct !== null && (
        <span className="text-[9px] font-mono font-bold" style={{ color: predColor }}>
          {predPct > pct ? '+' : ''}{predPct - pct}% predicted
        </span>
      )}
    </div>
  );
}

function DirectionBadge({ direction }) {
  const styles = {
    stable: 'text-emerald-400 border-emerald-500/30',
    declining: 'text-amber-400 border-amber-500/30',
    recovering: 'text-blue-400 border-blue-500/30',
    spiraling: 'text-val-red border-val-red/30',
  };
  const arrows = { stable: '~', declining: '\\', recovering: '/', spiraling: '!!' };
  return (
    <span className={`px-2 py-0.5 border rounded text-[9px] font-mono font-bold uppercase tracking-wide ${styles[direction] || styles.stable}`}>
      {arrows[direction] || '~'} {direction}
    </span>
  );
}

function UrgencyBadge({ urgency }) {
  const styles = {
    LOW: 'text-val-dim border-val-border',
    MEDIUM: 'text-amber-400 border-amber-500/30',
    HIGH: 'text-orange-400 border-orange-500/30',
    CRITICAL: 'text-val-red border-val-red/30',
  };
  return (
    <span className={`px-2 py-0.5 border rounded text-[9px] font-mono font-bold tracking-wide ${styles[urgency] || styles.LOW}`}>
      {urgency}
    </span>
  );
}

function Pills({ items, color = 'border-val-border' }) {
  if (!items?.length) return null;
  return (
    <div className="flex flex-wrap gap-1 mt-2">
      {items.map((item, i) => (
        <span key={i} className={`px-2 py-0.5 text-[9px] font-mono border ${color} text-val-dim bg-val-dark rounded`}>{item}</span>
      ))}
    </div>
  );
}

export default function AgentCard({ name, num, status, result }) {
  const [showJson, setShowJson] = useState(false);
  const isThinking = status === 'thinking';
  const isDone = status === 'done';

  const agentConfig = {
    trajectory:     { title: 'Trajectory Agent',     subtitle: 'behavioral health forecasting' },
    context:        { title: 'Context Agent',        subtitle: 'trigger & pattern identification' },
    intervention:   { title: 'Intervention Agent',   subtitle: 'proactive recommendation' },
    effectiveness:  { title: 'Effectiveness Agent',  subtitle: 'risk & proportionality audit' },
  };
  const config = agentConfig[name] || { title: name, subtitle: '' };

  return (
    <div className={`relative bg-val-card border border-val-border rounded overflow-hidden transition-all ${
      isThinking ? 'animate-pulse-red' : ''} ${isDone ? 'animate-fade-in' : ''}`}>
      {/* Red top accent line */}
      <div className={`h-0.5 ${isDone ? 'bg-val-red' : isThinking ? 'bg-amber-500' : 'bg-val-border'} transition-colors`}></div>

      <div className="p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-val-red font-mono text-[10px] font-bold">{num}</span>
            <span className="text-val-border font-mono text-[10px]">//</span>
            <span className="text-xs font-bold text-white uppercase tracking-wide">{config.title}</span>
          </div>
          <span className={`px-2 py-0.5 rounded text-[9px] font-mono font-bold tracking-wide ${
            isDone ? 'text-emerald-400 border border-emerald-500/30' : isThinking ? 'text-amber-400 border border-amber-500/30' : 'text-val-dim border border-val-border'}`}>
            {isDone ? 'DONE' : isThinking ? 'RUNNING' : 'IDLE'}
          </span>
        </div>
        <p className="text-[9px] font-mono text-val-dim uppercase tracking-wide mb-3">{config.subtitle}</p>

        {isThinking && (
          <div className="flex items-center justify-center h-24">
            <div className="flex gap-1.5">
              {[0, 1, 2].map(i => (
                <div key={i} className="w-1.5 h-1.5 bg-val-red animate-bounce" style={{ animationDelay: `${i * 150}ms` }} />
              ))}
            </div>
          </div>
        )}

        {isDone && result && (
          <div className="space-y-3">
            {name === 'trajectory' && (
              <>
                <div className="flex justify-around">
                  <HealthGauge value={result.current_health} label="Current" predicted={result.predicted_health_3_sessions} />
                  <HealthGauge value={result.baseline_health} label="Baseline" />
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-[9px] text-val-dim font-mono">DIR:</span>
                  <DirectionBadge direction={result.trajectory_direction} />
                  <span className="text-[9px] text-val-dim font-mono ml-auto">CONF:</span>
                  <span className="font-mono text-[11px] text-white font-bold">{Math.round(result.confidence * 100)}%</span>
                </div>
                {result.decline_velocity > 0 && (
                  <ScoreBar label="Decline vel." value={result.decline_velocity} />
                )}
                <Pills items={result.tilt_indicators} />
              </>
            )}

            {name === 'context' && (
              <>
                <div className="bg-val-dark border-l-2 border-val-red p-3">
                  <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide block mb-1">Primary Trigger</span>
                  <span className="text-sm text-white font-bold">{result.primary_trigger}</span>
                </div>
                {result.temporal_pattern && (
                  <div className="bg-val-dark border-l-2 border-val-border p-3">
                    <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide block mb-1">Temporal Pattern</span>
                    <span className="text-xs text-val-gray">{result.temporal_pattern}</span>
                  </div>
                )}
                {result.emotional_state_estimate && (
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-[9px] text-val-dim font-mono">EMOTIONAL STATE:</span>
                    <span className="text-xs text-amber-400 font-bold">{result.emotional_state_estimate}</span>
                  </div>
                )}
                <div className="flex items-center gap-2">
                  <span className="text-[9px] text-val-dim font-mono">TRIGGER CONF:</span>
                  <span className="font-mono text-[11px] text-white font-bold">{Math.round(result.trigger_confidence * 100)}%</span>
                </div>
                <Pills items={result.contributing_factors} color="border-amber-500/20" />
              </>
            )}

            {name === 'intervention' && (
              <>
                <div className="bg-val-dark border-l-2 border-val-red p-3 flex items-center justify-between">
                  <div>
                    <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide block mb-1">Recommended</span>
                    <span className="text-sm text-white font-bold uppercase">{result.intervention_type?.replace(/_/g, ' ')}</span>
                  </div>
                  <UrgencyBadge urgency={result.urgency} />
                </div>
                <ScoreBar label="Effectiveness" value={result.expected_effectiveness} color="bg-blue-500" />
                <Pills items={result.specific_actions} color="border-blue-500/20" />
              </>
            )}

            {name === 'effectiveness' && (
              <>
                <ScoreBar label="False pos. risk" value={result.false_positive_risk} />
                <ScoreBar label="Appropriateness" value={result.intervention_appropriateness} color="bg-emerald-500" />
                <ScoreBar label="Hist. success" value={result.historical_success_rate} color="bg-blue-500" />
                <div className="flex items-center gap-2 mt-2">
                  <span className="text-[9px] text-val-dim font-mono">HARM IF WRONG:</span>
                  <span className={`text-[11px] font-mono font-bold ${
                    result.harm_if_wrong === 'LOW' ? 'text-emerald-400' :
                    result.harm_if_wrong === 'MEDIUM' ? 'text-amber-400' : 'text-val-red'
                  }`}>{result.harm_if_wrong}</span>
                </div>
                <Pills items={result.alternative_explanations} color="border-amber-500/20" />
              </>
            )}

            <p className="text-[11px] text-val-gray mt-2 leading-relaxed">{result.reasoning}</p>

            <button onClick={() => setShowJson(!showJson)}
              className="text-[9px] text-val-dim font-mono uppercase tracking-wide hover:text-val-gray transition-colors mt-1">
              {showJson ? '[ - ] Hide JSON' : '[ + ] Raw JSON'}
            </button>
            {showJson && (
              <pre className="mt-2 p-3 bg-val-dark border border-val-border rounded text-[9px] font-mono text-val-dim overflow-x-auto max-h-48 overflow-y-auto">
                {JSON.stringify(result, null, 2)}
              </pre>
            )}
          </div>
        )}

        {!isThinking && !isDone && (
          <div className="h-24 flex items-center justify-center">
            <span className="text-val-dim text-[10px] font-mono uppercase tracking-wide">Awaiting forecast</span>
          </div>
        )}
      </div>
    </div>
  );
}
