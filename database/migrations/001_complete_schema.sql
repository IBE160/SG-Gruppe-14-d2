-- =====================================================
-- PM SIMULATOR - COMPLETE DATABASE SCHEMA v3.0
-- Nye Hædda Barneskole
-- Based on UX Mockups + Functional Flows
-- Date: December 14, 2025
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. GAME SESSIONS TABLE
-- Core table for tracking user game sessions
-- Implements 3-tier budget model: Tilgjengelig | Låst | Totalt
-- =====================================================

CREATE TABLE public.game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Budget tracking (3-tier model)
    total_budget NUMERIC(12, 2) NOT NULL DEFAULT 700000000.00,        -- 700 MNOK (constant)
    locked_budget NUMERIC(12, 2) NOT NULL DEFAULT 390000000.00,       -- 390 MNOK (12 locked packages)
    available_budget NUMERIC(12, 2) NOT NULL DEFAULT 310000000.00,    -- 310 MNOK (3 negotiable)
    current_budget_used NUMERIC(12, 2) NOT NULL DEFAULT 0.00,         -- From 3 negotiable packages

    -- Budget computed columns (auto-calculated)
    budget_tier1_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN available_budget > 0
         THEN (current_budget_used / available_budget) * 100
         ELSE 0 END) STORED,

    budget_tier3_total NUMERIC(12, 2) GENERATED ALWAYS AS
        (locked_budget + current_budget_used) STORED,

    budget_tier3_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN total_budget > 0
         THEN ((locked_budget + current_budget_used) / total_budget) * 100
         ELSE 0 END) STORED,

    budget_remaining NUMERIC(12, 2) GENERATED ALWAYS AS
        (available_budget - current_budget_used) STORED,

    -- Timeline tracking
    deadline_date DATE NOT NULL DEFAULT '2026-05-15',                 -- INFLEXIBLE deadline
    projected_completion_date DATE,                                   -- Based on WBS durations
    is_timeline_valid BOOLEAN GENERATED ALWAYS AS
        (projected_completion_date IS NULL OR projected_completion_date <= '2026-05-15') STORED,

    -- Game state
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('in_progress', 'completed', 'failed', 'paused', 'abandoned')),

    -- WBS commitments tracking (3 negotiable items only)
    -- Stores which WBS packages have been committed
    negotiable_wbs_commitments JSONB DEFAULT '[]'::jsonb,
    -- Example structure:
    -- [
    --   {"wbs_id": "1.3.1", "supplier_id": "bjorn-eriksen", "cost": 95000000, "duration": 3, "committed_at": "2025-12-14T10:00:00Z"},
    --   {"wbs_id": "1.3.2", "supplier_id": "kari-andersen", "cost": 55000000, "duration": 2.5, "committed_at": "2025-12-14T11:00:00Z"}
    -- ]

    -- Game metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Performance tracking
    duration_seconds INTEGER GENERATED ALWAYS AS
        (EXTRACT(EPOCH FROM (COALESCE(completed_at, NOW()) - started_at))::INTEGER) STORED,

    -- Constraints
    CONSTRAINT valid_budget_usage CHECK (current_budget_used >= 0),
    CONSTRAINT budget_within_available CHECK (current_budget_used <= available_budget),
    CONSTRAINT total_budget_valid CHECK ((locked_budget + current_budget_used) <= total_budget)
);

-- Indexes for performance
CREATE INDEX idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX idx_game_sessions_status ON public.game_sessions(status);
CREATE INDEX idx_game_sessions_created_at ON public.game_sessions(created_at DESC);

-- Row Level Security (RLS)
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;

-- Users can only see their own sessions
CREATE POLICY "Users can view their own sessions"
    ON public.game_sessions FOR SELECT
    USING (auth.uid() = user_id);

-- Users can create sessions for themselves
CREATE POLICY "Users can create their own sessions"
    ON public.game_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own sessions
CREATE POLICY "Users can update their own sessions"
    ON public.game_sessions FOR UPDATE
    USING (auth.uid() = user_id);

-- Users can delete their own sessions
CREATE POLICY "Users can delete their own sessions"
    ON public.game_sessions FOR DELETE
    USING (auth.uid() = user_id);

-- =====================================================
-- 2. WBS COMMITMENTS TABLE
-- Tracks commitments to the 3 negotiable WBS packages
-- Each commitment represents an accepted offer from a supplier
-- =====================================================

