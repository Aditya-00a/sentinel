import React from 'react';
import DataModeBadge from './DataModeBadge';

export default function TopNav({ game, onGameChange, dataMode, currentView, onViewChange }) {
  return (
    <nav className="h-14 bg-val-dark/95 backdrop-blur-sm border-b border-val-border flex items-center px-6 sticky top-0 z-50">
      <div className="flex items-center gap-3 mr-auto">
        <div className="flex items-center gap-2">
          <span className="text-val-red font-mono text-xs tracking-widest-xl">//</span>
          <span className="text-base font-extrabold tracking-wide text-white uppercase">
            SENTINEL
          </span>
        </div>
        <span className="hidden sm:inline text-[10px] font-mono tracking-wide-lg text-val-dim uppercase">
          pre-escalation intelligence
        </span>
      </div>

      <div className="flex items-center gap-0.5 bg-val-card rounded p-0.5 border border-val-border mr-6">
        <button
          onClick={() => onGameChange('lol')}
          className={`px-4 py-1.5 rounded text-[11px] font-bold uppercase tracking-wide-lg transition-all ${
            game === 'lol'
              ? 'bg-val-red text-white'
              : 'text-val-dim hover:text-white'
          }`}
        >
          LoL
        </button>
        <button
          onClick={() => onGameChange('valorant')}
          className={`px-4 py-1.5 rounded text-[11px] font-bold uppercase tracking-wide-lg transition-all ${
            game === 'valorant'
              ? 'bg-val-red text-white'
              : 'text-val-dim hover:text-white'
          }`}
        >
          Valorant
        </button>
      </div>

      <div className="flex items-center gap-4">
        <DataModeBadge mode={dataMode} />
        {['demo', 'how-it-works', 'about'].map(view => (
          <button
            key={view}
            onClick={() => onViewChange(view)}
            className={`text-[11px] font-mono uppercase tracking-wide-lg transition-colors ${
              currentView === view ? 'text-val-red' : 'text-val-dim hover:text-white'
            }`}
          >
            {view === 'demo' ? 'Demo' : view === 'how-it-works' ? 'System' : 'About'}
          </button>
        ))}
      </div>
    </nav>
  );
}
