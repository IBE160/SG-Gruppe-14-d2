/**
 * Chat API Client
 * Handles all communication with backend chat endpoints
 */

import { createClient } from '@/lib/supabase/client';
import type {
  ChatRequest,
  ChatResponse,
  ConversationMessage,
  GameContext,
  NegotiationMessage, // Import NegotiationMessage
  ChatMessage // Import ChatMessage from UI/COMPONENT TYPES
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Send a chat message to an AI agent
 */
export async function sendChatMessage(
  sessionId: string,
  agentId: string,
  message: string,
  conversationHistory: ChatMessage[], // Changed to ChatMessage[]
  gameContext?: GameContext
): Promise<ChatResponse> {
  const supabase = createClient();

  // Get JWT token from Supabase session
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const request: ChatRequest = {
    session_id: sessionId,
    agent_id: agentId,
    message,
    conversation_history: conversationHistory.map(msg => ({ // Map ChatMessage to ConversationMessage for backend
      role: msg.role === 'user' ? 'user' : 'agent', // Explicitly set role as 'user' or 'agent'
      content: msg.content,
      // The backend ConversationMessage expects only role and content, not id, timestamp, etc.
      // So we only send what's expected.
    })),
    game_context: gameContext,
  };

  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    // Handle 423 Locked status (agent timeout)
    if (response.status === 423) {
      const errorData = await response.json();
      throw {
        code: 'AGENT_LOCKED',
        message: errorData.message || 'Agenten er ikke tilgjengelig nå.',
        unlock_at: errorData.unlock_at,
        minutes_remaining: errorData.minutes_remaining,
        last_message: errorData.last_message,
      };
    }

    // Handle other errors
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke sende melding til agenten.'
    );
  }

  const data: ChatResponse = await response.json();
  return data;
}

/**
 * Get negotiation history for a session and agent
 */
export async function getNegotiationHistory(
  sessionId: string,
  agentId?: string
): Promise<ChatMessage[]> { // Return ChatMessage[]
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const url = new URL(`${API_URL}/api/sessions/${sessionId}/history`);
  if (agentId) {
    url.searchParams.append('agent_id', agentId);
  }

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke hente samtalehistorikk.'
    );
  }

  // Backend now returns List<NegotiationMessage>
  const rawHistory: NegotiationMessage[] = await response.json();

  const formattedHistory: ChatMessage[] = [];
  rawHistory.forEach((record) => {
    // User message
    formattedHistory.push({
      id: `${record.id}-user`, // Unique ID for frontend
      role: 'user',
      content: record.user_message,
      timestamp: record.timestamp,
    });

    // Agent response
    formattedHistory.push({
      id: `${record.id}-agent`, // Unique ID for frontend
      role: 'agent',
      content: record.agent_response,
      timestamp: record.timestamp, // Use the same timestamp for agent response
      agent_name: record.agent_name,
      is_disagreement: record.is_disagreement,
      contains_offer: record.contains_offer,
      offer_data: record.offer_data,
    });
  });

  // Sort chronologically
  formattedHistory.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  return formattedHistory;
}

/**
 * Parse AI response for offer detection
 * Looks for cost and duration patterns in Norwegian text
 */
export function parseOfferFromResponse(response: string): {
  containsOffer: boolean;
  cost?: number;
  duration?: number;
  qualityLevel?: string;
} {
  // Look for cost patterns: "55 MNOK", "55MNOK", "55 millioner"
  const costPatterns = [
    /(\d+)\s*MNOK/i,
    /(\d+)\s*millioner/i,
    /kr\s*(\d+)\s*millioner/i,
  ];

  let cost: number | undefined;
  for (const pattern of costPatterns) {
    const match = response.match(pattern);
    if (match) {
      cost = parseFloat(match[1]) * 1_000_000; // Convert to actual value
      break;
    }
  }

  // Look for duration patterns: "2.5 måneder", "2,5 mnd", "3 måneder"
  const durationPatterns = [
    /(\d+[.,]?\d*)\s*måneder/i,
    /(\d+[.,]?\d*)\s*mnd/i,
  ];

  let duration: number | undefined;
  for (const pattern of durationPatterns) {
    const match = response.match(pattern);
    if (match) {
      duration = parseFloat(match[1].replace(',', '.'));
      break;
    }
  }

  // Look for quality indicators
  let qualityLevel: string | undefined;
  if (response.match(/standard/i)) {
    qualityLevel = 'standard';
  } else if (response.match(/budsjett/i) || response.match(/enklere/i)) {
    qualityLevel = 'budget';
  } else if (response.match(/premium/i) || response.match(/høy kvalitet/i)) {
    qualityLevel = 'premium';
  }

  return {
    containsOffer: cost !== undefined && duration !== undefined,
    cost,
    duration,
    qualityLevel,
  };
}

/**
 * Format cost in Norwegian format
 * Example: 55000000 -> "55 MNOK"
 */
export function formatCost(amount: number): string {
  const millions = amount / 1_000_000;
  return `${millions.toFixed(0)} MNOK`;
}

/**
 * Format duration in Norwegian
 * Example: 2.5 -> "2,5 måneder"
 */
export function formatDuration(months: number): string {
  const formatted = months.toString().replace('.', ',');
  return `${formatted} måneder`;
}
