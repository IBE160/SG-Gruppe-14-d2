# Database Inconsistency Report
## Nye Hædda Barneskole - Supabase vs localStorage Documentation

**Report Date:** 2025-12-13
**Auditor:** Documentation Consistency Check
**Status:** CRITICAL INCONSISTENCIES FOUND
**Priority:** HIGH - Requires immediate fixes

---

## Executive Summary

**CRITICAL FINDING:** The repository documentation contains **major inconsistencies** regarding data storage architecture. The SCOPE_CHANGE_TASKS.md document (Section 5, lines 278-537) clearly states that the project has migrated from localStorage to **Supabase Database**, but ALL other documentation files still reference localStorage as the primary storage mechanism.

**Impact:** HIGH
- Developers following the documentation will implement the wrong architecture
- Technical specifications are inconsistent across documents
- Implementation plans reference outdated storage mechanism

**Required Action:** Update ALL documentation files to reflect Supabase Database usage instead of localStorage

---

## Database Architecture Change (Per SCOPE_CHANGE_TASKS.md)

### What Changed:
**OLD Architecture:**
- All data stored in browser localStorage
- User credentials in localStorage
- Game sessions in localStorage
- Negotiation history in localStorage
- Maximum storage: 5 MB browser limit

**NEW Architecture (Current):**
- **Supabase PostgreSQL database** for all data persistence
- **Supabase Auth** for JWT-based authentication
- Game sessions stored in `game_sessions` table
- WBS commitments stored in `wbs_commitments` table
- Negotiation history stored in `negotiation_history` table
- User data managed by Supabase Auth (auth.users table)

### Why This Matters:
✅ Persistent storage across devices and browser sessions
✅ Secure authentication with JWT tokens
✅ Multi-user support with proper user isolation
✅ Data integrity with relational database constraints
✅ Scalability for future features (leaderboards, multiplayer, etc.)

---

## Inconsistency Analysis

### Files with CORRECT Information (Supabase):
1. ✅ **SCOPE_CHANGE_TASKS.md** - Section 5 fully documents Supabase integration
2. ✅ **Backend code** (`backend/config.py`, `backend/main.py`) - Already implements Supabase
3. ✅ **Frontend package.json** - Supabase libraries installed (`@supabase/supabase-js`, `@supabase/ssr`)
4. ✅ **Functional flows SVG** (`flow-05-state-management.svg`) - Shows "DATABASE (Supabase)" with PostgreSQL

### Files with INCORRECT Information (localStorage):
The following files still reference localStorage and need to be updated:

#### 1. README.md
**Line 94:**
```markdown
**CURRENT (WRONG):**
- **Storage:** localStorage (browser-based, no database)

**SHOULD BE:**
- **Storage:** Supabase PostgreSQL database (user auth + game sessions + negotiation history)
- **Auth:** Supabase Auth (JWT-based)
```

**Impact:** HIGH - This is the first file developers/stakeholders read

---

#### 2. product-brief.md
**Line 152:**
```markdown
**CURRENT (WRONG):**
- **Storage:** localStorage (browser-based, no database)

**SHOULD BE:**
- **Storage:** Supabase PostgreSQL database
```

**Lines 157-161:**
```markdown
**CURRENT (WRONG):**
**Why localStorage?**
- Single-session focus (45-60 min)
- No cross-device resume needed (export-first design)
- Saves 1-2 weeks development time (no database setup)
- 5 MB limit sufficient for 40+ sessions (current usage: 62 KB)

**SHOULD BE REMOVED OR REPLACED WITH:**
**Why Supabase Database?**
- Persistent storage across devices and browser sessions
- Secure user authentication with JWT
- Data integrity and relational constraints
- Enables future features (leaderboards, analytics, multiplayer)
- Professional database solution for production readiness
```

**Impact:** HIGH - Stakeholder-facing document

---

#### 3. epics.md
**Multiple occurrences throughout**

**Line 90:**
```markdown
**CURRENT (WRONG):**
- Store JWT in localStorage: `supabase_auth_token`

**SHOULD BE:**
- JWT managed by Supabase Auth (stored securely, NOT in localStorage for security reasons)
```

