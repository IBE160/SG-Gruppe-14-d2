-- =====================================================
-- MIGRATION 002: Session Snapshots for History/Timeline View
-- Created: 2025-12-17
-- Purpose: Track contract acceptance snapshots for pedagogical history view
-- =====================================================

-- =====================================================
-- TABLE: session_snapshots
-- Purpose: Stores snapshots of session state at each contract acceptance
-- Scope: 1 baseline + up to 99 contract acceptances = 100 max per session
-- =====================================================

CREATE TABLE IF NOT EXISTS public.session_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES public.game_sessions(id) ON DELETE CASCADE,

    -- Version tracking
    version INTEGER NOT NULL,  -- 0 (baseline), 1, 2, 3... up to 100
    label VARCHAR(255) NOT NULL,  -- "Baseline" or "WBS 1.3.1 - Grunnarbeid"
    snapshot_type VARCHAR(50) NOT NULL CHECK (snapshot_type IN ('baseline', 'contract_acceptance')),

    -- Budget state (in øre for precision)
    budget_committed BIGINT NOT NULL CHECK (budget_committed >= 0),  -- e.g., 390000000 (390 MNOK)
    budget_available BIGINT NOT NULL CHECK (budget_available >= 0),  -- e.g., 310000000 (310 MNOK)
    budget_total BIGINT NOT NULL DEFAULT 700000000 CHECK (budget_total = 700000000),  -- Always 700 MNOK

    -- Contract details (null for baseline snapshots)
    contract_wbs_id VARCHAR(50),           -- "1.3.1", "1.3.2", etc.
    contract_cost BIGINT CHECK (contract_cost >= 0),  -- in øre
    contract_duration INTEGER CHECK (contract_duration > 0),  -- days
    contract_supplier VARCHAR(255),         -- "Bjørn Eriksen AS"

    -- Timeline state
    project_end_date DATE NOT NULL,
    days_before_deadline INTEGER NOT NULL,  -- Positive = before deadline, negative = overdue

    -- Visualization snapshots (JSONB for compression and querying)
    gantt_state JSONB NOT NULL DEFAULT '{}'::jsonb,        -- gantt-task-react data structure
    precedence_state JSONB NOT NULL DEFAULT '{}'::jsonb,    -- ReactFlow nodes and edges

    -- Metadata
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT unique_session_version UNIQUE (session_id, version),
    CONSTRAINT baseline_no_contract CHECK (
        (snapshot_type = 'baseline' AND contract_wbs_id IS NULL AND contract_cost IS NULL) OR
        (snapshot_type = 'contract_acceptance' AND contract_wbs_id IS NOT NULL AND contract_cost IS NOT NULL)
    )
);

-- =====================================================
-- INDEXES for Performance
-- =====================================================

-- Fast lookup of latest snapshots (most common query)
CREATE INDEX idx_snapshots_session_version
ON public.session_snapshots(session_id, version DESC);

-- Fast filtering by snapshot type
CREATE INDEX idx_snapshots_type
ON public.session_snapshots(session_id, snapshot_type);

-- Fast cleanup queries (delete old sessions)
CREATE INDEX idx_snapshots_created_at
ON public.session_snapshots(created_at);

-- JSONB indexes for querying visualization states (optional, add if needed)
-- CREATE INDEX idx_snapshots_gantt_state ON public.session_snapshots USING GIN (gantt_state);
-- CREATE INDEX idx_snapshots_precedence_state ON public.session_snapshots USING GIN (precedence_state);

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

ALTER TABLE public.session_snapshots ENABLE ROW LEVEL SECURITY;

-- Users can view snapshots for their own sessions
CREATE POLICY "Users can view snapshots for their sessions"
    ON public.session_snapshots FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = session_snapshots.session_id
            AND user_id = auth.uid()
        )
    );

