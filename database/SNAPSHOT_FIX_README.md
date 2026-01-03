# Snapshot Creation Fix - Migration 005

## Problem Identified

**Issue:** Snapshot creation was failing silently - database functions executed but no rows were inserted into `session_snapshots` table.

**Root Cause:** Row Level Security (RLS) policies blocking INSERT operations from database functions.

### Technical Details

The `session_snapshots` table has RLS enabled with this policy:

```sql
CREATE POLICY "System can create snapshots"
    ON public.session_snapshots FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.game_sessions
            WHERE id = session_snapshots.session_id
            AND user_id = auth.uid()  -- <<< THE PROBLEM
        )
    );
```

When database functions (`create_contract_snapshot`, `create_budget_revision_snapshot`) tried to INSERT, the RLS policy checked `auth.uid()`. However, **inside PL/pgSQL functions, the auth context may not be properly set**, causing `auth.uid()` to return NULL or an incorrect value.

Result: The INSERT was silently blocked by RLS, even though the function executed successfully.

## Solution

Add `SECURITY DEFINER` to both snapshot creation functions. This makes the functions run with the permissions of the **function owner** (who has full database access) rather than the calling user, effectively bypassing RLS.

### Changes Made

**Before:**
```sql
CREATE OR REPLACE FUNCTION public.create_budget_revision_snapshot(...)
RETURNS UUID AS $$
...
$$ LANGUAGE plpgsql;  -- Missing SECURITY DEFINER
```

**After:**
```sql
CREATE OR REPLACE FUNCTION public.create_budget_revision_snapshot(...)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER  -- <<< FIX: Bypass RLS
AS $$
...
$$;
```

## How to Apply the Fix

### Method 1: Supabase Dashboard (Recommended)

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Open your project
3. Navigate to **SQL Editor**
4. Create a new query
5. Copy the contents of `database/migrations/005_fix_snapshot_function_security.sql`
6. Paste and click **Run**

### Method 2: Command Line (if you have psql)

```bash
psql 'your-connection-string' < database/migrations/005_fix_snapshot_function_security.sql
```

## Verification

After applying the migration, verify both functions have SECURITY DEFINER:

```sql
SELECT
    proname,
    prosecdef,
    CASE WHEN prosecdef THEN 'SECURITY DEFINER' ELSE 'SECURITY INVOKER' END as security_mode
FROM pg_proc
WHERE proname IN ('create_budget_revision_snapshot', 'create_contract_snapshot');
```

**Expected result:** Both functions should show `prosecdef = true` and `security_mode = 'SECURITY DEFINER'`

## Test the Fix

After applying the migration, test snapshot creation:

1. Start the backend: `cd backend && uvicorn main:app --reload`
2. Create a new session and accept a vendor contract
3. Check if snapshot was created:

```sql
SELECT version, snapshot_type, label, created_at
FROM session_snapshots
WHERE session_id = 'your-session-id'
ORDER BY version;
```

4. Test budget revision:
   - Chat with owner agent (Anne-Lise Berg)
   - Request and accept a budget increase
   - Verify budget revision snapshot appears in the history panel

## Security Considerations

**Q: Is SECURITY DEFINER safe?**

A: Yes, in this case. The functions have proper input validation and only perform INSERT operations on `session_snapshots` table. They don't expose any dangerous functionality.

The functions validate:
- All required parameters are present and non-null
- Budget math is correct (new = old + increase)
- Session exists before creating snapshot
- Budget integrity (committed + available = total)

**Best practices followed:**
- Functions raise exceptions on invalid input
- No dynamic SQL execution
- Limited scope (only INSERT into one table)
- Proper parameter types and constraints

## Files Changed

- ✅ `database/migrations/005_fix_snapshot_function_security.sql` - Migration file (NEW)
- ✅ `database/SNAPSHOT_FIX_README.md` - This documentation (NEW)
- ✅ `database/apply_migration_005.py` - Migration helper script (NEW)

## Related Issues

This fixes:
- Budget revision snapshots not appearing in history panel
- Contract acceptance snapshots potentially not being created
- Silent failures in snapshot creation (function executes but no data inserted)

## Next Steps

1. **Apply the migration** using Method 1 or 2 above
2. **Test snapshot creation** for both contracts and budget revisions
3. **Update project plan** to mark snapshot creation as fully working
4. **Optional:** Add monitoring/logging to catch similar RLS issues in the future

## Questions?

If snapshot creation still fails after applying this migration, check:
1. Migration was applied successfully (run verification query above)
2. Backend logs for any error messages
3. Supabase logs in the Dashboard → Logs section
4. RLS policies haven't been modified since applying the fix
