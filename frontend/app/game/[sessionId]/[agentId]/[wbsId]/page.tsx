"use client";

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { colors } from '@/lib/design-system';
import { ChatInterface } from '@/components/chat-interface';
import { getSession, createCommitment } from '@/lib/api/sessions';
import type { GameSession, OfferData, GameContext } from '@/types';

interface WBSElement {
  id: string;
  name: string;
  description: string;
  is_negotiable: boolean;
  baseline_cost: number;
  baseline_duration: number;
  assigned_supplier: string;
}

interface Agent {
  id: string;
  name: string;
  role: string;
  type: 'owner' | 'supplier';
  initials: string;
  avatar_color: string;
}

export default function GamePage() {
  const params = useParams();
  const router = useRouter();

  const sessionId = params.sessionId as string;
  const agentId = params.agentId as string;
  const wbsId = params.wbsId as string;

  const [session, setSession] = useState<GameSession | null>(null);
  const [wbsElement, setWbsElement] = useState<WBSElement | null>(null);
  const [agent, setAgent] = useState<Agent | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pendingOffer, setPendingOffer] = useState<OfferData | null>(null);

  useEffect(() => {
    loadGameData();
  }, [sessionId, agentId, wbsId]);

  async function loadGameData() {
    try {
      setIsLoading(true);
      setError(null);

      // Load session data
      const sessionData = await getSession(sessionId);
      // Backend returns session object directly, not wrapped
      setSession(sessionData as unknown as GameSession);

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

      // Find the specific WBS element
      const wbs = wbsData.wbs_elements.find((w: any) => w.id === wbsId);
      if (!wbs) {
        throw new Error(`WBS-element ${wbsId} ikke funnet`);
      }
      setWbsElement(wbs);

      // Find the agent
      const agentInfo = agentsData.agents.find((a: any) => a.id === agentId);
      if (!agentInfo) {
        throw new Error(`Agent ${agentId} ikke funnet`);
      }
      setAgent(agentInfo);
    } catch (err: any) {
      console.error('Game load error:', err);
      setError(err.message || 'Kunne ikke laste spill');
    } finally {
      setIsLoading(false);
    }
  }

  async function handleOfferAccepted(offer: OfferData) {
    if (!session || !wbsElement) return;

    try {
      // Create commitment via API
      const response = await createCommitment(sessionId, {
        wbs_id: offer.wbs_id as '1.3.1' | '1.3.2' | '1.4.1',
        wbs_name: wbsElement.name,
        agent_id: agentId,
        baseline_cost: wbsElement.baseline_cost,
        negotiated_cost: offer.cost,
        committed_cost: offer.cost,
        baseline_duration: wbsElement.baseline_duration,
        negotiated_duration: offer.duration,
        quality_level: offer.quality_level as 'standard' | 'budget' | 'premium' | undefined,
      });

      // Update session state
      setSession(response.updated_session);
      setPendingOffer(null);

      // Show success and navigate back to dashboard after 2 seconds
      alert(
        `✓ TILBUD GODTATT!\n\nPakke: ${wbsElement.name}\nKostnad: ${(offer.cost / 1_000_000).toFixed(0)} MNOK\nVarighet: ${offer.duration} dager\n\nBudsjett oppdatert. Du blir sendt tilbake til oversikten.`
      );

      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 2000);
    } catch (err: any) {
      if (err.code === 'BUDGET_EXCEEDED') {
        alert(`⚠ BUDSJETTOVERSKRIDELSE\n\n${err.message}\n\nDu må avslå tilbudet og forhandle videre.`);
      } else {
        setError(err.message || 'Kunne ikke godta tilbud');
      }
    }
  }

  function handleOfferRejected(offer: OfferData) {
    setPendingOffer(null);
    // User can continue negotiating
  }

  function calculateBudgetImpact(offer: OfferData | null) {
    if (!session || !offer) {
      return {
        newUsed: session?.current_budget_used || 0,
        newRemaining: session?.budget_remaining || session?.available_budget || 0,
        newPercentage: session?.budget_tier1_percentage || 0,
        isOverBudget: false,
      };
    }

    const newUsed = session.current_budget_used + offer.cost;
    const newRemaining = session.available_budget - newUsed;
    const newPercentage = (newUsed / session.available_budget) * 100;
    const isOverBudget = newUsed > session.available_budget;

    return {
      newUsed,
      newRemaining,
      newPercentage,
      isOverBudget,
    };
  }

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-blue-500 border-t-transparent mx-auto" />
          <p className="text-sm text-gray-600">Laster forhandling...</p>
        </div>
      </div>
    );
  }

  if (error || !session || !wbsElement || !agent) {
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
          <p className="mt-2 text-sm text-red-800">{error || 'Data mangler'}</p>
          <button
            onClick={() => router.push('/dashboard')}
            className="mt-4 rounded-md px-4 py-2 text-sm font-semibold text-white"
            style={{ backgroundColor: colors.button.primary.bg }}
          >
            Tilbake til oversikten
          </button>
        </div>
      </div>
    );
  }

  const gameContext: GameContext = {
    total_budget: session.total_budget,
    current_budget_used: session.current_budget_used,
    available_budget: session.available_budget,
    locked_budget: session.locked_budget,
    deadline_date: session.deadline_date,
    committed_wbs: session.negotiable_wbs_commitments || [],
  };

  const budgetImpact = calculateBudgetImpact(pendingOffer);

  return (
    <div className="flex h-screen" style={{ backgroundColor: colors.background.page }}>
      {/* Left Side: Chat Interface (2/3 width) */}
      <div className="flex-1 flex flex-col" style={{ maxWidth: '66.666667%' }}>
        {/* Top Bar */}
        <div
          className="border-b p-4"
          style={{
            backgroundColor: colors.background.card,
            borderColor: colors.border.medium,
          }}
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-bold text-gray-900">
                Forhandling: {wbsElement.name}
              </h1>
              <p className="text-xs text-gray-600">{wbsElement.description}</p>
              <p className="mt-1 text-xs text-blue-700">
                Baseline: {(wbsElement.baseline_cost / 1_000_000).toFixed(0)} MNOK,{' '}
                {wbsElement.baseline_duration} dager
              </p>
            </div>
            <button
              onClick={() => router.push('/dashboard')}
              className="rounded border px-4 py-2 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-100"
              style={{
                borderColor: colors.border.medium,
              }}
            >
              ← Tilbake
            </button>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="flex-1 overflow-hidden">
          <ChatInterface
            sessionId={sessionId}
            agentId={agentId}
            agentType={agent.type}
            gameContext={gameContext}
            onOfferAccepted={handleOfferAccepted}
            onOfferRejected={handleOfferRejected}
            onOfferReceived={setPendingOffer}
          />
        </div>
      </div>

      {/* Right Side: Budget Impact Preview (1/3 width) */}
      <div
        className="w-96 border-l p-6 overflow-y-auto"
        style={{
          backgroundColor: colors.background.card,
          borderColor: colors.border.medium,
        }}
      >
        <h2 className="text-base font-bold text-gray-900 mb-4">Budsjettpåvirkning</h2>

        {/* Current Budget Status */}
        <div
          className="rounded-md border p-4 mb-4"
          style={{
            backgroundColor: colors.budget.tier1.bg,
            borderColor: colors.border.medium,
          }}
        >
          <p className="text-xs font-semibold text-gray-700 mb-2">Nåværende status</p>
          <p className="text-sm text-gray-700">
            Brukt: {(session.current_budget_used / 1_000_000).toFixed(0)} MNOK
          </p>
          <p className="text-sm text-gray-700">
            Gjenstår: {((session.budget_remaining || session.available_budget) / 1_000_000).toFixed(0)} MNOK
          </p>
          <p className="text-sm text-gray-700">
            Prosent: {(session.budget_tier1_percentage || 0).toFixed(0)}%
          </p>
        </div>

        {/* Pending Offer Impact */}
        {pendingOffer ? (
          <div
            className="rounded-md border-2 p-4 mb-4"
            style={{
              backgroundColor: budgetImpact.isOverBudget
                ? colors.status.error.bg
                : colors.status.warning.bg,
              borderColor: budgetImpact.isOverBudget
                ? colors.status.error.border
                : colors.status.warning.border,
            }}
          >
            <p className="text-xs font-bold text-gray-900 mb-2">
              {budgetImpact.isOverBudget ? '⚠ VED GODKJENNING (OVERSKRIDELSE)' : '⚠ VED GODKJENNING'}
            </p>
            <p className="text-sm text-gray-700">
              Nytt tilbud: +{(pendingOffer.cost / 1_000_000).toFixed(0)} MNOK
            </p>
            <p className="text-sm text-gray-700">
              Totalt brukt: {(budgetImpact.newUsed / 1_000_000).toFixed(0)} MNOK
            </p>
            <p className="text-sm text-gray-700">
              Gjenstår:{' '}
              <strong
                style={{
                  color: budgetImpact.isOverBudget ? colors.status.error.border : 'inherit',
                }}
              >
                {(budgetImpact.newRemaining / 1_000_000).toFixed(0)} MNOK
              </strong>
            </p>
            <p className="text-sm text-gray-700">
              Prosent: {budgetImpact.newPercentage.toFixed(0)}%
            </p>

            {budgetImpact.isOverBudget && (
              <p className="mt-2 text-xs text-red-800 font-semibold">
                Dette tilbudet vil overskride budsjettet. Avslå og forhandle videre!
              </p>
            )}
          </div>
        ) : (
          <div
            className="rounded-md border p-4 mb-4"
            style={{
              backgroundColor: colors.background.input,
              borderColor: colors.border.medium,
            }}
          >
            <p className="text-xs text-gray-600">
              Når leverandøren kommer med et tilbud, vil budsjettpåvirkningen vises her.
            </p>
          </div>
        )}

        {/* Info Panel */}
        <div
          className="rounded-md border p-4"
          style={{
            backgroundColor: colors.background.input,
            borderColor: colors.border.medium,
          }}
        >
          <h3 className="text-xs font-semibold text-gray-700 mb-2">Forhandlingstips</h3>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Vær tydelig på dine budsjettbegrensninger</li>
            <li>• Spør om alternative løsninger</li>
            <li>• Vurder kvalitet vs. pris</li>
            <li>• Husk: Fristen kan IKKE forlenges</li>
            <li>• Du kan forhandle med Anne-Lise om budsjettøkning</li>
          </ul>
        </div>

        {/* WBS Package Info */}
        <div
          className="rounded-md border p-4 mt-4"
          style={{
            backgroundColor: colors.background.input,
            borderColor: colors.border.medium,
          }}
        >
          <h3 className="text-xs font-semibold text-gray-700 mb-2">Pakkeinformasjon</h3>
          <p className="text-xs text-gray-700">
            <strong>ID:</strong> {wbsElement.id}
          </p>
          <p className="text-xs text-gray-700">
            <strong>Navn:</strong> {wbsElement.name}
          </p>
          <p className="text-xs text-gray-700">
            <strong>Leverandør:</strong> {agent.name}
          </p>
          <p className="text-xs text-gray-700">
            <strong>Baseline kostnad:</strong> {(wbsElement.baseline_cost / 1_000_000).toFixed(0)} MNOK
          </p>
          <p className="text-xs text-gray-700">
            <strong>Baseline varighet:</strong> {wbsElement.baseline_duration} dager
          </p>
        </div>
      </div>
    </div>
  );
}
