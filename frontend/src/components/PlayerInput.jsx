import React, { useState } from 'react';
import DemoProfileChips from './DemoProfileChips';

const REGIONS = [
  { value: 'americas', label: 'Americas', platforms: ['na1', 'br1', 'la1', 'la2', 'oc1'] },
  { value: 'europe', label: 'Europe', platforms: ['euw1', 'eun1', 'tr1', 'ru'] },
  { value: 'asia', label: 'Asia', platforms: ['kr', 'jp1'] },
];

export default function PlayerInput({ onReview, onDemoReview, isLoading, demoProfiles }) {
  const [riotId, setRiotId] = useState('');
  const [region, setRegion] = useState('americas');
  const [platform, setPlatform] = useState('na1');

  const currentRegion = REGIONS.find(r => r.value === region);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!riotId.includes('#')) return;
    onReview({ game: 'lol', riot_id: riotId, region, platform });
  };

  return (
    <section className="relative py-20 px-6 overflow-hidden">
      {/* Grid dots background */}
      <div className="absolute inset-0 grid-dots opacity-30"></div>

      {/* Decorative crosshairs */}
      <div className="absolute top-12 left-12 text-val-border text-2xl font-mono select-none hidden lg:block">+</div>
      <div className="absolute bottom-16 right-16 text-val-border text-2xl font-mono select-none hidden lg:block">+</div>
      <div className="absolute top-24 right-32 text-val-border text-lg font-mono select-none hidden lg:block opacity-50">x</div>
      <div className="absolute bottom-32 left-28 text-val-border text-lg font-mono select-none hidden lg:block opacity-50">x</div>

      {/* Red accent square */}
      <div className="absolute top-16 left-6 w-2 h-2 bg-val-red hidden lg:block"></div>

      <div className="max-w-3xl mx-auto text-center relative">
        {/* Section number */}
        <div className="section-num mb-6">00 // BEHAVIORAL FORECAST</div>

        <h1 className="text-5xl sm:text-6xl font-extrabold text-white mb-2 uppercase leading-none tracking-tight">
          Forecast the
        </h1>
        <h1 className="text-5xl sm:text-6xl font-extrabold text-val-red mb-6 uppercase leading-none tracking-tight">
          Spiral
        </h1>
        <p className="text-val-gray text-sm mb-12 max-w-xl mx-auto leading-relaxed">
          Four agents forecast player behavioral trajectories and recommend
          the minimum effective intervention before reports happen.
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2 max-w-2xl mx-auto mb-6">
          <input type="text" value={riotId} onChange={(e) => setRiotId(e.target.value)}
            placeholder="Riot ID (e.g. Player#NA1)"
            className="flex-1 px-4 py-3 bg-val-card border border-val-border rounded text-white placeholder:text-val-dim focus:outline-none focus:border-val-red transition-colors font-mono text-sm"
            disabled={isLoading} />
          <select value={region} onChange={(e) => { setRegion(e.target.value); const nr = REGIONS.find(r => r.value === e.target.value); if (nr) setPlatform(nr.platforms[0]); }}
            className="px-4 py-3 bg-val-card border border-val-border rounded text-white text-xs font-mono uppercase focus:outline-none focus:border-val-red cursor-pointer" disabled={isLoading}>
            {REGIONS.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
          <select value={platform} onChange={(e) => setPlatform(e.target.value)}
            className="px-4 py-3 bg-val-card border border-val-border rounded text-white text-xs font-mono uppercase focus:outline-none focus:border-val-red cursor-pointer" disabled={isLoading}>
            {currentRegion?.platforms.map(p => <option key={p} value={p}>{p.toUpperCase()}</option>)}
          </select>
          <button type="submit" disabled={isLoading || !riotId.includes('#')}
            className="px-6 py-3 bg-val-red hover:bg-val-red-deep text-white font-bold rounded transition-all disabled:opacity-30 disabled:cursor-not-allowed whitespace-nowrap uppercase text-xs tracking-wide-lg cut-corner">
            {isLoading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Forecasting
              </span>
            ) : 'Forecast'}
          </button>
        </form>

        <div className="mt-14">
          <div className="flex items-center justify-center gap-3 mb-5">
            <div className="h-px w-8 bg-val-border"></div>
            <p className="text-val-dim text-[9px] font-mono uppercase tracking-widest-xl">Or select a trajectory</p>
            <div className="h-px w-8 bg-val-border"></div>
          </div>
          <DemoProfileChips profiles={demoProfiles} onSelect={onDemoReview} isLoading={isLoading} />
        </div>
      </div>
    </section>
  );
}