-- System can create snapshots (called by backend API)
CREATE POLICY "System can create snapshots"
    ON public.session_snapshots FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = session_snapshots.session_id
            AND user_id = auth.uid()
        )
    );

-- No update policy (snapshots are immutable once created)
-- No delete policy for users (only cleanup jobs can delete via admin credentials)

-- =====================================================
-- TRIGGER: Auto-increment version number
-- =====================================================

CREATE OR REPLACE FUNCTION public.auto_increment_snapshot_version()
RETURNS TRIGGER AS $$
BEGIN
    -- If version not provided, calculate next version
    IF NEW.version IS NULL THEN
        SELECT COALESCE(MAX(version), -1) + 1
        INTO NEW.version
        FROM public.session_snapshots
        WHERE session_id = NEW.session_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_increment_version
BEFORE INSERT ON public.session_snapshots
FOR EACH ROW
EXECUTE FUNCTION public.auto_increment_snapshot_version();

-- =====================================================
-- TRIGGER: Enforce 100 snapshot limit (sliding window)
-- =====================================================

CREATE OR REPLACE FUNCTION public.enforce_snapshot_limit()
RETURNS TRIGGER AS $$
DECLARE
    snapshot_count INTEGER;
    max_snapshots INTEGER := 100;
BEGIN
    -- Count current snapshots for this session
    SELECT COUNT(*)
    INTO snapshot_count
    FROM public.session_snapshots
    WHERE session_id = NEW.session_id;

    -- If exceeding limit, delete oldest snapshots
    IF snapshot_count >= max_snapshots THEN
        DELETE FROM public.session_snapshots
        WHERE session_id = NEW.session_id
        AND version IN (
            SELECT version
            FROM public.session_snapshots
            WHERE session_id = NEW.session_id
            ORDER BY version ASC
            LIMIT (snapshot_count - max_snapshots + 1)
        );
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_enforce_snapshot_limit
AFTER INSERT ON public.session_snapshots
FOR EACH ROW
EXECUTE FUNCTION public.enforce_snapshot_limit();

-- =====================================================
-- HELPER FUNCTION: Create baseline snapshot
-- =====================================================

CREATE OR REPLACE FUNCTION public.create_baseline_snapshot(
    p_session_id UUID,
    p_project_end_date DATE DEFAULT '2025-08-30',
    p_days_before_deadline INTEGER DEFAULT 258
)
RETURNS UUID AS $$
DECLARE
    v_snapshot_id UUID;
BEGIN
    INSERT INTO public.session_snapshots (
        session_id,
        version,
        label,
        snapshot_type,
        budget_committed,
        budget_available,
        budget_total,
        contract_wbs_id,
        contract_cost,
        contract_duration,
        contract_supplier,
        project_end_date,
        days_before_deadline,
        gantt_state,
        precedence_state
    )
    VALUES (
        p_session_id,
        0,  -- Baseline is always version 0
        'Baseline - 12 Kontraktfestede Pakker',
        'baseline',
        390000000,  -- 390 MNOK locked
        310000000,  -- 310 MNOK available
        700000000,  -- 700 MNOK total
        NULL,       -- No contract for baseline
        NULL,
        NULL,
        NULL,
        p_project_end_date,
        p_days_before_deadline,
        '{}'::jsonb,  -- Empty gantt state (will be populated by frontend)
        '{}'::jsonb   -- Empty precedence state
    )
    RETURNING id INTO v_snapshot_id;

    RETURN v_snapshot_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- HELPER FUNCTION: Create contract acceptance snapshot
-- =====================================================

CREATE OR REPLACE FUNCTION public.create_contract_snapshot(
    p_session_id UUID,
    p_wbs_id VARCHAR(50),
    p_cost BIGINT,
    p_duration INTEGER,
    p_supplier VARCHAR(255),
    p_budget_committed BIGINT,
    p_budget_available BIGINT,
    p_project_end_date DATE,
    p_days_before_deadline INTEGER,
    p_gantt_state JSONB DEFAULT '{}'::jsonb,
    p_precedence_state JSONB DEFAULT '{}'::jsonb
)
RETURNS UUID AS $$
DECLARE
    v_snapshot_id UUID;
    v_label VARCHAR(255);
