-- =====================================================
-- MIGRATION 003: Budget Revision Support
-- Created: 2026-01-01
-- Purpose: Add budget revision snapshot support for owner negotiation
-- =====================================================

-- =====================================================
-- STEP 1: Modify session_snapshots table to support budget_revision type
-- =====================================================

-- Update the snapshot_type CHECK constraint to include 'budget_revision'
ALTER TABLE public.session_snapshots
DROP CONSTRAINT IF EXISTS session_snapshots_snapshot_type_check;

ALTER TABLE public.session_snapshots
ADD CONSTRAINT session_snapshots_snapshot_type_check
CHECK (snapshot_type IN ('baseline', 'contract_acceptance', 'budget_revision'));

-- Add columns for budget revision tracking (nullable for backward compatibility)
ALTER TABLE public.session_snapshots
ADD COLUMN IF NOT EXISTS revision_old_budget BIGINT CHECK (revision_old_budget >= 0),
ADD COLUMN IF NOT EXISTS revision_new_budget BIGINT CHECK (revision_new_budget >= 0),
ADD COLUMN IF NOT EXISTS revision_amount BIGINT,
ADD COLUMN IF NOT EXISTS revision_justification TEXT;

-- Update baseline constraint to allow budget_revision without contract details
ALTER TABLE public.session_snapshots
DROP CONSTRAINT IF EXISTS baseline_no_contract;

ALTER TABLE public.session_snapshots
ADD CONSTRAINT baseline_no_contract CHECK (
    (snapshot_type = 'baseline' AND contract_wbs_id IS NULL AND contract_cost IS NULL) OR
    (snapshot_type = 'contract_acceptance' AND contract_wbs_id IS NOT NULL AND contract_cost IS NOT NULL) OR
    (snapshot_type = 'budget_revision' AND contract_wbs_id IS NULL AND revision_amount IS NOT NULL)
);

-- =====================================================
-- STEP 2: Create budget revision snapshot function
-- =====================================================

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
        v_budget_total := v_latest_snapshot.budget_total;  -- Keep at 700 MNOK
    END IF;

    -- Validate budget constraints
    IF v_budget_total != 70000000000 AND NOT p_affects_total_budget THEN
        RAISE EXCEPTION 'Total budget must remain 700 MNOK (70000000000 øre) unless affects_total_budget is true';
    END IF;

    IF v_budget_committed + v_budget_available != v_budget_total THEN
        RAISE EXCEPTION 'Budget integrity error: committed (%) + available (%) != total (%)',
            v_budget_committed, v_budget_available, v_budget_total;
    END IF;

    -- Generate label showing the increase
    v_label := 'Budsjettøkning: +' || (p_revision_amount / 100000000) || ' MNOK';

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

-- =====================================================
-- COMMENTS for Documentation
-- =====================================================

COMMENT ON FUNCTION public.create_budget_revision_snapshot IS
'Creates a snapshot when owner agent approves budget increase. Timeline state is copied from latest snapshot (budget does not affect critical path). Returns snapshot ID.';

COMMENT ON COLUMN public.session_snapshots.revision_old_budget IS
'Previous available budget before revision (in øre). Only populated for budget_revision snapshots.';

COMMENT ON COLUMN public.session_snapshots.revision_new_budget IS
'New available budget after revision (in øre). Only populated for budget_revision snapshots.';

COMMENT ON COLUMN public.session_snapshots.revision_amount IS
'Amount of budget increase in øre (revision_new_budget - revision_old_budget). Only populated for budget_revision snapshots.';

COMMENT ON COLUMN public.session_snapshots.revision_justification IS
'Justification text for why budget was increased. Only populated for budget_revision snapshots. Example: "Godkjent på grunn av omfangsendring"';

-- =====================================================
-- SAMPLE USAGE (for testing)
-- =====================================================

-- Example: Create budget revision snapshot
-- SELECT public.create_budget_revision_snapshot(
--     'your-session-id-here',
--     31000000000,   -- old_budget: 310 MNOK (in øre)
--     36000000000,   -- new_budget: 360 MNOK (in øre)
--     5000000000,    -- revision_amount: +50 MNOK (in øre)
--     'Godkjent på grunn av omfangsendring og økte infrastrukturkostnader',
--     FALSE          -- affects_total_budget (FALSE = total stays at 700 MNOK)
-- );

-- =====================================================
-- ROLLBACK (if needed)
-- =====================================================

-- DROP FUNCTION IF EXISTS public.create_budget_revision_snapshot(UUID, BIGINT, BIGINT, BIGINT, TEXT, BOOLEAN);
-- ALTER TABLE public.session_snapshots DROP COLUMN IF EXISTS revision_old_budget;
-- ALTER TABLE public.session_snapshots DROP COLUMN IF EXISTS revision_new_budget;
-- ALTER TABLE public.session_snapshots DROP COLUMN IF EXISTS revision_amount;
-- ALTER TABLE public.session_snapshots DROP COLUMN IF EXISTS revision_justification;
-- -- Restore old constraint (would need to recreate manually)
