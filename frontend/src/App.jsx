import React, { useState, useEffect, useCallback } from 'react';
import TopNav from './components/TopNav';
import PlayerInput from './components/PlayerInput';
import AgentGrid from './components/AgentGrid';
import DecisionPanel from './components/DecisionPanel';
import HowItWorks from './components/HowItWorks';
import AboutModal from './components/AboutModal';
import Footer from './components/Footer';
import { fetchDemoProfiles, fetchDataMode, streamReview, streamDemoReview } from './api';

const INITIAL_AGENT_STATES = {
  trajectory: { status: 'idle', result: null },
  context: { status: 'idle', result: null },
  intervention: { status: 'idle', result: null },
  effectiveness: { status: 'idle', result: null },
};

export default function App() {
  const [game, setGame] = useState('lol');
  const [dataMode, setDataMode] = useState('demo');
  const [currentView, setCurrentView] = useState('demo');
  const [showAbout, setShowAbout] = useState(false);
  const [demoProfiles, setDemoProfiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [agentStates, setAgentStates] = useState(INITIAL_AGENT_STATES);
  const [orchestratorResult, setOrchestratorResult] = useState(null);
  const [fullReview, setFullReview] = useState(null);
  const [error, setError] = useState(null);
  const [hasResults, setHasResults] = useState(false);

  useEffect(() => {
    fetchDemoProfiles().then(setDemoProfiles).catch(() => {});
    fetchDataMode().then(d => setDataMode(d.mode)).catch(() => {});
  }, []);

  const resetState = useCallback(() => {
    setAgentStates(INITIAL_AGENT_STATES);
    setOrchestratorResult(null);
    setFullReview(null);
    setError(null);
    setHasResults(false);
    setIsLoading(false);
  }, []);

  const handleViewChange = useCallback((view) => {
    if (view === 'about') {
      setShowAbout(true);
    } else {
      setCurrentView(view);
      if (view === 'demo') resetState();
    }
  }, [resetState]);

  const handleEvent = useCallback((eventType, data) => {
    if (eventType === 'status') {
      if (data.stage === 'agents_running') {
        setAgentStates(prev => ({
          ...prev,
          trajectory: { ...prev.trajectory, status: 'thinking' },
          context: { ...prev.context, status: 'thinking' },
        }));
      } else if (data.stage === 'intervention_running') {
        setAgentStates(prev => ({
          ...prev,
          intervention: { ...prev.intervention, status: 'thinking' },
        }));
      } else if (data.stage === 'effectiveness_running') {
        setAgentStates(prev => ({
          ...prev,
          effectiveness: { ...prev.effectiveness, status: 'thinking' },
        }));
      } else if (data.data_mode) {
        setDataMode(data.data_mode);
      }
    } else if (eventType === 'agent_result') {
      if (data.agent === 'orchestrator') {
        setOrchestratorResult(data.result);
      } else {
        setAgentStates(prev => ({
          ...prev,
          [data.agent]: { status: 'done', result: data.result },
        }));
      }
    }
  }, []);

  const handleComplete = useCallback((review) => {
    setFullReview(review);
    setOrchestratorResult(review.orchestrator);
    setIsLoading(false);
    setHasResults(true);
    setDataMode(review.data_mode);
  }, []);

  const handleError = useCallback((err) => {
    setError(err.message || 'Forecast failed');
    setIsLoading(false);
  }, []);

  const handleReview = useCallback((body) => {
    resetState();
    setIsLoading(true);
    setHasResults(true);
    setCurrentView('demo');
    streamReview(body, handleEvent, handleComplete, handleError);
  }, [resetState, handleEvent, handleComplete, handleError]);

  const handleDemoReview = useCallback((profileId) => {
    resetState();
    setIsLoading(true);
    setHasResults(true);
    setCurrentView('demo');
    streamDemoReview(profileId, handleEvent, handleComplete, handleError);
  }, [resetState, handleEvent, handleComplete, handleError]);

  if (currentView === 'how-it-works') {
    return (
      <div className="min-h-screen bg-val-dark">
        <TopNav game={game} onGameChange={setGame} dataMode={dataMode} currentView={currentView} onViewChange={handleViewChange} />
        <HowItWorks onBack={() => setCurrentView('demo')} />
        <Footer />
        {showAbout && <AboutModal onClose={() => setShowAbout(false)} />}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-val-dark flex flex-col">
      <TopNav game={game} onGameChange={setGame} dataMode={dataMode} currentView={currentView} onViewChange={handleViewChange} />
      <PlayerInput game={game} onReview={handleReview} onDemoReview={handleDemoReview} isLoading={isLoading} demoProfiles={demoProfiles} />

      {error && (
        <div className="px-6 pb-4">
          <div className="max-w-3xl mx-auto bg-val-red/10 border border-val-red/30 rounded p-4 text-center">
            <p className="text-sm text-val-red">{error}</p>
            <button onClick={resetState} className="text-xs text-val-dim font-mono uppercase tracking-wide hover:text-white mt-2 transition-colors">Try again</button>
          </div>
        </div>
      )}

      {hasResults && (
        <>
          <AgentGrid agentStates={agentStates} />
          {orchestratorResult && (
            <DecisionPanel result={orchestratorResult} fullReview={fullReview}
              onReset={() => { resetState(); window.scrollTo({ top: 0, behavior: 'smooth' }); }} />
          )}
        </>
      )}

      <div className="mt-auto"><Footer /></div>
      {showAbout && <AboutModal onClose={() => setShowAbout(false)} />}
    </div>
  );
}