**Lines 136-159 (Story E1.3: Session Initialization):**
```markdown
**CURRENT (WRONG):**
- [ ] On Dashboard load, check localStorage for `current_session_id`
- [ ] If session exists → load session data from localStorage
- [ ] If no session → create new session with:
  - Save session to localStorage
- localStorage key: `nye_haedda_session_{user_id}`
- Load static files: `/data/wbs.json`, `/data/suppliers.json`

**SHOULD BE:**
- [ ] On Dashboard load, check Supabase database for active session
- [ ] If session exists → load session data from `game_sessions` table
- [ ] If no session → create new session in database with:
  - INSERT INTO game_sessions (user_id, status, total_budget...)
  - Save session to Supabase database
- Database table: `game_sessions` with user_id foreign key
- Load static files: `/data/wbs.json`, `/data/agents.json`
```

**Lines 208-215 (Story E2.2: Real-Time Budget Updates):**
```markdown
**CURRENT (WRONG):**
- [ ] When user commits quote → `current_plan` updated in localStorage
- Use React state + localStorage sync

**SHOULD BE:**
- [ ] When user commits quote → `wbs_commitments` table updated in Supabase
- Use React state + Supabase realtime subscriptions OR API polling
```

**Lines 468-496 (Story E4.1 & E4.2: Chat Interface):**
```markdown
**CURRENT (WRONG):**
- Messages: Array in React state, persisted to localStorage
- Store message in `session.chat_logs` (localStorage)

**SHOULD BE:**
- Messages: Array in React state, persisted to `negotiation_history` table
- INSERT INTO negotiation_history (session_id, wbs_id, agent_id, user_message, agent_response...)
```

**Lines 579-584 (Story E4.5: Negotiation History Persistence):**
```markdown
**CURRENT (WRONG):**
- [ ] All messages stored in `session.chat_logs` array
- [ ] When reopening chat → load history from localStorage
- localStorage update on every message send/receive

**SHOULD BE:**
- [ ] All messages stored in `negotiation_history` table
- [ ] When reopening chat → load history from Supabase (SELECT * FROM negotiation_history WHERE session_id = ?)
- Database INSERT on every message send/receive
```

**Lines 714, 990, 1017-1024, 1042-1043 (Stories E5.1, E7.1, E7.2, E7.3):**
All localStorage references should be replaced with Supabase database operations.

**Impact:** CRITICAL - This is the implementation guide for developers

---

#### 4. PRD.md (Product Requirements Document)
**Multiple occurrences throughout**

Based on grep results, PRD.md has ~20+ localStorage mentions including:
- Line 289: "load from localStorage"
- Line 515: "updated to 'completed' in localStorage"
- Line 634: "creates new session object in localStorage"
- Line 652: "session created in localStorage"
- Line 672-675: Auto-save to localStorage
- Line 955: "saves session to localStorage"
- Line 1069: "updated to 'completed' in localStorage"
- Line 1119: "stored efficiently in browser localStorage"
- Line 1489: "must fit within localStorage limits (5 MB per domain)"
- Line 1537: "stored in user's own browser (localStorage)"
- Line 1640: "Session Data: localStorage (direct read/write, no library needed)"
- Line 2289: "Session initialization and persistence (localStorage)"
- Line 2447: "Stored in `session.current_plan` in localStorage"

**All should be replaced with Supabase database operations**

**Impact:** CRITICAL - Core requirements document

---

#### 5. ux-design-specification.md
**Line 152, 468, 496, 579, 584, 714, 990, 1306, 1397, 1444, 1607 (from grep results)**

All localStorage UI/UX implementation notes should reference Supabase database operations instead.

**Impact:** HIGH - Frontend implementation guide

---

#### 6. Brainstorming Documents
**Files with localStorage mentions (from grep):**
- `brainstorming-executive-summary.md` - Multiple occurrences
- `brainstorming-session-core-functionality-and-scope-2025-12-07.md` - Extensive localStorage schema design
- `brainstorming-technical-architecture-report.md` - Line 30 mentions "browser storage" context

**Impact:** MEDIUM - Historical documents, but should have update notes

---

#### 7. Implementation Plans
**Files:**
- `IMPLEMENTATION_PLAN_DEC_9-15.md` - References localStorage and sessionStorage
- `REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md` - Lines 36, 141, 150 reference localStorage/Zustand store

**Impact:** HIGH - Active implementation guides

---

#### 8. Test Design
**File:** `test-design.md`
- Line 268: "loaded from localStorage"

**Impact:** MEDIUM - Test specifications

---

#### 9. Consistency Audit Report (Dec 7)
**File:** `consistency-audit-report-2025-12-07.md`
- This audit APPROVED the localStorage → Supabase change but was dated Dec 7
- Later documents reverted to localStorage mentions
- Lines 24, 53, 56, 99-127 document the architecture change

**Impact:** LOW - Historical audit, but shows the change was approved

