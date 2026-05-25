import React from 'react';

export default function Footer() {
  return (
    <footer className="py-6 px-6 border-t border-val-border">
      <div className="max-w-5xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-val-red font-mono text-[9px]">//</span>
          <span className="text-[9px] font-mono text-val-dim uppercase tracking-wide">SENTINEL v1.0</span>
        </div>
        <p className="text-[9px] text-val-dim leading-relaxed text-center max-w-2xl font-mono">
          Independent concept demo by Aditya Sakhale, built using the public Riot Games API.
          Not affiliated with, endorsed by, or sponsored by Riot Games.
          League of Legends, Valorant, and Riot Games are trademarks of Riot Games, Inc.
        </p>
        <span className="text-val-border font-mono text-sm select-none hidden sm:block">+</span>
      </div>
    </footer>
  );
}
