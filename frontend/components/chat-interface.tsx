"use client";

import { useState, useRef, useEffect } from 'react';
import { colors } from '@/lib/design-system';
import type { ChatMessage, OfferData, GameContext } from '@/types';
import {
  sendChatMessage,
  getNegotiationHistory,
  parseOfferFromResponse,
  formatCost,
  formatDuration,
} from '@/lib/api/chat';
import { getAgentName, getAgentInitials, getAgentRole } from '@/lib/api/agent-status';
import { acceptBudgetRevision } from '@/lib/api/sessions';

interface BudgetRevisionOffer {
  revision_amount: number; // in øre
  justification: string;
  old_budget: number; // in øre
  new_budget: number; // in øre
}

interface ChatInterfaceProps {
  sessionId: string;
  agentId: string;
  agentType: 'owner' | 'supplier';
  gameContext?: GameContext;
  onOfferAccepted?: (offer: OfferData) => void;
  onOfferRejected?: (offer: OfferData) => void;
  onOfferReceived?: (offer: OfferData | null) => void;
  onBudgetRevisionAccepted?: () => void; // New callback for budget revision
  onSwitchAgent?: () => void;
}

// Parse budget revision offers from owner agent responses
function parseBudgetRevisionFromResponse(response: string, currentBudget?: number): {
  containsRevision: boolean;
  revision_amount?: number; // in øre
  justification?: string;
  old_budget?: number; // in øre
  new_budget?: number; // in øre
} {
  // Look for budget revision patterns - VERY specific to catch ONLY the increase amount
  // Must match the APPROVAL phrase with the amount right next to it
  const revisionPatterns = [
    // Pattern 1: "godkjenner en budsjettøkning på X MNOK" (most specific - prioritize this!)
    /godkjenner\s+(?:en\s+)?budsjett(?:økning|revisjon)\s+på\s+(\d+[.,]?\d*)\s*MNOK/i,
    // Pattern 2: "godkjenner X MNOK" (followed immediately by MNOK)
    /godkjenner\s+(\d+[.,]?\d*)\s*MNOK(?:\s+ekstra)?/i,
    // Pattern 3: "økning på X MNOK" (in same sentence as approval)
    /(?:godkjenn|godtar|aksepterer).*?økning\s+på\s+(\d+[.,]?\d*)\s*MNOK/i,
    // Pattern 4: "+X MNOK" (explicit plus sign right before number)
    /\+\s*(\d+[.,]?\d*)\s*MNOK/i,
  ];

  let revision_amount: number | undefined;
  for (const pattern of revisionPatterns) {
    const match = response.match(pattern);
    if (match) {
      const value = parseFloat(match[1].replace(',', '.'));
      // Sanity check: budget increase should be between 10 and 500 MNOK
      if (value >= 10 && value <= 500) {
        revision_amount = value * 1_000_000; // Convert MNOK to NOK (same as offers)
        break;
      }
    }
  }

  // Extract justification - look for text explaining why
  let justification: string | undefined;
  const justificationPatterns = [
    /(?:fordi|grunnet|på grunn av|begrunnelse)[:\s]+([^.!?]+)/is,
    /(?:godkjent|godkjenner)[:\s]+([^.!?]+)/is,
  ];

  for (const pattern of justificationPatterns) {
    const match = response.match(pattern);
    if (match) {
      justification = match[1].trim();
      break;
    }
  }

  // Default justification if not found but revision detected
  if (revision_amount && !justification) {
    justification = "Godkjent budsjettøkning fra eier";
  }

  const containsRevision = revision_amount !== undefined;

  // Try to extract old budget from response if not provided
  let old_budget = currentBudget || 0;

  // If currentBudget seems wrong (< 10 million NOK = < 10 MNOK), try to find it in the response
  if (old_budget < 10_000_000) {
    const oldBudgetMatch = response.match(/(?:nåværende|tilgjengelig|gammelt)\s+budsjett.*?(\d+)\s*MNOK/i);
    if (oldBudgetMatch) {
      old_budget = parseFloat(oldBudgetMatch[1]) * 1_000_000; // Convert MNOK to NOK
      console.log('[BudgetRevision] Extracted old budget from response:', old_budget / 1_000_000, 'MNOK');
    } else {
      // Default to 310 MNOK if we can't find it
      old_budget = 310_000_000; // 310 MNOK in NOK
      console.warn('[BudgetRevision] Could not determine old budget, defaulting to 310 MNOK');
    }
  }

  const new_budget = old_budget + (revision_amount || 0);

  return {
    containsRevision,
    revision_amount,
    justification,
    old_budget,
    new_budget,
  };
}

