-- =====================================================
-- PM SIMULATOR - COMPLETE DATABASE SCHEMA v3.2 - CORRECTED
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. GAME SESSIONS TABLE
-- =====================================================

CREATE TABLE public.game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    total_budget NUMERIC(12, 2) NOT NULL DEFAULT 700000000.00,
    locked_budget NUMERIC(12, 2) NOT NULL DEFAULT 390000000.00,
    available_budget NUMERIC(12, 2) NOT NULL DEFAULT 310000000.00,
    current_budget_used NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
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
    deadline_date DATE NOT NULL DEFAULT '2026-05-15',
    projected_completion_date DATE,
    is_timeline_valid BOOLEAN GENERATED ALWAYS AS
        (projected_completion_date IS NULL OR projected_completion_date <= '2026-05-15') STORED,
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('in_progress', 'completed', 'failed', 'paused', 'abandoned')),
    negotiable_wbs_commitments JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT valid_budget_usage CHECK (current_budget_used >= 0),
    CONSTRAINT budget_within_available CHECK (current_budget_used <= available_budget),
    CONSTRAINT total_budget_valid CHECK ((locked_budget + current_budget_used) <= total_budget)
);

-- Indexes and RLS for game_sessions
CREATE INDEX idx_game_sessions_user_id ON public.game_sessions(user_id);
CREATE INDEX idx_game_sessions_status ON public.game_sessions(status);
CREATE INDEX idx_game_sessions_created_at ON public.game_sessions(created_at DESC);
ALTER TABLE public.game_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view their own sessions" ON public.game_sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create their own sessions" ON public.game_sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own sessions" ON public.game_sessions FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own sessions" ON public.game_sessions FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- 2. WBS COMMITMENTS TABLE
-- =====================================================

CREATE TABLE public.wbs_commitments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    wbs_id VARCHAR(50) NOT NULL,
    wbs_name VARCHAR(200) NOT NULL,
    wbs_category VARCHAR(100) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    baseline_cost NUMERIC(12, 2) NOT NULL,
    negotiated_cost NUMERIC(12, 2) NOT NULL,
    committed_cost NUMERIC(12, 2) NOT NULL,
    savings NUMERIC(12, 2) GENERATED ALWAYS AS
        (baseline_cost - committed_cost) STORED,
    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN baseline_cost > 0
         THEN ((baseline_cost - committed_cost) / baseline_cost * 100)
         ELSE 0 END) STORED,
    baseline_duration NUMERIC(3, 1) NOT NULL,
    negotiated_duration NUMERIC(3, 1) NOT NULL,
    committed_duration NUMERIC(3, 1) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'committed'
        CHECK (status IN ('pending', 'committed', 'rejected', 'renegotiating')),
    user_reasoning TEXT,
    quality_level VARCHAR(50),
    scope_changes TEXT,
    committed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

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
    CONSTRAINT unique_wbs_per_session UNIQUE (session_id, wbs_id)
);

-- Indexes and RLS for wbs_commitments
CREATE INDEX idx_wbs_commitments_session_id ON public.wbs_commitments(session_id);
CREATE INDEX idx_wbs_commitments_agent_id ON public.wbs_commitments(agent_id);
CREATE INDEX idx_wbs_commitments_wbs_id ON public.wbs_commitments(wbs_id);
CREATE INDEX idx_wbs_commitments_status ON public.wbs_commitments(status);
ALTER TABLE public.wbs_commitments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view commitments for their sessions" ON public.wbs_commitments FOR SELECT USING (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = wbs_commitments.session_id AND user_id = auth.uid()));
CREATE POLICY "Users can create commitments for their sessions" ON public.wbs_commitments FOR INSERT WITH CHECK (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = wbs_commitments.session_id AND user_id = auth.uid()));
CREATE POLICY "Users can update commitments for their sessions" ON public.wbs_commitments FOR UPDATE USING (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = wbs_commitments.session_id AND user_id = auth.uid()));
CREATE POLICY "Users can delete commitments for their sessions" ON public.wbs_commitments FOR DELETE USING (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = wbs_commitments.session_id AND user_id = auth.uid()));


-- =====================================================
-- 3. NEGOTIATION HISTORY TABLE
-- =====================================================