CREATE TABLE public.wbs_commitments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    -- WBS identification (only 3 negotiable items)
    wbs_id VARCHAR(50) NOT NULL,           -- "1.3.1" | "1.3.2" | "1.4.1"
    wbs_name VARCHAR(200) NOT NULL,        -- "Grunnarbeid" | "Fundamentering" | "Råbygg"
    wbs_category VARCHAR(100) NOT NULL,    -- Category for grouping

    -- Supplier/Agent information
    agent_id VARCHAR(50) NOT NULL,         -- "bjorn-eriksen" | "kari-andersen" | "per-johansen"
    agent_name VARCHAR(100) NOT NULL,      -- "Bjørn Eriksen" | etc.

    -- Pricing information (all in NOK)
    baseline_cost NUMERIC(12, 2) NOT NULL,        -- Original estimate (105M | 60M | 180M)
    negotiated_cost NUMERIC(12, 2) NOT NULL,      -- Final negotiated price
    committed_cost NUMERIC(12, 2) NOT NULL,       -- Same as negotiated (for consistency)

    -- Computed savings
    savings NUMERIC(12, 2) GENERATED ALWAYS AS
        (baseline_cost - committed_cost) STORED,
    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN baseline_cost > 0
         THEN ((baseline_cost - committed_cost) / baseline_cost * 100)
         ELSE 0 END) STORED,

    -- Duration information (in months)
    baseline_duration NUMERIC(3, 1) NOT NULL,     -- Original estimate (3.5 | 2.5 | 4.0 months)
    negotiated_duration NUMERIC(3, 1) NOT NULL,   -- Final negotiated duration
    committed_duration NUMERIC(3, 1) NOT NULL,    -- Same as negotiated

    -- Status tracking
    status VARCHAR(20) NOT NULL DEFAULT 'committed'
        CHECK (status IN ('pending', 'committed', 'rejected', 'renegotiating')),

    -- Additional metadata
    user_reasoning TEXT,                   -- Why user accepted this offer
    quality_level VARCHAR(50),             -- "standard" | "budget" | "premium"
    scope_changes TEXT,                    -- Any scope modifications

    -- Timestamps
    committed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT positive_costs CHECK (
        baseline_cost >= 0 AND
        negotiated_cost >= 0 AND
        committed_cost >= 0
    ),
    CONSTRAINT positive_durations CHECK (
        baseline_duration > 0 AND
        negotiated_duration > 0 AND
        committed_duration > 0
    ),
    CONSTRAINT valid_wbs_id CHECK (
        wbs_id IN ('1.3.1', '1.3.2', '1.4.1')
    ),
    CONSTRAINT valid_agent_id CHECK (
        agent_id IN ('bjorn-eriksen', 'kari-andersen', 'per-johansen')
    ),
    -- Only one commitment per WBS per session
    CONSTRAINT unique_wbs_per_session UNIQUE (session_id, wbs_id)
);

-- Indexes
CREATE INDEX idx_wbs_commitments_session_id ON public.wbs_commitments(session_id);
CREATE INDEX idx_wbs_commitments_agent_id ON public.wbs_commitments(agent_id);
CREATE INDEX idx_wbs_commitments_wbs_id ON public.wbs_commitments(wbs_id);
CREATE INDEX idx_wbs_commitments_status ON public.wbs_commitments(status);

-- RLS Policies
ALTER TABLE public.wbs_commitments ENABLE ROW LEVEL SECURITY;

-- Users can view commitments for their own sessions
CREATE POLICY "Users can view commitments for their sessions"
    ON public.wbs_commitments FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = wbs_commitments.session_id
            AND user_id = auth.uid()
        )
    );

-- Users can create commitments for their sessions
CREATE POLICY "Users can create commitments for their sessions"
    ON public.wbs_commitments FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = wbs_commitments.session_id
            AND user_id = auth.uid()
        )
    );

-- Users can update commitments for their sessions
CREATE POLICY "Users can update commitments for their sessions"
    ON public.wbs_commitments FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = wbs_commitments.session_id
            AND user_id = auth.uid()
        )
    );

-- Users can delete commitments for their sessions
CREATE POLICY "Users can delete commitments for their sessions"
    ON public.wbs_commitments FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = wbs_commitments.session_id
            AND user_id = auth.uid()
        )
    );