---

## Database Schema (From SCOPE_CHANGE_TASKS.md)

The following tables should be referenced in documentation instead of localStorage:

### 1. `users` (Managed by Supabase Auth)
- `id` (UUID, primary key)
- `email` (unique)
- `encrypted_password`
- `created_at`, `updated_at`

### 2. `game_sessions`
```sql
CREATE TABLE game_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_name VARCHAR(255),
  status VARCHAR(50) DEFAULT 'in_progress',

  total_budget DECIMAL(10, 2) DEFAULT 700.00,
  locked_budget DECIMAL(10, 2) DEFAULT 390.00,
  available_budget DECIMAL(10, 2) DEFAULT 310.00,
  current_budget_used DECIMAL(10, 2) DEFAULT 0.00,

  deadline_date DATE DEFAULT '2026-05-15',
  projected_completion_date DATE,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);
```

### 3. `wbs_commitments`
```sql
CREATE TABLE wbs_commitments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES game_sessions(id) ON DELETE CASCADE,
  wbs_id VARCHAR(50) NOT NULL,
  wbs_name VARCHAR(255),

  supplier_agent_id VARCHAR(100),
  committed_cost DECIMAL(10, 2),
  committed_duration_days INTEGER,
  committed_at TIMESTAMP DEFAULT NOW(),

  negotiation_rounds INTEGER DEFAULT 0,
  quality_reduced BOOLEAN DEFAULT false,
  scope_reduced BOOLEAN DEFAULT false,

  UNIQUE(session_id, wbs_id)
);
```

