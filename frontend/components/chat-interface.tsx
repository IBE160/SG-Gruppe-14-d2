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

interface ChatInterfaceProps {
  sessionId: string;
  agentId: string;
  agentType: 'owner' | 'supplier';
  gameContext?: GameContext;
  onOfferAccepted?: (offer: OfferData) => void;
  onOfferRejected?: (offer: OfferData) => void;
  onOfferReceived?: (offer: OfferData | null) => void;
  onSwitchAgent?: () => void;
}

export function ChatInterface({
  sessionId,
  agentId,
  agentType,
  gameContext,
  onOfferAccepted,
  onOfferRejected,
  onOfferReceived,
  onSwitchAgent,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingOffer, setPendingOffer] = useState<OfferData | null>(null);
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

      // Set pending offer if detected
      if (agentMessage.contains_offer && agentMessage.offer_data) {
        setPendingOffer(agentMessage.offer_data);
        if (onOfferReceived) {
          onOfferReceived(agentMessage.offer_data);
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

            {/* Offer Box */}
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

// Helper to map agent ID to WBS ID
function getWBSIdForAgent(agentId: string): '1.3.1' | '1.3.2' | '1.4.1' {
  const mapping: Record<string, '1.3.1' | '1.3.2' | '1.4.1'> = {
    'bjorn-eriksen': '1.3.1',
    'kari-andersen': '1.3.2',
    'per-johansen': '1.4.1',
  };

  return mapping[agentId] || '1.3.1';
}
