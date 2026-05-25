import React from 'react';

const MODE_CONFIG = {
  live: { color: 'text-emerald-400', border: 'border-emerald-500/20', dot: 'bg-emerald-400', label: 'LIVE' },
  cached: { color: 'text-amber-400', border: 'border-amber-500/20', dot: 'bg-amber-400', label: 'CACHED' },
  demo: { color: 'text-blue-400', border: 'border-blue-500/20', dot: 'bg-blue-400', label: 'DEMO' },
};

export default function DataModeBadge({ mode }) {
  const config = MODE_CONFIG[mode] || MODE_CONFIG.demo;
  return (
    <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded border ${config.border} bg-val-card`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`}></span>
      <span className={`text-[9px] font-mono font-bold tracking-widest-xl ${config.color}`}>{config.label}</span>
    </div>
  );
}
