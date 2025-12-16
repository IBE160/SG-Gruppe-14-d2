/**
 * TypeScript Types for PM Simulator
 * Based on database schema and API specifications
 */

// ============================================
// DATABASE TYPES
// ============================================

export interface GameSession {
  id: string;
  user_id: string;

  // 3-tier budget model
  total_budget: number;                // 700 MNOK
  locked_budget: number;               // 390 MNOK
  available_budget: number;            // 310 MNOK
  current_budget_used: number;         // 0-310 MNOK

  // Computed fields
  budget_tier1_percentage?: number;    // (current_budget_used / available_budget) * 100
  budget_tier3_total?: number;         // locked_budget + current_budget_used
  budget_remaining?: number;           // available_budget - current_budget_used

  // Timeline (inflexible)
  deadline_date: string;               // "2026-05-15"
  projected_completion_date?: string | null;
  is_timeline_valid?: boolean;        // projected <= deadline

  // Status
  status: 'in_progress' | 'completed' | 'abandoned';
  negotiable_wbs_commitments: WBSCommitmentSummary[];

  created_at: string;
  updated_at: string;
}

export interface WBSCommitment {
  id: string;
  session_id: string;

  wbs_id: '1.3.1' | '1.3.2' | '1.4.1';
  wbs_name: string;
  agent_id: 'bjorn-eriksen' | 'kari-andersen' | 'per-johansen';

  // Costs
  baseline_cost: number;               // Original estimate
  negotiated_cost: number;             // Final negotiated
  committed_cost: number;              // What user committed to

  // Computed
  savings?: number;                    // baseline - committed
  savings_percentage?: number;         // (savings / baseline) * 100

  // Duration
  baseline_duration: number;           // Original months
  negotiated_duration: number;         // Final months

  // Status
  status: 'committed' | 'rejected';
  committed_at: string;

  // Additional metadata
  quality_level?: 'standard' | 'budget' | 'premium';
  notes?: string;
}

export interface WBSCommitmentSummary {
  wbs_id: string;
  wbs_name: string;
  agent_id: string;
  committed_cost: number;
  committed_duration: number;
  committed_at: string;
}

export interface NegotiationMessage {
  id: string;
  session_id: string;

  agent_id: string;
  agent_name: string;
  agent_type: 'owner' | 'supplier';

  user_message: string;
  agent_response: string;

  // Timeout mechanic
  is_disagreement: boolean;
  disagreement_reason?: string;

  // Offer tracking
  contains_offer: boolean;
  offer_data?: OfferData;

  timestamp: string;
}

export interface OfferData {
  wbs_id: string;
  cost: number;
  duration: number;
  quality_level?: string;
  conditions?: string[];
}

export interface AgentTimeout {
  id: string;
  session_id: string;
  agent_id: string;

  locked_at: string;
  unlock_at: string;
  lock_duration_minutes: number;

  agent_message: string;               // Agent's goodbye message
  trigger_reason?: string;
  disagreement_count: number;

  is_active: boolean;
  unlocked_at?: string;
}

export interface UserAnalytics {
  id: string;
  user_id: string;

  total_sessions: number;
  completed_sessions: number;
  total_budget_saved: number;
  average_savings_percentage: number;
  best_savings_percentage: number;

  created_at: string;
  updated_at: string;
}

// ============================================
// API REQUEST/RESPONSE TYPES
// ============================================

export interface ChatRequest {
  session_id: string;
  agent_id: string;
  message: string;
  conversation_history: ConversationMessage[];
  game_context?: GameContext;
}

export interface ChatResponse {
  agent_id: string;
  agent_name: string;
  response: string;
  timestamp: string;
  is_disagreement: boolean;
  contains_offer?: boolean;
  offer_data?: OfferData;
}

export interface ConversationMessage {
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  is_disagreement?: boolean;
}

export interface GameContext {
  total_budget: number;
  current_budget_used: number;
  available_budget: number;
  locked_budget: number;
  deadline_date: string;
  committed_wbs: WBSCommitmentSummary[];
}

export interface CreateSessionRequest {
  total_budget?: number;               // Defaults to 700 MNOK
  deadline_date?: string;              // Defaults to "2026-05-15"
}

export interface CreateSessionResponse {
  session: GameSession;
}

export interface GetSessionResponse {
  session: GameSession;
  commitments: WBSCommitment[];
  message_count: number;
  last_activity: string;
}

