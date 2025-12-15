/**
 * Sessions API Client
 * Handles game session management
 */

import { createClient } from '@/lib/supabase/client';
import type {
  GameSession,
  CreateSessionRequest,
  CreateSessionResponse,
  GetSessionResponse,
  UpdateSessionRequest,
  CreateCommitmentRequest,
  CreateCommitmentResponse,
  WBSCommitment,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Create a new game session
 */
export async function createSession(
  request?: CreateSessionRequest
): Promise<GameSession> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify(request || {}),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke opprette økt.'
    );
  }

  const data: CreateSessionResponse = await response.json();
  return data.session;
}

/**
 * Get session by ID with all related data
 */
export async function getSession(sessionId: string): Promise<GetSessionResponse> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Økten ble ikke funnet.');
    }

    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke hente økt.'
    );
  }

  const data: GetSessionResponse = await response.json();
  return data;
}

/**
 * Update session
 */
export async function updateSession(
  sessionId: string,
  updates: UpdateSessionRequest
): Promise<GameSession> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke oppdatere økt.'
    );
  }

  const data = await response.json();
  return data.session;
}

/**
 * Create a WBS commitment
 */
export async function createCommitment(
  sessionId: string,
  commitment: CreateCommitmentRequest
): Promise<CreateCommitmentResponse> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}/commitments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${session.access_token}`,
    },
    body: JSON.stringify(commitment),
  });

  if (!response.ok) {
    // Handle budget exceeded error
    if (response.status === 400) {
      const errorData = await response.json().catch(() => ({}));
      if (errorData.detail?.includes('budsjett')) {
        throw {
          code: 'BUDGET_EXCEEDED',
          message: errorData.detail,
        };
      }
    }

    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke opprette forpliktelse.'
    );
  }

  const data: CreateCommitmentResponse = await response.json();
  return data;
}

/**
 * Get all commitments for a session
 */
export async function getCommitments(sessionId: string): Promise<WBSCommitment[]> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}/commitments`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke hente forpliktelser.'
    );
  }

  const data = await response.json();
  return data.commitments || [];
}

/**
 * Complete the game session
 */
export async function completeSession(sessionId: string): Promise<{
  session: GameSession;
  validation: {
    is_valid: boolean;
    errors: string[];
    warnings: string[];
    stats: Record<string, any>;
  };
}> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions/${sessionId}/complete`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke fullføre økten.'
    );
  }

  const data = await response.json();
  return data;
}

/**
 * Get all sessions for current user
 */
export async function getUserSessions(): Promise<GameSession[]> {
  const supabase = createClient();

  // Get JWT token
  const {
    data: { session },
    error: authError,
  } = await supabase.auth.getSession();

  if (authError || !session) {
    throw new Error('Ikke autentisert. Vennligst logg inn igjen.');
  }

  const response = await fetch(`${API_URL}/api/sessions`, {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${session.access_token}`,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || errorData.message || 'Kunne ikke hente økter.'
    );
  }

  const data = await response.json();
  return data.sessions || [];
}
