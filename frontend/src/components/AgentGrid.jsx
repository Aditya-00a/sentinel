import React from 'react';
import AgentCard from './AgentCard';

export default function AgentGrid({ agentStates }) {
  const agents = [
    { key: 'trajectory', num: '01' },
    { key: 'context', num: '02' },
    { key: 'intervention', num: '03' },
    { key: 'effectiveness', num: '04' },
  ];

  return (
    <section className="relative py-10 px-6">
      <div className="absolute inset-0 grid-dots opacity-20"></div>
      <div className="max-w-5xl mx-auto relative">
        <div className="flex items-center gap-3 mb-8">
          <div className="accent-bar h-6"></div>
          <span className="section-num">// AGENT FORECAST</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {agents.map(({ key, num }) => (
            <AgentCard
              key={key}
              name={key}
              num={num}
              status={agentStates[key]?.status || 'idle'}
              result={agentStates[key]?.result || null}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