export interface UpdateSessionRequest {
  status?: 'in_progress' | 'completed' | 'abandoned';
  projected_completion_date?: string;
  game_state?: Record<string, any>;
}

export interface CreateCommitmentRequest {
  wbs_id: '1.3.1' | '1.3.2' | '1.4.1';
  wbs_name: string;
  agent_id: string;
  baseline_cost: number;
  negotiated_cost: number;
  committed_cost: number;
  baseline_duration: number;
  negotiated_duration: number;
  quality_level?: 'standard' | 'budget' | 'premium';
  notes?: string;
}

export interface CreateCommitmentResponse {
  commitment: WBSCommitment;
  updated_session: GameSession;
}

export interface AgentStatus {
  is_locked: boolean;
  disagreement_count: number;
  disagreements_until_timeout: number;
  unlock_at: string | null;
  last_message: string | null;
  minutes_remaining?: number;
}

export interface AgentStatusResponse {
  [agent_id: string]: AgentStatus;
}

// ============================================
// UI/COMPONENT TYPES
// ============================================

export interface Agent {
  id: 'anne-lise-berg' | 'bjorn-eriksen' | 'kari-andersen' | 'per-johansen';
  name: string;
  role: string;
  type: 'owner' | 'supplier';
  avatar: string;                      // Initials for avatar
  color: string;                       // Badge color
  capabilities: string[];
  restrictions: string[];
}

export interface WBSItem {
  id: '1.3.1' | '1.3.2' | '1.4.1';
  name: string;
  agent_id: string;
  agent_name: string;
  baseline_cost: number;
  baseline_duration: number;
  is_negotiable: boolean;
  is_critical_path: boolean;
  status: 'pending' | 'in_progress' | 'committed' | 'rejected';
  committed_cost?: number;
  committed_duration?: number;
}

export interface BudgetTier {
  label: string;
  used: number;
  total: number;
  percentage: number;
  color: string;
  isOverBudget: boolean;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
  agent_name?: string;
  is_disagreement?: boolean;
  contains_offer?: boolean;
  offer_data?: OfferData;
}

export interface BudgetImpact {
  tier1_used_before: number;
  tier1_used_after: number;
  tier1_percentage_after: number;
  tier3_total_after: number;
  budget_remaining_after: number;
  is_valid: boolean;
  exceeds_budget: boolean;
}

// ============================================
// CONSTANTS
// ============================================

export const AGENT_IDS = {
  OWNER: 'anne-lise-berg',
  SUPPLIER_1: 'bjorn-eriksen',
  SUPPLIER_2: 'kari-andersen',
  SUPPLIER_3: 'per-johansen',
} as const;

export const WBS_IDS = {
  SITE_PREP: '1.3.1',
  FOUNDATION: '1.3.2',
  STRUCTURAL: '1.4.1',
} as const;

export const BASELINE_ESTIMATES = {
  '1.3.1': { cost: 105_000_000, duration: 3.5, name: 'Grunnarbeid' },
  '1.3.2': { cost: 60_000_000, duration: 2.5, name: 'Fundamentering' },
  '1.4.1': { cost: 180_000_000, duration: 4.0, name: 'Råbygg' },
} as const;

export const BUDGET_CONSTANTS = {
  TOTAL: 700_000_000,                  // 700 MNOK
  LOCKED: 390_000_000,                 // 390 MNOK
  AVAILABLE: 310_000_000,              // 310 MNOK
  BASELINE_TOTAL: 345_000_000,         // 345 MNOK (sum of 3 negotiable)
  REQUIRED_SAVINGS: 35_000_000,        // 35 MNOK (deficit)
} as const;

export const DEADLINE = '2026-05-15' as const;

export const TIMEOUT_SETTINGS = {
  DISAGREEMENT_THRESHOLD: 6,           // Timeout after 6 disagreements
  LOCK_DURATION_MINUTES: 10,           // 10 minutes
} as const;

// ============================================
// HELPER TYPE GUARDS
// ============================================

export function isSupplierAgent(agentId: string): boolean {
  return ['bjorn-eriksen', 'kari-andersen', 'per-johansen'].includes(agentId);
}

export function isOwnerAgent(agentId: string): boolean {
  return agentId === 'anne-lise-berg';
}

export function isValidWBSId(wbsId: string): wbsId is '1.3.1' | '1.3.2' | '1.4.1' {
  return ['1.3.1', '1.3.2', '1.4.1'].includes(wbsId);
}
