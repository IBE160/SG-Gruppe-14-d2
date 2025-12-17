"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { colors } from '@/lib/design-system';
import { BudgetDisplay } from '@/components/budget-display';
import { GanttChart } from '@/components/gantt-chart';
import { PrecedenceDiagram } from '@/components/precedence-diagram';
import { HistoryPanel } from '@/components/history-panel';
import { ChatInterface } from '@/components/chat-interface';
import { createSession, getUserSessions } from '@/lib/api/sessions';
import { createClient } from '@/lib/supabase/client';
import { getAuthToken } from '@/lib/auth-utils';
import type { GameSession, GameContext } from '@/types';

export default function DashboardPage() {
  const router = useRouter();
  const [session, setSession] = useState<GameSession | null>(null);
  const [wbsElements, setWbsElements] = useState<any[]>([]);
  const [agents, setAgents] = useState<any[]>([]);
  const [commitments, setCommitments] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'gantt' | 'precedence'>('overview');
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    // Load commitments and validation data when session changes
    if (session) {
      loadCommitmentsAndValidation();
    }
  }, [session]);

  async function loadDashboard() {
    try {
      setIsLoading(true);
      setError(null);

      // Load static data
      const [wbsRes, agentsRes] = await Promise.all([
        fetch('/data/wbs.json'),
        fetch('/data/agents.json'),
      ]);

      if (!wbsRes.ok || !agentsRes.ok) {
        throw new Error('Kunne ikke laste data');
      }

      const wbsData = await wbsRes.json();
      const agentsData = await agentsRes.json();

      setWbsElements(wbsData.wbs_elements || []);
      setAgents(agentsData.agents || []);

      // Check for existing active session
      const sessions = await getUserSessions();
      const activeSession = sessions.find((s) => s.status === 'in_progress');

      if (activeSession) {
        setSession(activeSession);
      } else {
        // Create new session
        const newSession = await createSession();
        setSession(newSession);
      }
    } catch (err: any) {
      console.error('Dashboard load error:', err);
      setError(err.message || 'Kunne ikke laste dashboard');
    } finally {
      setIsLoading(false);
    }
  }

  async function loadCommitmentsAndValidation() {
    if (!session) return;

    try {
      // Get JWT token from Supabase session
      const token = await getAuthToken();
      if (!token) {
        console.error('No auth token found');
        return;
      }

      // Fetch commitments
      const commitmentsRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${session.id}/commitments`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (commitmentsRes.ok) {
        const commitmentsData = await commitmentsRes.json();
        setCommitments(commitmentsData);
      }

      // Fetch validation/timeline data
      const validationRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${session.id}/validate`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      if (validationRes.ok) {
        const validationData = await validationRes.json();
        setTimeline(validationData);
      }
    } catch (err) {
      console.error('Error loading commitments/validation:', err);
    }
  }

  function handleWBSClick(wbs: any) {
    if (!wbs.is_negotiable || !session) return;

    // Navigate to game page for this WBS
    router.push(`/game/${session.id}/${wbs.assigned_supplier}/${wbs.id}`);
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-500 border-t-transparent mx-auto" />
          <p className="text-sm text-gray-600">Laster prosjektoversikt...</p>
        </div>
      </div>
    );
  }

  if (error || !session) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div
          className="max-w-md rounded-lg border-2 p-6"
          style={{
            backgroundColor: colors.status.error.bg,
            borderColor: colors.status.error.border,
          }}
        >
          <p className="text-sm font-bold text-red-900">⚠ Feil</p>
          <p className="mt-2 text-sm text-red-800">{error || 'Ingen aktiv økt'}</p>
          <button
            onClick={() => loadDashboard()}
            className="mt-4 rounded-md px-4 py-2 text-sm font-semibold text-white"
            style={{ backgroundColor: colors.button.primary.bg }}
          >
            Prøv igjen
          </button>
        </div>
      </div>
    );
  }

  const negotiableWBS = wbsElements.filter((w) => w.is_negotiable);
  const lockedWBS = wbsElements.filter((w) => !w.is_negotiable);

  // Calculate initial deficit
  const initialDeficit = 35000000; // 35 MNOK as specified
  const totalNeeded = negotiableWBS.reduce((sum, w) => sum + (w.baseline_cost || 0), 0);

  const gameContext: GameContext = {
    total_budget: session.total_budget,
    current_budget_used: session.current_budget_used,
    available_budget: session.available_budget,
    locked_budget: session.locked_budget,
    deadline_date: session.deadline_date,
    committed_wbs: session.negotiable_wbs_commitments || [],
  };

  return (
    <div className="min-h-screen" style={{ backgroundColor: colors.background.page }}>
      {/* Header */}
      <header
        className="border-b"
        style={{
          backgroundColor: colors.background.card,
          borderColor: colors.border.medium,
        }}
      >
        <div className="mx-auto max-w-7xl px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">PM Simulator</h1>
          <p className="text-sm text-gray-600">
            Boligutbyggingsprosjekt Fjordvik | Frist: 15. mai 2026
          </p>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="mx-auto max-w-7xl px-6 pt-6">
        <div className="flex gap-2 mb-4 border-b justify-between items-center" style={{ borderColor: colors.border.medium }}>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-4 py-2 text-sm font-semibold transition-colors ${
                activeTab === 'overview'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              📊 Oversikt
            </button>
            <button
              onClick={() => setActiveTab('gantt')}
              className={`px-4 py-2 text-sm font-semibold transition-colors ${
                activeTab === 'gantt'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              📈 Gantt-diagram
            </button>
            <button
              onClick={() => setActiveTab('precedence')}
              className={`px-4 py-2 text-sm font-semibold transition-colors ${
                activeTab === 'precedence'
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              🔀 Presedensdiagram
            </button>
          </div>
          <button
            onClick={() => setIsHistoryOpen(true)}
            className="px-4 py-2 text-sm font-semibold text-white rounded transition-colors hover:opacity-90"
            style={{ backgroundColor: colors.button.primary.bg }}
          >
            🕒 Historikk
          </button>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* Visualization Views */}
        {activeTab === 'gantt' && (
          <GanttChart wbsItems={wbsElements} commitments={commitments} timeline={timeline} />
        )}

        {activeTab === 'precedence' && (
          <PrecedenceDiagram wbsItems={wbsElements} timeline={timeline} />
        )}

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2 space-y-8">
            {/* Budget Section */}
            <div
              className="rounded-lg border p-6"
              style={{
                backgroundColor: colors.background.card,
                borderColor: colors.border.medium,
              }}
            >
              <BudgetDisplay session={session} showDetails={true} />
            </div>

            {/* Initial Challenge Banner */}
            {initialDeficit > 0 && (
              <div
                className="rounded-lg border-2 p-6"
                style={{
                  backgroundColor: colors.status.warning.bg,
                  borderColor: colors.status.warning.border,
                }}
              >
                <p className="text-lg font-bold text-orange-900">⚠ BUDSJETTUTFORDRING</p>
                <p className="mt-2 text-sm text-orange-800">
                  Leverandørenes starttilbud overstiger tilgjengelig budsjett med{' '}
                  <strong>35 MNOK</strong>. Du må forhandle ned kostnadene før du kan forplikte deg
                  til leveransene.
                </p>
              </div>
            )}

            {/* WBS List */}
            <div
              className="rounded-lg border"
              style={{
                backgroundColor: colors.background.card,
                borderColor: colors.border.medium,
              }}
            >
              <div className="border-b p-6" style={{ borderColor: colors.border.medium }}>
                <h2 className="text-lg font-bold text-gray-900">Arbeidspakker (WBS)</h2>
                <p className="text-sm text-gray-600">
                  {negotiableWBS.length} forhandlingsbare | {lockedWBS.length} låste
                </p>
              </div>

              <div className="p-6 space-y-3">
                {/* Negotiable WBS */}
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Forhandlingsbare pakker
                </h3>
                {negotiableWBS.map((wbs) => {
                  const agent = agents.find((a) => a.id === wbs.assigned_supplier);
                  return (
                    <div
                      key={wbs.id}
                      onClick={() => handleWBSClick(wbs)}
                      className="rounded-lg border p-4 cursor-pointer transition-all hover:shadow-md"
                      style={{
                        backgroundColor: colors.wbs.negotiable.bg,
                        borderColor: colors.wbs.negotiable.border,
                      }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-mono text-gray-600">{wbs.id}</span>
                            <span className="text-sm font-bold text-gray-900">{wbs.name}</span>
                          </div>
                          <p className="mt-1 text-xs text-gray-600">{wbs.description}</p>
                          {agent && (
                            <p className="mt-2 text-xs text-blue-700">
                              Leverandør: {agent.name}
                            </p>
                          )}
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-bold text-gray-900">
                            {(wbs.baseline_cost / 1_000_000).toFixed(0)} MNOK
                          </p>
                          <p className="text-xs text-gray-600">{wbs.baseline_duration} dager</p>
                          <button
                            className="mt-2 rounded px-3 py-1 text-xs font-semibold text-white"
                            style={{ backgroundColor: colors.button.primary.bg }}
                          >
                            Forhandle →
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}

                {/* Locked WBS */}
                <h3 className="text-sm font-semibold text-gray-700 mt-6 mb-2">Låste pakker</h3>
                {lockedWBS.map((wbs) => (
                  <div
                    key={wbs.id}
                    className="rounded-lg border p-4 opacity-75"
                    style={{
                      backgroundColor: colors.wbs.locked.bg,
                      borderColor: colors.wbs.locked.border,
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono text-gray-600">{wbs.id}</span>
                          <span className="text-sm font-medium text-gray-700">{wbs.name}</span>
                          <span className="text-xs text-gray-500">🔒 Låst</span>
                        </div>
                        <p className="mt-1 text-xs text-gray-600">{wbs.description}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-700">
                          {(wbs.locked_cost / 1_000_000).toFixed(0)} MNOK
                        </p>
                        <p className="text-xs text-gray-600">{wbs.locked_duration} dager</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Challenge Box */}
            <div
              className="rounded-lg border-2 p-6"
              style={{
                backgroundColor: colors.status.error.bg,
                borderColor: colors.status.error.border,
              }}
            >
              <h3 className="text-sm font-bold text-red-900">Budsjettutfordring</h3>
              <p className="mt-2 text-xs text-red-800">
                Tilgjengelig: 310 MNOK
                <br />
                Starttilbud: 345 MNOK
                <br />
                <strong>Underskudd: -35 MNOK</strong>
              </p>
            </div>

            {/* Solution Box */}
            <div
              className="rounded-lg border-2 p-6"
              style={{
                backgroundColor: colors.status.success.bg,
                borderColor: colors.status.success.border,
              }}
            >
              <h3 className="text-sm font-bold text-green-900">Løsning</h3>
              <p className="mt-2 text-xs text-green-800">
                Forhandle med leverandørene for å redusere kostnadene, eller be kommunen om
                budsjettøkning eller omfangsreduksjon.
              </p>
            </div>

            {/* Owner Chat Panel */}
            <div
              className="rounded-lg border overflow-hidden flex flex-col h-[600px]"
              style={{
                backgroundColor: colors.background.card,
                borderColor: colors.border.medium,
              }}
            >
              <ChatInterface
                sessionId={session.id}
                agentId="anne-lise-berg"
                agentType="owner"
                gameContext={gameContext}
              />
            </div>
          </div>
        </div>
        )}
      </div>

      {/* History Panel Overlay */}
      {session && (
        <HistoryPanel
          sessionId={session.id}
          isOpen={isHistoryOpen}
          onClose={() => setIsHistoryOpen(false)}
          wbsItems={wbsElements}
        />
      )}
    </div>
  );
}
