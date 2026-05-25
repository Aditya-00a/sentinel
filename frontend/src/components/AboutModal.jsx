import React from 'react';

export default function AboutModal({ onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-val-card border border-val-border rounded max-w-lg w-full overflow-hidden animate-fade-in" onClick={e => e.stopPropagation()}>
        <div className="h-0.5 bg-val-red"></div>
        <div className="p-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <div className="section-num mb-1">// About</div>
              <h2 className="text-xl font-extrabold text-white uppercase tracking-wide">Sentinel</h2>
            </div>
            <button onClick={onClose} className="text-val-dim hover:text-white transition-colors font-mono text-lg">x</button>
          </div>

          <div className="space-y-6 text-sm text-val-gray leading-relaxed">
            <div>
              <h3 className="text-[9px] font-mono font-bold text-val-red uppercase tracking-widest-xl mb-2">What This Is</h3>
              <p>
                Sentinel is a concept demo of a pre-escalation intelligence system. Instead of reviewing
                player reports after the fact, it forecasts behavioral spirals and recommends proactive
                interventions — treating community health like public health, not policing.
              </p>
            </div>

            <div>
              <h3 className="text-[9px] font-mono font-bold text-val-red uppercase tracking-widest-xl mb-2">Who Built It</h3>
              <p>
                <span className="text-white font-bold">Aditya Sakhale</span> — MS Management & Analytics, NYU Stern 2026.
                Trust & Safety Lab coordinator at NYU. Building at the intersection of AI governance,
                behavioral prediction, and player experience.
              </p>
              <a href="https://linkedin.com/in/adityasakhale" target="_blank" rel="noopener noreferrer"
                className="text-val-red hover:text-val-red-deep text-[10px] font-mono mt-2 inline-block transition-colors tracking-wide">
                linkedin.com/in/adityasakhale
              </a>
            </div>

            <div>
              <h3 className="text-[9px] font-mono font-bold text-val-red uppercase tracking-widest-xl mb-2">Why Prediction Over Detection</h3>
              <p>
                The gaming industry has gotten very good at detecting toxicity after it happens.
                The unsolved problem is that players still don't feel safer despite more bans.
                Sentinel demonstrates that the next frontier isn't better detection — it's earlier
                intervention. Predict the spiral, intervene with the minimum effective dose,
                and measure whether it worked.
              </p>
            </div>

            <div className="pt-4 border-t border-val-border">
              <a href="mailto:as18513@nyu.edu?subject=Sentinel%20Demo%20-%20Let's%20Talk"
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-val-red hover:bg-val-red-deep text-white font-bold rounded transition-colors text-xs uppercase tracking-wide-lg cut-corner">
                Let's talk
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
