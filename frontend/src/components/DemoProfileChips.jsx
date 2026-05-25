import React from 'react';

const DECISION_META = {
  NO_ACTION: { color: 'border-emerald-500', bg: 'bg-emerald-500', text: 'text-emerald-400', label: 'NO ACTION' },
  NUDGE:     { color: 'border-blue-500',    bg: 'bg-blue-500',    text: 'text-blue-400',    label: 'NUDGE' },
  ADJUST:    { color: 'border-amber-500',   bg: 'bg-amber-500',   text: 'text-amber-400',   label: 'ADJUST' },
  MONITOR:   { color: 'border-orange-500',  bg: 'bg-orange-500',  text: 'text-orange-400',  label: 'MONITOR' },
  ESCALATE:  { color: 'border-val-red',     bg: 'bg-val-red',     text: 'text-val-red',     label: 'ESCALATE' },
};

export default function DemoProfileChips({ profiles, onSelect, isLoading, currentGame }) {
  const filtered = profiles.filter(p => p.game === currentGame);
  const otherGame = profiles.filter(p => p.game !== currentGame);
  const all = [...filtered, ...otherGame];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-2xl mx-auto">
      {all.map((p, i) => {
        const meta = DECISION_META[p.expected_decision] || DECISION_META.MONITOR;
        const isOther = p.game !== currentGame;

        return (
          <button
            key={p.id}
            onClick={() => onSelect(p.id)}
            disabled={isLoading}
            className={`group relative flex items-stretch text-left bg-val-card border border-val-border rounded overflow-hidden
              hover:border-val-red/50 transition-all disabled:opacity-30 disabled:cursor-not-allowed
              ${isOther ? 'opacity-50 hover:opacity-100' : ''}`}
          >
            {/* Left accent bar */}
            <div className={`w-0.5 shrink-0 ${meta.bg} transition-all group-hover:w-1`}></div>

            <div className="flex items-center gap-3 px-3 py-2.5 flex-1 min-w-0">
              {/* Number */}
              <span className="text-[9px] font-mono text-val-dim shrink-0 w-4 text-right">
                {String(i + 1).padStart(2, '0')}
              </span>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold text-white group-hover:text-val-red transition-colors uppercase tracking-wide truncate">
                    {p.name}
                  </span>
                  {isOther && (
                    <span className="text-[8px] font-mono text-val-dim border border-val-border px-1 py-px shrink-0 uppercase">
                      {p.game === 'valorant' ? 'VAL' : 'LOL'}
                    </span>
                  )}
                </div>
                <div className="text-[9px] text-val-dim font-mono truncate">{p.description}</div>
              </div>

              {/* Expected decision badge */}
              <span className={`text-[7px] font-mono font-bold ${meta.text} shrink-0 tracking-widest uppercase`}>
                {meta.label}
              </span>
            </div>
          </button>
        );
      })}
    </div>
  );
}