export function ChatInterface({
  sessionId,
  agentId,
  agentType,
  gameContext,
  onOfferAccepted,
  onOfferRejected,
  onOfferReceived,
  onBudgetRevisionAccepted,
  onSwitchAgent,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingOffer, setPendingOffer] = useState<OfferData | null>(null);
  const [pendingBudgetRevision, setPendingBudgetRevision] = useState<BudgetRevisionOffer | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const agentName = getAgentName(agentId);
  const agentRole = getAgentRole(agentId);
  const agentInitials = getAgentInitials(agentId);

  // Load history on mount
  useEffect(() => {
    async function loadHistory() {
      try {
        setIsLoading(true);
        const history = await getNegotiationHistory(sessionId, agentId);
        setMessages(history);

        // Check for pending offer in last message
        const lastMsg = history[history.length - 1];
        if (lastMsg?.contains_offer && lastMsg.offer_data && lastMsg.role === 'agent') {
          setPendingOffer(lastMsg.offer_data);
          if (onOfferReceived) {
            onOfferReceived(lastMsg.offer_data);
          }
        }
      } catch (err) {
        console.error('Failed to load history:', err);
        // Don't show error to user, just start empty
      } finally {
        setIsLoading(false);
      }
    }

    loadHistory();
  }, [sessionId, agentId]);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      // Build conversation history
      const conversationHistory = messages.map((msg) => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.timestamp,
        is_disagreement: msg.is_disagreement,
      }));

      // Send to backend
      const response = await sendChatMessage(
        sessionId,
        agentId,
        inputMessage,
        conversationHistory,
        gameContext
      );

      // Parse response for offers
      const offerInfo = parseOfferFromResponse(response.response);

      // Create agent message
      const agentMessage: ChatMessage = {
        id: Date.now().toString() + '-agent',
        role: 'agent',
        content: response.response,
        timestamp: response.timestamp,
        agent_name: response.agent_name,
        is_disagreement: response.is_disagreement,
        contains_offer: offerInfo.containsOffer,
        offer_data: offerInfo.containsOffer
          ? {
              wbs_id: getWBSIdForAgent(agentId),
              cost: offerInfo.cost!,
              duration: offerInfo.duration!,
              quality_level: offerInfo.qualityLevel,
            }
          : undefined,
      };

      setMessages((prev) => [...prev, agentMessage]);

      // Set pending offer if detected (for supplier agents)
      if (agentMessage.contains_offer && agentMessage.offer_data) {
        setPendingOffer(agentMessage.offer_data);
        if (onOfferReceived) {
          onOfferReceived(agentMessage.offer_data);
        }
      }

      // Check for budget revision offers (for owner agent only)
      if (agentType === 'owner') {
        const budgetRevisionInfo = parseBudgetRevisionFromResponse(
          response.response,
          gameContext?.available_budget
        );

        if (budgetRevisionInfo.containsRevision) {
          const revisionOffer: BudgetRevisionOffer = {
            revision_amount: budgetRevisionInfo.revision_amount!,
            justification: budgetRevisionInfo.justification!,
            old_budget: budgetRevisionInfo.old_budget!,
            new_budget: budgetRevisionInfo.new_budget!,
          };
          setPendingBudgetRevision(revisionOffer);
        }
      }
    } catch (err: any) {
      // Handle agent locked error
      if (err.code === 'AGENT_LOCKED') {
        setError(
          `${err.message} Tilgjengelig om ${err.minutes_remaining} minutter. ${err.last_message || ''}`
        );
      } else {
        setError(err.message || 'Kunne ikke sende melding. Prøv igjen.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleAcceptOffer = () => {
    if (pendingOffer && onOfferAccepted) {
      onOfferAccepted(pendingOffer);
      setPendingOffer(null);
      if (onOfferReceived) {
        onOfferReceived(null);
      }
    }
  };

  const handleRejectOffer = () => {
    if (pendingOffer && onOfferRejected) {
      onOfferRejected(pendingOffer);
      setPendingOffer(null);
      if (onOfferReceived) {
        onOfferReceived(null);
      }

      // Add rejection message
      const rejectionMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: 'Jeg avslår dette tilbudet. Kan vi forhandle videre?',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, rejectionMessage]);
    }
  };

  const handleAcceptBudgetRevision = async () => {
    if (!pendingBudgetRevision) return;

    try {
      setIsLoading(true);
      setError(null);

      await acceptBudgetRevision(sessionId, {
        revision_amount: pendingBudgetRevision.revision_amount,
        justification: pendingBudgetRevision.justification,
        affects_total_budget: true, // Municipality budget increase affects both available and total
      });

      setPendingBudgetRevision(null);

      // Add acceptance message
      const mnokAmount = Math.round(pendingBudgetRevision.revision_amount / 1_000_000);
      const acceptanceMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: `Jeg godtar budsjettøkningen på ${mnokAmount} MNOK. Takk!`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, acceptanceMessage]);

      // Notify parent component
      if (onBudgetRevisionAccepted) {
        onBudgetRevisionAccepted();
      }
    } catch (err: any) {
      setError(err.message || 'Kunne ikke godkjenne budsjettrevisjon.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRejectBudgetRevision = () => {
    if (!pendingBudgetRevision) return;

    setPendingBudgetRevision(null);

    // Add rejection message
    const rejectionMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: 'Jeg avslår denne budsjettøkningen. Kan vi diskutere andre løsninger?',
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, rejectionMessage]);
  };

  return (
    <div className="flex h-full flex-col" style={{ backgroundColor: colors.background.card }}>
      {/* Chat Header */}
      <div
        className="flex items-center justify-between border-b p-6"
        style={{
          backgroundColor: colors.background.page,
          borderColor: colors.border.medium,
        }}
      >
        <div className="flex items-center gap-4">
          {/* Agent Avatar */}
          <div
            className="flex h-12 w-12 items-center justify-center rounded-full text-white"
            style={{
              backgroundColor: colors.button.primary.bg,
            }}
          >
            <span className="text-base font-bold">{agentInitials}</span>
          </div>

          {/* Agent Info */}
          <div>
            <h2 className="text-lg font-bold text-gray-900">{agentName}</h2>
            <p className="text-xs text-gray-600">{agentRole}</p>
          </div>
        </div>

        {/* Toggle Leverandør/Eier (optional) */}
        {onSwitchAgent && (
          <button
            onClick={onSwitchAgent}
            className="rounded border px-4 py-2 text-sm font-semibold text-gray-700 transition-colors hover:bg-gray-100"
            style={{
              borderColor: colors.border.medium,
            }}
          >
            Bytt agent
          </button>
        )}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 space-y-4 overflow-y-auto p-6">
        {messages.length === 0 && (
          <div className="text-center text-sm text-gray-500">
            <p>Start forhandlingene med {agentName}</p>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id}>
            {message.role === 'user' ? (
              <UserMessage message={message} />
            ) : (
              <AgentMessage message={message} />
            )}

            {/* Offer Box (for supplier agents) */}
            {message.contains_offer && message.offer_data && message === messages[messages.length - 1] && (
              <OfferBox
                offer={message.offer_data}
                onAccept={handleAcceptOffer}
                onReject={handleRejectOffer}
                disabled={!pendingOffer}
              />
            )}
          </div>
        ))}

        {/* Budget Revision Offer Box (for owner agent) - shown after all messages */}
        {pendingBudgetRevision && agentType === 'owner' && (
          <BudgetRevisionOfferBox
            offer={pendingBudgetRevision}
            onAccept={handleAcceptBudgetRevision}
            onReject={handleRejectBudgetRevision}
            disabled={isLoading}
          />
        )}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <div className="h-2 w-2 animate-pulse rounded-full bg-blue-500" />
            <div className="h-2 w-2 animate-pulse rounded-full bg-blue-500 animation-delay-200" />
            <div className="h-2 w-2 animate-pulse rounded-full bg-blue-500 animation-delay-400" />
            <span>{agentName} skriver...</span>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div
            className="rounded-md border-2 p-4"
            style={{
              backgroundColor: colors.status.error.bg,
              borderColor: colors.status.error.border,
            }}
          >
            <p className="text-sm font-semibold text-red-900">⚠ Feil</p>
            <p className="mt-1 text-xs text-red-800">{error}</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Field */}
      <div
        className="border-t p-4"
        style={{
          borderColor: colors.border.medium,
        }}
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            placeholder={
              pendingOffer
                ? 'Du må godta eller avslå tilbudet før du kan fortsette...'
                : 'Skriv melding...'
            }
            disabled={isLoading || !!pendingOffer}
            className="flex-1 rounded-md border px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            style={{
              backgroundColor: pendingOffer ? colors.background.input : colors.background.card,
              borderColor: colors.border.medium,
              color: colors.text.secondary,
              opacity: pendingOffer ? 0.5 : 1,
            }}
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim() || !!pendingOffer}
            className="rounded-md px-6 py-2 text-sm font-semibold text-white transition-colors disabled:opacity-50"
            style={{
              backgroundColor: colors.button.primary.bg,
            }}
          >
            {isLoading ? 'Sender...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}

// User message bubble
function UserMessage({ message }: { message: ChatMessage }) {
  return (
    <div className="flex justify-end">
      <div
        className="max-w-[700px] rounded-lg border p-4"
        style={{
          backgroundColor: colors.chat.user.bg,
          borderColor: colors.chat.user.border,
        }}
      >
        <p className="text-sm text-gray-700">{message.content}</p>
        <p className="mt-2 text-right text-xs text-gray-500">
          Du, {new Date(message.timestamp).toLocaleTimeString('nb-NO', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}

// Agent message bubble
function AgentMessage({ message }: { message: ChatMessage }) {
  return (
    <div className="flex justify-start">
      <div
        className="max-w-[700px] rounded-lg border p-4"
        style={{
          backgroundColor: colors.chat.ai.bg,
          borderColor: colors.chat.ai.border,
        }}
      >
        <p className="text-sm text-gray-700">{message.content}</p>
        <p className="mt-2 text-right text-xs text-gray-500">
          {message.agent_name},{' '}
          {new Date(message.timestamp).toLocaleTimeString('nb-NO', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}

// Offer box with accept/reject buttons
function OfferBox({
  offer,
  onAccept,
  onReject,
  disabled,
}: {
  offer: OfferData;
  onAccept: () => void;
  onReject: () => void;
  disabled: boolean;
}) {
  return (
    <div className="mt-4 flex justify-start">
      <div
        className="max-w-[700px] rounded-lg border-2 p-4"
        style={{
          backgroundColor: colors.chat.offer.bg,
          borderColor: colors.chat.offer.border,
        }}
      >
        <p className="text-sm font-bold text-green-900">✓ TILBUD KLAR</p>
        <div className="mt-2 space-y-1 text-sm text-gray-700">
          <p>Pakke: WBS {offer.wbs_id}</p>
          <p>Kostnad: {formatCost(offer.cost)}</p>
          <p>Varighet: {formatDuration(offer.duration)}</p>
          {offer.quality_level && (
            <p>
              Kvalitet: {offer.quality_level === 'standard' ? 'Standard' : offer.quality_level === 'budget' ? 'Budsjett' : 'Premium'}
            </p>
          )}
        </div>

        {/* Accept/Reject Buttons */}
        <div className="mt-4 flex gap-4">
          <button
            onClick={onAccept}
            disabled={disabled}
            className="rounded-md px-6 py-3 text-sm font-semibold text-white transition-colors disabled:opacity-50"
            style={{
              backgroundColor: colors.button.success.bg,
            }}
            onMouseEnter={(e) => {
              if (!disabled) {
                e.currentTarget.style.backgroundColor = colors.button.success.hover;
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = colors.button.success.bg;
            }}
          >
            ✓ Godta tilbud: {formatCost(offer.cost)}, {formatDuration(offer.duration)}
          </button>

          <button
            onClick={onReject}
            disabled={disabled}
            className="rounded-md border px-6 py-3 text-sm font-semibold transition-colors disabled:opacity-50"
            style={{
              backgroundColor: colors.button.secondary.bg,
              borderColor: colors.button.secondary.border,
              color: colors.button.secondary.text,
            }}
          >
            ✗ Avslå og reforhandle
          </button>
        </div>

        <p className="mt-2 text-xs text-green-700">
          Ved å godta, oppdateres budsjettet ditt automatisk
        </p>
      </div>
    </div>
  );
}

// Budget Revision Offer Box with accept/reject buttons
function BudgetRevisionOfferBox({
  offer,
  onAccept,
  onReject,
  disabled,
}: {
  offer: BudgetRevisionOffer;
  onAccept: () => void;
  onReject: () => void;
  disabled: boolean;
}) {
  // Helper to convert NOK to MNOK for display
  const formatToMNOK = (nokAmount: number): string => {
    const mnok = nokAmount / 1_000_000; // NOK to MNOK
    return `${mnok.toFixed(0)} MNOK`;
  };

  return (
    <div className="mt-4 flex justify-start">
      <div
        className="max-w-[700px] rounded-lg border-2 p-4"
        style={{
          backgroundColor: colors.chat.offer.bg,
          borderColor: colors.chat.offer.border,
        }}
      >
        <p className="text-sm font-bold text-green-900">💰 BUDSJETTØKNING TILGJENGELIG</p>
        <div className="mt-2 space-y-1 text-sm text-gray-700">
          <p>Økning: {formatToMNOK(offer.revision_amount)}</p>
          <p>Gammelt budsjett: {formatToMNOK(offer.old_budget)}</p>
          <p>Nytt budsjett: {formatToMNOK(offer.new_budget)}</p>
          <p className="mt-2 italic">Begrunnelse: {offer.justification}</p>
        </div>

        {/* Accept/Reject Buttons */}
        <div className="mt-4 flex gap-4">
          <button
            onClick={onAccept}
            disabled={disabled}
            className="rounded-md px-6 py-3 text-sm font-semibold text-white transition-colors disabled:opacity-50"
            style={{
              backgroundColor: colors.button.success.bg,
            }}
            onMouseEnter={(e) => {
              if (!disabled) {
                e.currentTarget.style.backgroundColor = colors.button.success.hover;
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = colors.button.success.bg;
            }}
          >
            ✓ Godta budsjettøkning
          </button>

          <button
            onClick={onReject}
            disabled={disabled}
            className="rounded-md border px-6 py-3 text-sm font-semibold transition-colors disabled:opacity-50"
            style={{
              backgroundColor: colors.button.secondary.bg,
              borderColor: colors.button.secondary.border,
              color: colors.button.secondary.text,
            }}
          >
            ✗ Avslå
          </button>
        </div>

        <p className="mt-2 text-xs text-green-700">
          Ved å godta, øker det tilgjengelige budsjettet ditt
        </p>
      </div>
    </div>
  );
}

// Helper to map agent ID to WBS ID
function getWBSIdForAgent(agentId: string): '1.3.1' | '1.3.2' | '1.4.1' {
  const mapping: Record<string, '1.3.1' | '1.3.2' | '1.4.1'> = {
    'bjorn-eriksen': '1.3.1',
    'kari-andersen': '1.3.2',
    'per-johansen': '1.4.1',
  };

  return mapping[agentId] || '1.3.1';
}