### 4. `negotiation_history`
```sql
CREATE TABLE negotiation_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES game_sessions(id) ON DELETE CASCADE,
  wbs_id VARCHAR(50),
  agent_id VARCHAR(100),
  agent_type VARCHAR(50),

  user_message TEXT,
  agent_response TEXT,

  offer_cost DECIMAL(10, 2),
  offer_duration_days INTEGER,
  offer_accepted BOOLEAN DEFAULT false,

  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints (From SCOPE_CHANGE_TASKS.md)

Documentation should reference these endpoints instead of localStorage operations:

**Game Sessions:**
- `POST /api/sessions` - Create new game session
- `GET /api/sessions` - List user's game sessions
- `GET /api/sessions/:id` - Get specific session details
- `PUT /api/sessions/:id` - Update session (budget, timeline)
- `DELETE /api/sessions/:id` - Delete session

**WBS Commitments:**
- `POST /api/sessions/:id/commitments` - Commit to a WBS package
- `GET /api/sessions/:id/commitments` - Get all commitments for session
- `PUT /api/sessions/:id/commitments/:wbs_id` - Update commitment
- `DELETE /api/sessions/:id/commitments/:wbs_id` - Remove commitment

**Negotiation:**
- `POST /api/sessions/:id/negotiate` - Send message to AI agent, get response
- `GET /api/sessions/:id/history` - Get negotiation history
- `POST /api/sessions/:id/accept-offer` - Accept an offer from agent

**Validation:**
- `POST /api/sessions/:id/validate` - Validate current plan (budget, timeline)

---

## Security Implications

**CRITICAL:** Documentation currently shows JWT stored in localStorage, which is a security vulnerability (XSS attacks).

**WRONG (from epics.md line 90):**
```
Store JWT in localStorage: `supabase_auth_token`
```

**CORRECT:**
```
JWT managed by Supabase Auth client library (stored securely in memory or httpOnly cookies)
Never store JWT in localStorage due to XSS vulnerability
```

---

## Recommended Fixes

### Priority 1 (CRITICAL - Must Fix Immediately):
1. **README.md** - Line 94: Change storage description to Supabase
2. **product-brief.md** - Lines 152-161: Update storage architecture section
3. **epics.md** - All localStorage references (20+ occurrences): Replace with Supabase database operations
4. **PRD.md** - All localStorage references (20+ occurrences): Replace with Supabase database operations

### Priority 2 (HIGH - Fix This Week):
5. **ux-design-specification.md** - Update implementation notes with Supabase
6. **IMPLEMENTATION_PLAN_DEC_9-15.md** - Replace localStorage logic with database operations
7. **REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md** - Update Zustand store to use Supabase client
8. **test-design.md** - Update test cases to verify database operations

### Priority 3 (MEDIUM - Fix When Possible):
9. **Brainstorming documents** - Add update notes indicating localStorage was replaced by Supabase
10. **consistency-audit-report-2025-12-07.md** - Add note that this audit is historical

---

## Additional Database Use Cases

Based on the Supabase database capabilities, here are additional use cases that should be considered:

### 1. **User Analytics & Progress Tracking**
**Tables to add:**
```sql
CREATE TABLE user_analytics (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  session_id UUID REFERENCES game_sessions(id),

  total_sessions_played INTEGER DEFAULT 0,
  total_sessions_completed INTEGER DEFAULT 0,
  average_budget_accuracy DECIMAL(5, 2), -- % within target
  average_negotiation_rounds DECIMAL(5, 2),
  best_completion_time_minutes INTEGER,

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Track student learning progress over multiple sessions

---

### 2. **Leaderboard System**
**Tables to add:**
```sql
CREATE TABLE leaderboard (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  user_display_name VARCHAR(255),

  best_budget_efficiency DECIMAL(10, 2), -- MNOK under baseline
  best_time_minutes INTEGER,
  total_successful_negotiations INTEGER,

  ranking_score DECIMAL(10, 2), -- Calculated metric
  created_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Gamification for classroom competitions

---

### 3. **Session Templates & Scenarios**
**Tables to add:**
```sql
CREATE TABLE session_templates (
  id UUID PRIMARY KEY,
  template_name VARCHAR(255),
  description TEXT,
  difficulty_level VARCHAR(50), -- 'easy', 'medium', 'hard'

  total_budget DECIMAL(10, 2),
  available_budget DECIMAL(10, 2),
  baseline_cost DECIMAL(10, 2),
  deadline_months INTEGER,

  wbs_configuration JSONB, -- Which WBS items are negotiable
  agent_difficulty_settings JSONB,

  created_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Instructors can create different difficulty scenarios

---

### 4. **Multi-User/Classroom Management**
**Tables to add:**
```sql
CREATE TABLE classrooms (
  id UUID PRIMARY KEY,
  classroom_name VARCHAR(255),
  instructor_user_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE classroom_members (
  id UUID PRIMARY KEY,
  classroom_id UUID REFERENCES classrooms(id),
  student_user_id UUID REFERENCES auth.users(id),
  enrolled_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(classroom_id, student_user_id)
);
```

**Use Case:** Instructors track student progress across a class

---

### 5. **AI Agent Performance Tracking**
**Tables to add:**
```sql
CREATE TABLE agent_performance_metrics (
  id UUID PRIMARY KEY,
  agent_id VARCHAR(100), -- e.g., 'bjorn_eriksen', 'owner_anne_lise'

  total_negotiations INTEGER DEFAULT 0,
  successful_deals INTEGER DEFAULT 0,
  average_concession_percentage DECIMAL(5, 2),
  average_rounds_to_deal DECIMAL(5, 2),

  updated_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Monitor AI agent realism and tune system prompts

---

### 6. **Session Snapshots/Versioning**
**Tables to add:**
```sql
CREATE TABLE session_snapshots (
  id UUID PRIMARY KEY,
  session_id UUID REFERENCES game_sessions(id),
  snapshot_version INTEGER,

  budget_snapshot JSONB,
  commitments_snapshot JSONB,
  timeline_snapshot JSONB,

  created_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Allow users to review past versions of their plan (undo/redo, history view)

---

### 7. **Export/Import Session Data**
**Current:** Export session as JSON file (local download)
**Enhanced:** Store exported sessions in database for later re-import

```sql
CREATE TABLE exported_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  original_session_id UUID,
  export_name VARCHAR(255),
  session_data JSONB,
  exported_at TIMESTAMP DEFAULT NOW()
);
```

**Use Case:** Cross-device session resume, sharing sessions with instructors

---

## Summary

**Total Files Needing Updates:** 9 critical files + 3 medium priority
**Total localStorage References:** 100+ occurrences across all files
**Estimated Fix Time:** 8-12 hours for all Priority 1 & 2 fixes

**Critical Action Required:**
All documentation must be updated to reflect the Supabase database architecture. The current localStorage references are misleading and will cause implementation errors.

**Database Architecture is CONFIRMED:**
- Backend already implements Supabase (config.py, main.py)
- Frontend has Supabase libraries installed (package.json)
- Database schema is documented in SCOPE_CHANGE_TASKS.md
- The change is approved and final

---

**End of Report**

**Next Steps:**
1. Review this report with stakeholders
2. Approve the fix plan
3. Begin systematic documentation updates (README.md first)
4. Verify all changes against SCOPE_CHANGE_TASKS.md Section 5
5. Re-run consistency audit after fixes
