-- =====================================================
-- PM SIMULATOR - SUPABASE-FRIENDLY SCHEMA
-- Simplified import for Supabase SQL Editor
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLE 1: GAME SESSIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Budget (3-tier model)
    total_budget NUMERIC(12, 2) NOT NULL DEFAULT 700000000.00,
    locked_budget NUMERIC(12, 2) NOT NULL DEFAULT 390000000.00,
    available_budget NUMERIC(12, 2) NOT NULL DEFAULT 310000000.00,
    current_budget_used NUMERIC(12, 2) NOT NULL DEFAULT 0.00,

    -- Computed budget columns
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

    -- Timeline
    deadline_date DATE NOT NULL DEFAULT '2026-05-15',
    projected_completion_date DATE,
    is_timeline_valid BOOLEAN GENERATED ALWAYS AS
        (projected_completion_date IS NULL OR projected_completion_date <= '2026-05-15') STORED,

    -- Game state
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    game_state JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    CONSTRAINT budget_not_exceeded CHECK (current_budget_used <= available_budget),
    CONSTRAINT total_budget_valid CHECK ((locked_budget + current_budget_used) <= total_budget)
);

-- =====================================================
-- TABLE 2: WBS COMMITMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.wbs_commitments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    -- WBS identification
    wbs_id VARCHAR(10) NOT NULL,
    wbs_name VARCHAR(200),

    -- Commitment details
    committed_price NUMERIC(12, 2) NOT NULL,
    committed_duration_weeks INTEGER NOT NULL,

    -- Baseline for comparison
    baseline_price NUMERIC(12, 2) NOT NULL,
    baseline_duration_weeks INTEGER NOT NULL,

    -- Computed savings
    savings NUMERIC(12, 2) GENERATED ALWAYS AS
        (baseline_price - committed_price) STORED,

    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN baseline_price > 0
         THEN ((baseline_price - committed_price) / baseline_price) * 100
         ELSE 0 END) STORED,

    -- Negotiated changes
    negotiated_scope TEXT,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_wbs_id CHECK (wbs_id IN ('1.3.1', '1.3.2', '1.4.1')),
    CONSTRAINT unique_wbs_per_session UNIQUE (session_id, wbs_id),
    CONSTRAINT positive_price CHECK (committed_price >= 0),
    CONSTRAINT positive_duration CHECK (committed_duration_weeks > 0)
);

-- =====================================================
-- TABLE 3: NEGOTIATION HISTORY
-- =====================================================

CREATE TABLE IF NOT EXISTS public.negotiation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    -- Agent identification
    agent_id VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100),
    agent_type VARCHAR(20) NOT NULL,

    -- Message content
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,

    -- Disagreement tracking
    is_disagreement BOOLEAN DEFAULT FALSE,
    disagreement_reason TEXT,

    -- Context snapshot
    context_snapshot JSONB DEFAULT '{}',

    -- Timestamp
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_agent_type CHECK (agent_type IN ('owner', 'supplier'))
);

-- =====================================================
-- TABLE 4: AGENT TIMEOUTS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.agent_timeouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,

    -- Timeout details
    locked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    unlock_at TIMESTAMP WITH TIME ZONE NOT NULL,
    lock_duration_minutes INTEGER NOT NULL DEFAULT 10,

    -- Reason
    agent_message TEXT NOT NULL,
    trigger_reason VARCHAR(100),
    disagreement_count INTEGER NOT NULL,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    unlocked_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLE 5: USER ANALYTICS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Statistics
    total_sessions INTEGER DEFAULT 0,
    completed_sessions INTEGER DEFAULT 0,
    total_savings NUMERIC(12, 2) DEFAULT 0,
    average_savings_percentage NUMERIC(5, 2) DEFAULT 0,
    best_savings_percentage NUMERIC(5, 2) DEFAULT 0,

    -- Performance metrics
    total_negotiations INTEGER DEFAULT 0,
    successful_negotiations INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Constraints
    CONSTRAINT unique_user_analytics UNIQUE (user_id)
);

-- =====================================================
-- INDEXES
-- =====================================================

-- Game sessions indexes
CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_game_sessions_status ON public.game_sessions(status);
CREATE INDEX IF NOT EXISTS idx_game_sessions_created_at ON public.game_sessions(created_at DESC);

