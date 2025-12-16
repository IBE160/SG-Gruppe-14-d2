# Import Database to Supabase - Step-by-Step Guide

## ⚡ Quick Start (2 Minutes)

### Step 1: Open Supabase SQL Editor

1. Go to your Supabase project: https://supabase.com/dashboard
2. Select your project: **cmntglldaqrekloixxoc** (or your project name)
3. Click **"SQL Editor"** in the left sidebar
4. Click **"New query"** button

### Step 2: Copy the Complete SQL File

1. Open the file: `database/migrations/001_complete_schema.sql`
2. Select all content (`Ctrl+A`)
3. Copy (`Ctrl+C`)

### Step 3: Paste and Execute

1. Paste into Supabase SQL Editor (`Ctrl+V`)
2. Click **"Run"** button (or press `Ctrl+Enter`)
3. Wait 5-10 seconds for completion

### Step 4: Verify Installation

Run this query to check all tables were created:

```sql
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
```

**Expected result:** 5 rows (all 5 tables)

---

## ✅ What Gets Created Automatically

### 1. **5 Database Tables**

| Table | Purpose | Key Features |
|-------|---------|--------------|
| `game_sessions` | Track each game | 3-tier budget, computed columns |
| `wbs_commitments` | Package commitments | Auto-calculated savings |
| `negotiation_history` | Chat messages | Offer detection, disagreements |
| `agent_timeouts` | Agent lockouts | 10-minute timeout mechanic |
| `user_analytics` | Leaderboards | User statistics |

### 2. **Computed Columns** (Auto-Calculated)

- `budget_tier1_percentage` - % of available budget used
- `budget_tier3_total` - Total budget used (locked + negotiable)
- `budget_remaining` - Money left to spend
- `savings` - Money saved from baseline
- `savings_percentage` - % saved from baseline
- `is_timeline_valid` - Whether project meets deadline

### 3. **Row-Level Security (RLS)**

All tables are secured so users can ONLY see their own data.

**Example:** User A cannot see User B's game sessions.

### 4. **Triggers**

- Auto-update `updated_at` timestamp when rows change
- Auto-update session budget when commitments are created

### 5. **Indexes**

Optimized for fast queries on:
- User lookups
- Session searches
- Agent filtering
- Timeline sorting

### 6. **Helper Views**

- `active_sessions_summary` - Quick overview of active games
- `leaderboard` - Rankings by savings

---

## 🔍 Verification Tests

### Test 1: Check RLS is Enabled

```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'game_sessions',
    'wbs_commitments',
    'negotiation_history',
    'agent_timeouts',
    'user_analytics'
  );
```

**Expected:** All 5 tables should show `rowsecurity = true`

### Test 2: Check Indexes Exist

```sql
SELECT tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
    'game_sessions',
    'wbs_commitments',
    'negotiation_history',
    'agent_timeouts',
    'user_analytics'
  )
ORDER BY tablename, indexname;
```

**Expected:** Multiple indexes per table (15+ total)

### Test 3: Check Triggers Exist

```sql
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE event_object_schema = 'public'
ORDER BY event_object_table;
```

**Expected:** At least 2 triggers (update_updated_at triggers)

---

## 📊 Database Structure Visual

```
Supabase PostgreSQL Database
│
├── public.game_sessions (main table)
│   ├── Computed: budget_tier1_percentage
│   ├── Computed: budget_tier3_total
│   ├── Computed: budget_remaining
│   └── Computed: is_timeline_valid
│
├── public.wbs_commitments
│   ├── Computed: savings
│   └── Computed: savings_percentage
│
├── public.negotiation_history (chat logs)
│
├── public.agent_timeouts (lockout tracking)
│
└── public.user_analytics (leaderboards)
```

---

## 🛡️ Security Features

### Row-Level Security Policies

✅ **Users can only access their own data**

```sql
-- Example: game_sessions RLS
CREATE POLICY "Users can view their own sessions"
ON game_sessions FOR SELECT
USING (auth.uid() = user_id);
```

**Result:** User with ID `abc123` can ONLY see sessions where `user_id = 'abc123'`

### Constraints Prevent Invalid Data

✅ **Budget cannot exceed limits**
```sql
CHECK (current_budget_used <= available_budget)
CHECK ((locked_budget + current_budget_used) <= total_budget)
```

✅ **Only valid WBS IDs allowed**
```sql
CHECK (wbs_id IN ('1.3.1', '1.3.2', '1.4.1'))
```

✅ **Only valid agent types**
```sql
CHECK (agent_type IN ('owner', 'supplier'))
```

---

## 🎯 Budget Constants Reference

| Constant | Value (MNOK) | Value (NOK) | Purpose |
|----------|--------------|-------------|---------|
| Total Budget | 700 | 700,000,000.00 | Maximum project budget |
| Locked Budget | 390 | 390,000,000.00 | 12 non-negotiable packages |
| Available Budget | 310 | 310,000,000.00 | 3 negotiable packages |
| Baseline Total | 345 | 345,000,000.00 | Initial estimates (too high!) |
| **Deficit** | **35** | **35,000,000.00** | **Must save this much** |

---

## 🚨 Troubleshooting

### Issue: "relation already exists"

**Cause:** Tables already created from previous run.

**Solution:** Drop tables first (WARNING: deletes all data!)

```sql
DROP TABLE IF EXISTS public.agent_timeouts CASCADE;
DROP TABLE IF EXISTS public.negotiation_history CASCADE;
DROP TABLE IF EXISTS public.wbs_commitments CASCADE;
DROP TABLE IF EXISTS public.user_analytics CASCADE;
DROP TABLE IF EXISTS public.game_sessions CASCADE;

DROP VIEW IF EXISTS active_sessions_summary;
DROP VIEW IF EXISTS leaderboard;
```

Then re-run the migration.

### Issue: "permission denied"

**Cause:** Not logged in or insufficient permissions.

**Solution:** Ensure you're the project owner or have admin access.

### Issue: RLS blocking all queries

**Cause:** RLS is enabled but you're not authenticated.

**Solution:**
- For testing, you can temporarily disable RLS (NOT in production!):
  ```sql
  ALTER TABLE game_sessions DISABLE ROW LEVEL SECURITY;
  ```
- Or ensure you're querying with an authenticated user via Supabase client.

---

## 📝 Next Steps After Import

1. ✅ **Verify all tables created** (run verification queries above)
2. ✅ **Test RLS policies** (try creating a test session)
3. ✅ **Connect backend API** (configure Supabase client in FastAPI)
4. ✅ **Connect frontend** (already configured with Supabase client)

---

## 🔗 Important Files

| File | Purpose |
|------|---------|
| `database/migrations/001_complete_schema.sql` | **Main import file** (use this!) |
| `docs/DATABASE_IMPLEMENTATION_GUIDE.md` | Full documentation |
| `backend/.env.local` | Supabase URL and keys |
| `frontend/.env.local` | Frontend Supabase config |

---

## ✨ You're Done!

After running the SQL import, your Supabase database is **100% configured** and ready for:
- ✅ Backend API to read/write data
- ✅ Frontend to query data
- ✅ User authentication and RLS
- ✅ All game mechanics (budget, timeouts, analytics)

**No additional database configuration needed!**

---

**For questions:** Refer to `docs/DATABASE_IMPLEMENTATION_GUIDE.md` for detailed documentation.