-- =====================================================
-- 3. NEGOTIATION HISTORY TABLE
-- Logs all chat messages between user and AI agents
-- Used for history, analytics, and timeout mechanic
-- =====================================================

CREATE TABLE public.negotiation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    -- Agent information
    agent_id VARCHAR(50) NOT NULL,         -- "anne-lise-berg" | "bjorn-eriksen" | etc.
    agent_name VARCHAR(100) NOT NULL,      -- "Anne-Lise Berg" | etc.
    agent_type VARCHAR(20) NOT NULL        -- "owner" | "supplier"
        CHECK (agent_type IN ('owner', 'supplier')),

    -- Message content
    user_message TEXT NOT NULL,            -- User's message
    agent_response TEXT NOT NULL,          -- AI agent's response

    -- Disagreement tracking (for timeout mechanic)
    is_disagreement BOOLEAN DEFAULT FALSE, -- Was this a disagreement?
    disagreement_reason TEXT,              -- Why was it flagged as disagreement?
    -- Disagreement keywords: "dessverre", "det går ikke", "for lavt", "urealistisk", etc.

    -- Offer tracking (if response contains an offer)
    contains_offer BOOLEAN DEFAULT FALSE,
    offer_data JSONB,                      -- {cost, duration, quality, description}

    -- Context snapshot (game state at time of message)
    context_snapshot JSONB DEFAULT '{}'::jsonb,
    -- Example: {"budget_used": 55000000, "wbs_committed": ["1.3.2"], "round": 2}

    -- Metadata
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_ms INTEGER,              -- How long AI took to respond

    -- Sentiment (optional - for future analytics)
    sentiment VARCHAR(20) CHECK (sentiment IN ('positive', 'neutral', 'negative', NULL))
);

-- Indexes
CREATE INDEX idx_negotiation_history_session_id ON public.negotiation_history(session_id);
CREATE INDEX idx_negotiation_history_agent_id ON public.negotiation_history(agent_id);
CREATE INDEX idx_negotiation_history_timestamp ON public.negotiation_history(timestamp DESC);
CREATE INDEX idx_negotiation_history_disagreement ON public.negotiation_history(is_disagreement)
    WHERE is_disagreement = TRUE;

-- RLS Policies
ALTER TABLE public.negotiation_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view negotiation history for their sessions"
    ON public.negotiation_history FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = negotiation_history.session_id
            AND user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create negotiation history for their sessions"
    ON public.negotiation_history FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = negotiation_history.session_id
            AND user_id = auth.uid()
        )
    );

-- =====================================================
-- 4. AGENT TIMEOUTS TABLE
-- Tracks when agents are locked due to timeout mechanic
-- After 6 disagreements, agent locks for 10 minutes
-- =====================================================

CREATE TABLE public.agent_timeouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,         -- Which agent is locked

    -- Timeout details
    locked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    unlock_at TIMESTAMP WITH TIME ZONE NOT NULL,
    lock_duration_minutes INTEGER NOT NULL DEFAULT 10,

    -- Reason for timeout
    agent_message TEXT NOT NULL,           -- Agent's goodbye message
    trigger_reason VARCHAR(100),           -- "disagreement_threshold" | "unreasonable_demands"

    -- Disagreement count at time of timeout
    disagreement_count INTEGER NOT NULL,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,        -- Is timeout currently active?
    unlocked_at TIMESTAMP WITH TIME ZONE,  -- When was it actually unlocked?

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_lock_duration CHECK (lock_duration_minutes > 0),
    CONSTRAINT valid_disagreement_count CHECK (disagreement_count >= 0)
);

-- Indexes
CREATE INDEX idx_agent_timeouts_session_agent ON public.agent_timeouts(session_id, agent_id);
CREATE INDEX idx_agent_timeouts_active ON public.agent_timeouts(is_active, unlock_at)
    WHERE is_active = TRUE;
CREATE INDEX idx_agent_timeouts_unlock_at ON public.agent_timeouts(unlock_at);

-- RLS Policies
ALTER TABLE public.agent_timeouts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view timeouts for their sessions"
    ON public.agent_timeouts FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = agent_timeouts.session_id
            AND user_id = auth.uid()
        )
    );