BEGIN
    -- Generate label from WBS data (can be enhanced with WBS name lookup)
    v_label := 'WBS ' || p_wbs_id || ' - Akseptert';

    INSERT INTO public.session_snapshots (
        session_id,
        label,
        snapshot_type,
        budget_committed,
        budget_available,
        budget_total,
        contract_wbs_id,
        contract_cost,
        contract_duration,
        contract_supplier,
        project_end_date,
        days_before_deadline,
        gantt_state,
        precedence_state
    )
    VALUES (
        p_session_id,
        v_label,
        'contract_acceptance',
        p_budget_committed,
        p_budget_available,
        700000000,  -- Always 700 MNOK
        p_wbs_id,
        p_cost,
        p_duration,
        p_supplier,
        p_project_end_date,
        p_days_before_deadline,
        p_gantt_state,
        p_precedence_state
    )
    RETURNING id INTO v_snapshot_id;

    RETURN v_snapshot_id;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- COMMENTS for Documentation
-- =====================================================

COMMENT ON TABLE public.session_snapshots IS
'Stores snapshots of session state at each contract acceptance for history/timeline view. Maximum 100 snapshots per session (sliding window). Used for pedagogical analysis of decision impacts.';

COMMENT ON COLUMN public.session_snapshots.version IS
'Auto-incrementing version number starting at 0 (baseline). Unique per session.';

COMMENT ON COLUMN public.session_snapshots.snapshot_type IS
'Type of snapshot: "baseline" (version 0, starting state) or "contract_acceptance" (version 1+, after accepting offer)';

COMMENT ON COLUMN public.session_snapshots.budget_committed IS
'Total budget committed at this snapshot, in Norwegian øre (NOK × 100). Example: 390000000 = 390 MNOK';

COMMENT ON COLUMN public.session_snapshots.gantt_state IS
'JSONB snapshot of gantt-task-react data structure at this version. Compressed automatically by PostgreSQL TOAST.';

COMMENT ON COLUMN public.session_snapshots.precedence_state IS
'JSONB snapshot of ReactFlow nodes and edges at this version. Compressed automatically by PostgreSQL TOAST.';

-- =====================================================
-- SAMPLE DATA (for testing)
-- =====================================================

-- Example: Create baseline snapshot for a session
-- SELECT public.create_baseline_snapshot('your-session-id-here');

-- Example: Create contract acceptance snapshot
-- SELECT public.create_contract_snapshot(
--     'your-session-id-here',
--     '1.3.1',
--     105000000,
--     60,
--     'Bjørn Eriksen AS',
--     495000000,
--     205000000,
--     '2025-09-29',
--     228,
--     '{"tasks": [...]}'::jsonb,
--     '{"nodes": [...], "edges": [...]}'::jsonb
-- );

-- =====================================================
-- ROLLBACK (if needed)
-- =====================================================

-- DROP TRIGGER IF EXISTS trigger_enforce_snapshot_limit ON public.session_snapshots;
-- DROP TRIGGER IF EXISTS trigger_auto_increment_version ON public.session_snapshots;
-- DROP FUNCTION IF EXISTS public.enforce_snapshot_limit();
-- DROP FUNCTION IF EXISTS public.auto_increment_snapshot_version();
-- DROP FUNCTION IF EXISTS public.create_contract_snapshot(UUID, VARCHAR, BIGINT, INTEGER, VARCHAR, BIGINT, BIGINT, DATE, INTEGER, JSONB, JSONB);
-- DROP FUNCTION IF EXISTS public.create_baseline_snapshot(UUID, DATE, INTEGER);
-- DROP TABLE IF EXISTS public.session_snapshots CASCADE;
