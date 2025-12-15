/**
 * Agent Status API Client
 * Handles agent timeout/lock status tracking
 */

import { createClient } from '@/lib/supabase/client';
import type { AgentStatus, AgentStatusResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get lock status for all agents in a session
 */
export async function getAgentStatus(sessionId: string): Promise<AgentStatusResponse> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}/agent-status`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke hente agentstatus.'
    );
  }

  const data: AgentStatusResponse = await response.json();
  return data;
}

/**
 * Check if a specific agent is locked
 */
export async function isAgentLocked(
  sessionId: string,
  agentId: string
): Promise<AgentStatus | null> {
  const statuses = await getAgentStatus(sessionId);
  const agentStatus = statuses[agentId];

  return agentStatus?.is_locked ? agentStatus : null;
}

/**
 * Calculate minutes remaining until unlock
 */
export function calculateMinutesRemaining(unlockAt: string): number {
  const now = new Date();
  const unlock = new Date(unlockAt);
  const diff = unlock.getTime() - now.getTime();

  if (diff <= 0) return 0;

  return Math.ceil(diff / 60000); // Convert to minutes
}

/**
 * Calculate seconds remaining until unlock
 */
export function calculateSecondsRemaining(unlockAt: string): number {
  const now = new Date();
  const unlock = new Date(unlockAt);
  const diff = unlock.getTime() - now.getTime();

  if (diff <= 0) return 0;

  return Math.ceil(diff / 1000); // Convert to seconds
}

/**
 * Format time remaining as MM:SS
 */
export function formatTimeRemaining(unlockAt: string): string {
  const now = new Date();
  const unlock = new Date(unlockAt);
  const diff = unlock.getTime() - now.getTime();

  if (diff <= 0) return '00:00';

  const minutes = Math.floor(diff / 60000);
  const seconds = Math.floor((diff % 60000) / 1000);

  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/**
 * Get agent name from agent ID
 */
export function getAgentName(agentId: string): string {
  const names: Record<string, string> = {
    'anne-lise-berg': 'Anne-Lise Berg',
    'bjorn-eriksen': 'Bjørn Eriksen',
    'kari-andersen': 'Kari Andersen',
    'per-johansen': 'Per Johansen',
  };

  return names[agentId] || agentId;
}

/**
 * Get agent role description
 */
export function getAgentRole(agentId: string): string {
  const roles: Record<string, string> = {
    'anne-lise-berg': 'Prosjekteier (Kommune)',
    'bjorn-eriksen': 'Leverandør 1: Grunnarbeid (WBS 1.3.1)',
    'kari-andersen': 'Leverandør 2: Fundamentering (WBS 1.3.2)',
    'per-johansen': 'Leverandør 3: Råbygg (WBS 1.4.1)',
  };

  return roles[agentId] || 'Ukjent rolle';
}

/**
 * Get agent initials for avatar
 */
export function getAgentInitials(agentId: string): string {
  const initials: Record<string, string> = {
    'anne-lise-berg': 'AB',
    'bjorn-eriksen': 'BE',
    'kari-andersen': 'KA',
    'per-johansen': 'PJ',
  };

  return initials[agentId] || '??';
}

/**
 * Get agent color for UI elements
 */
export function getAgentColor(agentId: string): string {
  if (agentId === 'anne-lise-berg') {
    return '#f59e0b'; // Yellow/orange for owner
  }

  return '#3b82f6'; // Blue for suppliers
}
