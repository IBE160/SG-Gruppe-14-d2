-- PART 1: CREATE TABLES ONLY
-- Run this first

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    total_budget NUMERIC(12, 2) NOT NULL DEFAULT 700000000.00,
    locked_budget NUMERIC(12, 2) NOT NULL DEFAULT 390000000.00,
    available_budget NUMERIC(12, 2) NOT NULL DEFAULT 310000000.00,
    current_budget_used NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    budget_tier1_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN available_budget > 0 THEN (current_budget_used / available_budget) * 100 ELSE 0 END) STORED,
    budget_tier3_total NUMERIC(12, 2) GENERATED ALWAYS AS (locked_budget + current_budget_used) STORED,
    budget_tier3_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN total_budget > 0 THEN ((locked_budget + current_budget_used) / total_budget) * 100 ELSE 0 END) STORED,
    budget_remaining NUMERIC(12, 2) GENERATED ALWAYS AS (available_budget - current_budget_used) STORED,
    deadline_date DATE NOT NULL DEFAULT '2026-05-15',
    projected_completion_date DATE,
    is_timeline_valid BOOLEAN GENERATED ALWAYS AS
        (projected_completion_date IS NULL OR projected_completion_date <= '2026-05-15') STORED,
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress',
    game_state JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    CONSTRAINT budget_not_exceeded CHECK (current_budget_used <= available_budget),
    CONSTRAINT total_budget_valid CHECK ((locked_budget + current_budget_used) <= total_budget)
);

CREATE TABLE IF NOT EXISTS public.wbs_commitments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    wbs_id VARCHAR(10) NOT NULL,
    wbs_name VARCHAR(200),
    committed_price NUMERIC(12, 2) NOT NULL,
    committed_duration_weeks INTEGER NOT NULL,
    baseline_price NUMERIC(12, 2) NOT NULL,
    baseline_duration_weeks INTEGER NOT NULL,
    savings NUMERIC(12, 2) GENERATED ALWAYS AS (baseline_price - committed_price) STORED,
    savings_percentage NUMERIC(5, 2) GENERATED ALWAYS AS
        (CASE WHEN baseline_price > 0 THEN ((baseline_price - committed_price) / baseline_price) * 100 ELSE 0 END) STORED,
    negotiated_scope TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_wbs_id CHECK (wbs_id IN ('1.3.1', '1.3.2', '1.4.1')),
    CONSTRAINT unique_wbs_per_session UNIQUE (session_id, wbs_id),
    CONSTRAINT positive_price CHECK (committed_price >= 0),
    CONSTRAINT positive_duration CHECK (committed_duration_weeks > 0)
);

CREATE TABLE IF NOT EXISTS public.negotiation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,
    agent_id VARCHAR(50) NOT NULL,
    agent_name VARCHAR(100),
    agent_type VARCHAR(20) NOT NULL,
    user_message TEXT NOT NULL,
    agent_response TEXT NOT NULL,
    is_disagreement BOOLEAN DEFAULT FALSE,
    disagreement_reason TEXT,
    context_snapshot JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT valid_agent_type CHECK (agent_type IN ('owner', 'supplier'))
);

CREATE TABLE IF NOT EXISTS public.agent_timeouts (
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    total_sessions INTEGER DEFAULT 0,
    completed_sessions INTEGER DEFAULT 0,
    total_savings NUMERIC(12, 2) DEFAULT 0,
    average_savings_percentage NUMERIC(5, 2) DEFAULT 0,
    best_savings_percentage NUMERIC(5, 2) DEFAULT 0,
    total_negotiations INTEGER DEFAULT 0,
    successful_negotiations INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_user_analytics UNIQUE (user_id)
);