CREATE TABLE public.negotiation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    agent_type VARCHAR(20) NOT NULL
        CHECK (agent_type IN ('owner', 'supplier')),
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    is_disagreement BOOLEAN DEFAULT FALSE,
    disagreement_reason TEXT,
    contains_offer BOOLEAN DEFAULT FALSE,
    offer_data JSONB,
    context_snapshot JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_ms INTEGER,
    sentiment VARCHAR(20) CHECK (sentiment IN ('positive', 'neutral', 'negative', NULL))
);

-- Indexes and RLS for negotiation_history
CREATE INDEX idx_negotiation_history_session_id ON public.negotiation_history(session_id);
CREATE INDEX idx_negotiation_history_agent_id ON public.negotiation_history(agent_id);
CREATE INDEX idx_negotiation_history_timestamp ON public.negotiation_history(timestamp DESC);
CREATE INDEX idx_negotiation_history_disagreement ON public.negotiation_history(is_disagreement) WHERE is_disagreement = TRUE;
ALTER TABLE public.negotiation_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view negotiation history for their sessions" ON public.negotiation_history FOR SELECT USING (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = negotiation_history.session_id AND user_id = auth.uid()));
CREATE POLICY "Users can create negotiation history for their sessions" ON public.negotiation_history FOR INSERT WITH CHECK (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = negotiation_history.session_id AND user_id = auth.uid()));

-- =====================================================
-- 4. AGENT TIMEOUTS TABLE
-- =====================================================

CREATE TABLE public.agent_timeouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,
    locked_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    unlock_at TIMESTAMP WITH TIME ZONE NOT NULL,
    lock_duration_minutes INTEGER NOT NULL DEFAULT 10,
    agent_message TEXT NOT NULL,
    trigger_reason VARCHAR(100),
    disagreement_count INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    unlocked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_lock_duration CHECK (lock_duration_minutes > 0),
    CONSTRAINT valid_disagreement_count CHECK (disagreement_count >= 0)
);

-- Indexes and RLS for agent_timeouts
CREATE INDEX idx_agent_timeouts_session_agent ON public.agent_timeouts(session_id, agent_id);
CREATE INDEX idx_agent_timeouts_active ON public.agent_timeouts(is_active, unlock_at) WHERE is_active = TRUE;
CREATE INDEX idx_agent_timeouts_unlock_at ON public.agent_timeouts(unlock_at);
ALTER TABLE public.agent_timeouts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view timeouts for their sessions" ON public.agent_timeouts FOR ALL USING (EXISTS (SELECT 1 FROM public.game_sessions WHERE id = agent_timeouts.session_id AND user_id = auth.uid()));

-- =====================================================
-- 5. USER ANALYTICS TABLE (Optional - Future)
-- =====================================================

CREATE TABLE public.user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    total_sessions INTEGER DEFAULT 0,
    completed_sessions INTEGER DEFAULT 0,
    failed_sessions INTEGER DEFAULT 0,
    total_budget_saved NUMERIC(12, 2) DEFAULT 0.00,
    average_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,
    best_savings_percentage NUMERIC(5, 2) DEFAULT 0.00,
    best_session_id UUID REFERENCES public.game_sessions(id) ON DELETE SET NULL,
    average_session_duration_seconds INTEGER DEFAULT 0,
    total_play_time_seconds INTEGER DEFAULT 0,
    fastest_completion_seconds INTEGER,
    total_negotiations INTEGER DEFAULT 0,
    average_negotiations_per_session NUMERIC(5, 2) DEFAULT 0.00,
    total_timeouts INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_analytics UNIQUE (user_id)
);

-- Indexes and RLS for user_analytics
CREATE INDEX idx_user_analytics_user_id ON public.user_analytics(user_id);
CREATE INDEX idx_user_analytics_best_savings ON public.user_analytics(best_savings_percentage DESC);
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view their own analytics" ON public.user_analytics FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own analytics" ON public.user_analytics FOR ALL USING (auth.uid() = user_id);

-- =====================================================
-- 6. FUNCTIONS & TRIGGERS
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_game_sessions_updated_at
    BEFORE UPDATE ON public.game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_wbs_commitments_updated_at
    BEFORE UPDATE ON public.wbs_commitments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_analytics_updated_at
    BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

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
    gs.created_at
FROM public.game_sessions gs
LEFT JOIN public.wbs_commitments wc ON gs.id = wc.session_id AND wc.status = 'committed'
WHERE gs.status = 'in_progress'
GROUP BY gs.id;

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