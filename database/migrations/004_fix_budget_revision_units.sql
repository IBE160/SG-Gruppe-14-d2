-- =====================================================
-- MIGRATION 004: Fix Budget Revision Units (NOK not øre)
-- Created: 2026-01-01
-- Purpose: Update create_budget_revision_snapshot to use NOK instead of øre
-- =====================================================

-- Drop and recreate the function with correct NOK units
DROP FUNCTION IF EXISTS public.create_budget_revision_snapshot(UUID, BIGINT, BIGINT, BIGINT, TEXT, BOOLEAN);

CREATE OR REPLACE FUNCTION public.create_budget_revision_snapshot(
    p_session_id UUID,
    p_old_budget BIGINT,
    p_new_budget BIGINT,
    p_revision_amount BIGINT,
    p_justification TEXT,
    p_affects_total_budget BOOLEAN DEFAULT FALSE
)
RETURNS UUID AS $$
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

    -- Note: Removed strict validation that required exactly 700 MNOK
    -- Budget revisions can increase total budget, so we allow flexibility

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

    RETURN v_snapshot_id;
END;
$$ LANGUAGE plpgsql;

-- Update comments to reflect NOK units (not øre)
COMMENT ON FUNCTION public.create_budget_revision_snapshot IS
'Creates a snapshot when owner agent approves budget increase. Timeline state is copied from latest snapshot (budget does not affect critical path). Values are in NOK (not øre). Returns snapshot ID.';

COMMENT ON COLUMN public.session_snapshots.revision_old_budget IS
'Previous available budget before revision (in NOK). Only populated for budget_revision snapshots.';

COMMENT ON COLUMN public.session_snapshots.revision_new_budget IS
'New available budget after revision (in NOK). Only populated for budget_revision snapshots.';

COMMENT ON COLUMN public.session_snapshots.revision_amount IS
'Amount of budget increase in NOK (revision_new_budget - revision_old_budget). Only populated for budget_revision snapshots.';

-- =====================================================
-- SAMPLE USAGE (for testing with NOK units)
-- =====================================================

-- Example: Create budget revision snapshot
-- SELECT public.create_budget_revision_snapshot(
--     'your-session-id-here',
--     310000000,    -- old_budget: 310 MNOK (in NOK)
--     360000000,    -- new_budget: 360 MNOK (in NOK)
--     50000000,     -- revision_amount: +50 MNOK (in NOK)
--     'Godkjent på grunn av omfangsendring og økte infrastrukturkostnader',
--     TRUE          -- affects_total_budget (TRUE = total increases too)
-- );