-- WBS commitments indexes
CREATE INDEX IF NOT EXISTS idx_wbs_commitments_session_id ON public.wbs_commitments(session_id);
CREATE INDEX IF NOT EXISTS idx_wbs_commitments_wbs_id ON public.wbs_commitments(wbs_id);

-- Negotiation history indexes
CREATE INDEX IF NOT EXISTS idx_negotiation_history_session_id ON public.negotiation_history(session_id);
CREATE INDEX IF NOT EXISTS idx_negotiation_history_agent_id ON public.negotiation_history(agent_id);
CREATE INDEX IF NOT EXISTS idx_negotiation_history_timestamp ON public.negotiation_history(timestamp DESC);

-- Agent timeouts indexes
CREATE INDEX IF NOT EXISTS idx_agent_timeouts_session_agent ON public.agent_timeouts(session_id, agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_timeouts_active ON public.agent_timeouts(is_active, unlock_at);

-- User analytics indexes
CREATE INDEX IF NOT EXISTS idx_user_analytics_user_id ON public.user_analytics(user_id);

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.wbs_commitments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.negotiation_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_timeouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;

-- RLS Policies for game_sessions
CREATE POLICY "Users can view their own sessions"
    ON public.game_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own sessions"
    ON public.game_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions"
    ON public.game_sessions FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own sessions"
    ON public.game_sessions FOR DELETE
    USING (auth.uid() = user_id);

-- RLS Policies for wbs_commitments
CREATE POLICY "Users can view commitments for their sessions"
    ON public.wbs_commitments FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = wbs_commitments.session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can insert commitments for their sessions"
    ON public.wbs_commitments FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = session_id
        AND game_sessions.user_id = auth.uid()
    ));

-- RLS Policies for negotiation_history
CREATE POLICY "Users can view their negotiation history"
    ON public.negotiation_history FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = negotiation_history.session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can insert their negotiation history"
    ON public.negotiation_history FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = session_id
        AND game_sessions.user_id = auth.uid()
    ));

-- RLS Policies for agent_timeouts
CREATE POLICY "Users can view timeouts for their sessions"
    ON public.agent_timeouts FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = agent_timeouts.session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can insert timeouts for their sessions"
    ON public.agent_timeouts FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = session_id
        AND game_sessions.user_id = auth.uid()
    ));

CREATE POLICY "Users can update timeouts for their sessions"
    ON public.agent_timeouts FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM public.game_sessions
        WHERE game_sessions.id = agent_timeouts.session_id
        AND game_sessions.user_id = auth.uid()
    ));

-- RLS Policies for user_analytics
CREATE POLICY "Users can view their own analytics"
    ON public.user_analytics FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own analytics"
    ON public.user_analytics FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own analytics"
    ON public.user_analytics FOR UPDATE
    USING (auth.uid() = user_id);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for game_sessions
DROP TRIGGER IF EXISTS update_game_sessions_updated_at ON public.game_sessions;
CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON public.game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for user_analytics
DROP TRIGGER IF EXISTS update_user_analytics_updated_at ON public.user_analytics;
CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- HELPER VIEWS
-- =====================================================

-- Active sessions view
CREATE OR REPLACE VIEW active_sessions_summary AS
SELECT
    gs.id,
    gs.user_id,
    gs.status,
    gs.current_budget_used,
    gs.budget_tier1_percentage,
    gs.budget_remaining,
    COUNT(DISTINCT wc.id) as commitments_count,
    COUNT(DISTINCT nh.id) as negotiation_messages_count,
    gs.created_at,
    gs.updated_at
FROM public.game_sessions gs
LEFT JOIN public.wbs_commitments wc ON wc.session_id = gs.id
LEFT JOIN public.negotiation_history nh ON nh.session_id = gs.id
WHERE gs.status = 'in_progress'
GROUP BY gs.id;

-- Leaderboard view
CREATE OR REPLACE VIEW leaderboard AS
SELECT
    ua.user_id,
    ua.total_sessions,
    ua.completed_sessions,
    ua.total_savings,
    ua.average_savings_percentage,
    ua.best_savings_percentage,
    RANK() OVER (ORDER BY ua.average_savings_percentage DESC) as rank
FROM public.user_analytics ua
WHERE ua.completed_sessions > 0
ORDER BY ua.average_savings_percentage DESC;

-- =====================================================
-- COMPLETE!
-- =====================================================
