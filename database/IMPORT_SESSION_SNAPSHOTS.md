# Session Snapshots Table Import Guide

## Quick Import to Supabase

### Option 1: SQL Editor (Recommended)

1. **Open Supabase Dashboard:** https://supabase.com/dashboard
2. **Navigate to:** Your Project → SQL Editor
3. **New Query:** Click "New query"
4. **Copy & Paste:** Open `database/migrations/002_session_snapshots.sql` and paste entire contents
5. **Run:** Click "Run" button (or Ctrl+Enter)
6. **Verify:** Check "Table Editor" → should see `session_snapshots` table

### Option 2: Using Supabase CLI

```bash
# If you have Supabase CLI installed
cd C:\Users\morte\Documents\GitHub\SG-Gruppe-14-d2
supabase db push
```

---

## Verification Checklist

After running the migration, verify:

- [ ] **Table created:** `session_snapshots` visible in Table Editor
- [ ] **6 tables total:** game_sessions, wbs_commitments, negotiation_history, agent_timeouts, user_analytics, **session_snapshots**
- [ ] **Indexes created:** Check Indexes tab for `idx_snapshots_session_version`, `idx_snapshots_type`, `idx_snapshots_created_at`
- [ ] **RLS enabled:** Row Level Security should be ON
- [ ] **Functions created:** `create_baseline_snapshot()`, `create_contract_snapshot()`, `auto_increment_snapshot_version()`, `enforce_snapshot_limit()`

---

## Test the Functions

After import, test the helper functions:

```sql
-- Test 1: Create a test session (if needed)
INSERT INTO game_sessions (id, user_id, status)
VALUES ('test-session-123', auth.uid(), 'in_progress');

-- Test 2: Create baseline snapshot
SELECT public.create_baseline_snapshot('test-session-123');

-- Test 3: Verify baseline created
SELECT * FROM session_snapshots WHERE session_id = 'test-session-123';
-- Should return 1 row with version = 0

-- Test 4: Create contract snapshot
SELECT public.create_contract_snapshot(
  'test-session-123',
  '1.3.1',
  105000000,
  60,
  'Bjørn Eriksen AS',
  495000000,
  205000000,
  '2025-09-29',
  228
);

-- Test 5: Verify both snapshots exist
SELECT version, label, budget_committed, budget_available
FROM session_snapshots
WHERE session_id = 'test-session-123'
ORDER BY version;
-- Should return 2 rows (version 0 and 1)

-- Cleanup test data
DELETE FROM game_sessions WHERE id = 'test-session-123';
```

---

## Troubleshooting

**Error: "uuid_generate_v4() does not exist"**
- **Fix:** Run `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` first

**Error: "auth.uid() does not exist"**
- **Fix:** You're not authenticated. RLS policies only work when logged in as a user.
- **Workaround for testing:** Temporarily disable RLS: `ALTER TABLE session_snapshots DISABLE ROW LEVEL SECURITY;`

**Error: "relation session_snapshots already exists"**
- **Fix:** Table already created. Drop it first: `DROP TABLE IF EXISTS session_snapshots CASCADE;`

---

## Next Steps

After successful import:
1. ✅ Database migration complete
2. ⏭️ Implement backend API endpoints (see `backend/main.py`)
3. ⏭️ Implement frontend components (see `frontend/components/`)

---

## Migration File Location

`database/migrations/002_session_snapshots.sql`
