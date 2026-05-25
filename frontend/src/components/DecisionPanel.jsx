import React, { useState } from 'react';

const DECISION_STYLES = {
  NO_ACTION: { border: 'border-emerald-500/30', text: 'text-emerald-400', badge: 'bg-emerald-500', label: 'NO ACTION' },
  NUDGE:     { border: 'border-blue-500/30', text: 'text-blue-400', badge: 'bg-blue-500', label: 'NUDGE' },
  ADJUST:    { border: 'border-amber-500/30', text: 'text-amber-400', badge: 'bg-amber-500', label: 'ADJUST' },
  MONITOR:   { border: 'border-orange-500/30', text: 'text-orange-400', badge: 'bg-orange-500', label: 'MONITOR' },
  ESCALATE:  { border: 'border-val-red/30', text: 'text-val-red', badge: 'bg-val-red', label: 'ESCALATE' },
};

export default function DecisionPanel({ result, fullReview, onReset }) {
  const [showTrail, setShowTrail] = useState(false);
  const [checkedActions, setCheckedActions] = useState({});

  if (!result) return null;
  const style = DECISION_STYLES[result.decision] || DECISION_STYLES.MONITOR;

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(fullReview, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sentinel-forecast-${fullReview?.id || 'export'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <section className="relative py-12 px-6 animate-slide-up">
      <div className="absolute inset-0 grid-dots opacity-10"></div>
      <div className="max-w-4xl mx-auto relative">
        <div className="flex items-center gap-3 mb-8">
          <div className="accent-bar h-6"></div>
          <span className="section-num">05 // INTERVENTION RECOMMENDATION</span>
        </div>

        <div className={`bg-val-card border ${style.border} rounded overflow-hidden`}>
          {/* Red top bar */}
          <div className={`h-1 ${style.badge}`}></div>

          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-4">
                <span className={`${style.badge} text-white px-5 py-2.5 font-extrabold text-lg tracking-wide uppercase cut-corner`}>
                  {style.label}
                </span>
                <div>
                  <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide block">Severity</span>
                  <span className="text-sm font-bold text-white uppercase">{result.severity}</span>
                </div>
              </div>
              <div className="text-right">
                <span className="text-[9px] text-val-dim font-mono uppercase tracking-wide block">Confidence</span>
                <span className="font-mono text-3xl font-bold text-white">
                  {Math.round(result.confidence * 100)}%
                </span>
              </div>
            </div>

            <p className="text-sm text-val-text leading-relaxed mb-6">{result.executive_summary}</p>

            {result.recommended_actions?.length > 0 && (
              <div className="mb-6">
                <h3 className="text-[9px] font-mono font-bold text-val-dim uppercase tracking-widest-xl mb-3">Recommended Actions</h3>
                <div className="space-y-2">
                  {result.recommended_actions.map((action, i) => (
                    <label key={i} className="flex items-center gap-3 cursor-pointer group">
                      <input type="checkbox" checked={!!checkedActions[i]}
                        onChange={() => setCheckedActions(prev => ({ ...prev, [i]: !prev[i] }))}
                        className="w-3.5 h-3.5 rounded-none border-val-border bg-val-dark accent-val-red" />
                      <span className="text-xs text-val-gray group-hover:text-white transition-colors">{action}</span>
                    </label>
                  ))}
                </div>
              </div>
            )}

            {result.dissent_notes && (
              <div className="border-l-2 border-amber-500/50 bg-amber-500/5 p-4 mb-6">
                <h3 className="text-[9px] font-mono font-bold text-amber-400 uppercase tracking-widest-xl mb-2">Dissent Notes</h3>
                <p className="text-xs text-amber-200/70 leading-relaxed">{result.dissent_notes}</p>
              </div>
            )}

            <button onClick={() => setShowTrail(!showTrail)}
              className="text-[9px] text-val-dim font-mono uppercase tracking-wide hover:text-val-gray transition-colors flex items-center gap-1">
              <span className="text-val-red">{showTrail ? '-' : '+'}</span>
              {showTrail ? 'Hide' : 'Show'} Explainability Trail
            </button>

            {showTrail && result.explainability_trail?.length > 0 && (
              <div className="mt-4 space-y-2 pl-4 border-l border-val-border">
                {result.explainability_trail.map((bullet, i) => (
                  <p key={i} className="text-[11px] text-val-gray flex items-start gap-2">
                    <span className="text-val-red font-mono text-[9px] mt-0.5 shrink-0">{String(i + 1).padStart(2, '0')}</span> {bullet}
                  </p>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex gap-3 justify-center mt-8">
          <button onClick={handleDownload}
            className="px-6 py-2.5 bg-val-red hover:bg-val-red-deep text-white font-bold rounded transition-colors text-[11px] uppercase tracking-wide-lg cut-corner">
            Download Audit JSON
          </button>
          <button onClick={onReset}
            className="px-6 py-2.5 border border-val-border hover:border-val-red/50 text-white font-mono rounded transition-colors text-[11px] uppercase tracking-wide">
            Forecast Another
          </button>
        </div>
      </div>
    </section>
  );
}