-- =====================================================
-- 5. USER ANALYTICS TABLE (Optional - Future)
-- Aggregated statistics per user for leaderboards
-- =====================================================

CREATE TABLE public.user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Session statistics
    total_sessions INTEGER DEFAULT 0,
    completed_sessions INTEGER DEFAULT 0,
    failed_sessions INTEGER DEFAULT 0,

    -- Budget performance
    total_budget_saved NUMERIC(12, 2) DEFAULT 0.00,
    average_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,
    best_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,
    best_session_id UUID REFERENCES public.game_sessions(id) ON DELETE SET NULL,

    -- Time performance
    average_session_duration_seconds INTEGER DEFAULT 0,
    total_play_time_seconds INTEGER DEFAULT 0,
    fastest_completion_seconds INTEGER,

    -- Negotiation statistics
    total_negotiations INTEGER DEFAULT 0,
    average_negotiations_per_session NUMERIC(5, 2) DEFAULT 0.00,
    total_timeouts INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Unique constraint
    CONSTRAINT unique_user_analytics UNIQUE (user_id)
);

-- Index
CREATE INDEX idx_user_analytics_user_id ON public.user_analytics(user_id);
CREATE INDEX idx_user_analytics_best_savings ON public.user_analytics(best_savings_percentage DESC);

-- RLS
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own analytics"
    ON public.user_analytics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own analytics"
    ON public.user_analytics FOR ALL
    USING (auth.uid() = user_id);

-- =====================================================
-- 6. FUNCTIONS & TRIGGERS
-- =====================================================

-- Function: Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update game_sessions.updated_at
CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON public.game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Update wbs_commitments.updated_at
CREATE TRIGGER update_wbs_commitments_updated_at
    BEFORE UPDATE ON public.wbs_commitments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger: Update user_analytics.updated_at
CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Auto-unlock expired timeouts
CREATE OR REPLACE FUNCTION auto_unlock_expired_timeouts()
RETURNS void AS $$
BEGIN
    UPDATE public.agent_timeouts
    SET is_active = FALSE,
        unlocked_at = NOW()
    WHERE is_active = TRUE
    AND unlock_at <= NOW();
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 7. HELPER VIEWS (Optional - for easier queries)
-- =====================================================

-- View: Active game sessions with budget summary
CREATE OR REPLACE VIEW active_sessions_summary AS
SELECT
    gs.id,
    gs.user_id,
    gs.status,
    gs.current_budget_used,
    gs.budget_remaining,
    gs.budget_tier1_percentage,
    gs.budget_tier3_percentage,
    gs.projected_completion_date,
    gs.is_timeline_valid,
    COUNT(wc.id) AS committed_wbs_count,
    gs.created_at,
    gs.duration_seconds
FROM public.game_sessions gs
LEFT JOIN public.wbs_commitments wc ON gs.id = wc.session_id AND wc.status = 'committed'
WHERE gs.status = 'in_progress'
GROUP BY gs.id;

-- View: Leaderboard (best savings)
CREATE OR REPLACE VIEW leaderboard AS
SELECT
    ua.user_id,
    u.email,
    ua.best_savings_percentage,
    ua.completed_sessions,
    ua.average_session_duration_seconds,
    ua.total_budget_saved,
    ua.updated_at
FROM public.user_analytics ua
JOIN auth.users u ON ua.user_id = u.id
WHERE ua.completed_sessions > 0
ORDER BY ua.best_savings_percentage DESC
LIMIT 100;

-- =====================================================
-- 8. INITIAL DATA / SEED DATA
-- =====================================================

-- Note: WBS data (15 items) and Agent data (4 agents) will be stored
-- in the frontend as constants since they don't change

-- WBS 1.3.1 Grunnarbeid - 105 MNOK baseline, 3.5 months, Bjørn Eriksen
-- WBS 1.3.2 Fundamentering - 60 MNOK baseline, 2.5 months, Kari Andersen
-- WBS 1.4.1 Råbygg - 180 MNOK baseline, 4.0 months, Per Johansen
-- + 12 locked items totaling 390 MNOK

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================

-- Verify tables created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'game_sessions',
    'wbs_commitments',
    'negotiation_history',
    'agent_timeouts',
    'user_analytics'
)
ORDER BY table_name;

-- Expected output:
-- agent_timeouts
-- game_sessions
-- negotiation_history
-- user_analytics
-- wbs_commitments
