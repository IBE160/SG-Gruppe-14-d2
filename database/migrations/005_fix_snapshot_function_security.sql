-- =====================================================
-- MIGRATION 005: Fix Snapshot Function Security
-- Created: 2026-01-02
-- Purpose: Add SECURITY DEFINER to snapshot creation functions to bypass RLS
-- =====================================================

-- The issue: RLS policies check auth.uid(), but inside PL/pgSQL functions,
-- the auth context may not be properly set, causing INSERT to fail silently.
-- Solution: Add SECURITY DEFINER so functions run with owner permissions and bypass RLS.

-- =====================================================
-- Fix create_budget_revision_snapshot
-- =====================================================

DROP FUNCTION IF EXISTS public.create_budget_revision_snapshot(UUID, BIGINT, BIGINT, BIGINT, TEXT, BOOLEAN);

CREATE OR REPLACE FUNCTION public.create_budget_revision_snapshot(
    p_session_id UUID,
    p_old_budget BIGINT,
    p_new_budget BIGINT,
    p_revision_amount BIGINT,
    p_justification TEXT,
    p_affects_total_budget BOOLEAN DEFAULT FALSE
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER  -- <<< THIS IS THE FIX - Run as function owner, bypass RLS
AS $$
DECLARE
    v_snapshot_id UUID;
    v_label VARCHAR(255);
    v_latest_snapshot RECORD;
    v_budget_committed BIGINT;
    v_budget_available BIGINT;
    v_budget_total BIGINT;
BEGIN
    -- Validate inputs
    IF p_revision_amount <= 0 THEN
        RAISE EXCEPTION 'Revision amount must be positive, got: %', p_revision_amount;
    END IF;

    IF p_justification IS NULL OR TRIM(p_justification) = '' THEN
        RAISE EXCEPTION 'Justification is required for budget revisions';
    END IF;

    IF p_new_budget != p_old_budget + p_revision_amount THEN
        RAISE EXCEPTION 'Budget math error: new_budget (%) != old_budget (%) + revision_amount (%)',
            p_new_budget, p_old_budget, p_revision_amount;
    END IF;

    -- Fetch latest snapshot to get current timeline state
    SELECT *
    INTO v_latest_snapshot
    FROM public.session_snapshots
    WHERE session_id = p_session_id
    ORDER BY version DESC
    LIMIT 1;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'No existing snapshots found for session %', p_session_id;
    END IF;

    -- Calculate new budget state
    v_budget_committed := v_latest_snapshot.budget_committed;  -- Unchanged
    v_budget_available := v_latest_snapshot.budget_available + p_revision_amount;

    IF p_affects_total_budget THEN
        v_budget_total := v_latest_snapshot.budget_total + p_revision_amount;
    ELSE
        v_budget_total := v_latest_snapshot.budget_total;  -- Keep at current total
    END IF;

    -- Validate budget integrity (committed + available = total)
    IF v_budget_committed + v_budget_available != v_budget_total THEN
        RAISE EXCEPTION 'Budget integrity error: committed (%) + available (%) != total (%)',
            v_budget_committed, v_budget_available, v_budget_total;
    END IF;

    -- Generate label showing the increase (values are in NOK, divide by 1,000,000 for MNOK)
    v_label := 'Budsjettøkning: +' || (p_revision_amount / 1000000) || ' MNOK';

    -- Create snapshot (copy timeline from latest, update budget only)
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
        precedence_state,
        revision_old_budget,
        revision_new_budget,
        revision_amount,
        revision_justification
    )
    VALUES (
        p_session_id,
        v_label,
        'budget_revision',
        v_budget_committed,
        v_budget_available,
        v_budget_total,
        NULL,  -- No contract for budget revision
        NULL,
        NULL,
        NULL,
        v_latest_snapshot.project_end_date,      -- Copy from latest (timeline unchanged)
        v_latest_snapshot.days_before_deadline,  -- Copy from latest (timeline unchanged)
        v_latest_snapshot.gantt_state,           -- Copy from latest (timeline unchanged)
        v_latest_snapshot.precedence_state,      -- Copy from latest (timeline unchanged)
        p_old_budget,
        p_new_budget,
        p_revision_amount,
        p_justification
    )
    RETURNING id INTO v_snapshot_id;

    RAISE NOTICE 'Budget revision snapshot created with ID: %', v_snapshot_id;

    RETURN v_snapshot_id;
END;
$$;

-- Update comments
COMMENT ON FUNCTION public.create_budget_revision_snapshot IS
'Creates a snapshot when owner agent approves budget increase. Timeline state is copied from latest snapshot (budget does not affect critical path). Values are in NOK (not øre). Runs with SECURITY DEFINER to bypass RLS. Returns snapshot ID.';

-- =====================================================
-- Also fix create_contract_snapshot
-- =====================================================

DROP FUNCTION IF EXISTS public.create_contract_snapshot(UUID, VARCHAR, BIGINT, INTEGER, VARCHAR, BIGINT, BIGINT, DATE, INTEGER, JSONB, JSONB);

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
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER  -- <<< THIS IS THE FIX - Run as function owner, bypass RLS
AS $$
DECLARE
    v_snapshot_id UUID;
    v_label VARCHAR(255);
BEGIN
    -- Generate label from WBS data
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
        70000000000,  -- Always 700 MNOK (70 billion øre)
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

    RAISE NOTICE 'Contract snapshot created with ID: %', v_snapshot_id;

    RETURN v_snapshot_id;
END;
$$;

COMMENT ON FUNCTION public.create_contract_snapshot IS
'Creates a snapshot when a vendor contract is accepted. Stores complete timeline state (Gantt, Precedence). Runs with SECURITY DEFINER to bypass RLS. Returns snapshot ID.';

-- =====================================================
-- Verification Query
-- =====================================================

-- After running this migration, verify the function has SECURITY DEFINER:
-- SELECT
--     proname,
--     prosecdef,
--     CASE WHEN prosecdef THEN 'SECURITY DEFINER' ELSE 'SECURITY INVOKER' END as security_mode
-- FROM pg_proc
-- WHERE proname = 'create_budget_revision_snapshot';

-- Expected result: prosecdef = true, security_mode = 'SECURITY DEFINER'
