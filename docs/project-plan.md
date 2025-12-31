# Project Plan

## Instructions

1. Where you see {prompt / user-input-file}, you can add your own prompt or filename to provide extra instructions. If you don't wish to add anything, you can remove this part.
2. If a prompt is already written, e.g., "Root Cause Analysis...", feel free to replace it with your own.

---

## 📊 Executive Summary (Updated: December 31, 2025)

### Project Status: **MVP-READY - 99% COMPLETE** ✅

The PM Simulator project has successfully implemented core functionality and is **ready for classroom demonstrations**. The application features a working AI-powered negotiation system, full authentication, budget tracking, data persistence, critical path calculation, fully functional Gantt chart and Precedence diagram visualizations, stable offer acceptance flow, and **complete snapshot system with history/timeline view**. Users can now view project state at any point in time, compare different snapshots, and see how decisions impacted the timeline via Gantt and Precedence diagrams. The core application is stable.

**Recent Completions (December 30-31, 2025):**

- ✅ Authentication fix - Replaced debug bypass with proper `supabase.auth.get_user()` validation
- ✅ Dependency validation - Prevents commits without completing prerequisites (backend/main.py:610-635)
- ✅ Timeline validation - Blocks commits that make project late (backend/main.py:659-703)
- ✅ Baseline snapshot - Client-side workaround generates virtual baseline (history-panel.tsx:118-169)
- ✅ Snapshot system fixes - Fixed database constraints, type conversions, and timeline format consistency (December 31, 2025)
- ✅ History/Timeline View - Full end-to-end snapshot creation, storage, and visualization working (December 31, 2025)

**Only 1 critical feature remains for MVP (6-8 hours total):**

1. Owner perspective budget revision acceptance (6-8 hours) - **See detailed implementation plan below**

All other remaining items are nice-to-have enhancements.

---

### ⚠️ Known Issues

**No critical issues at this time.**

**Recently Resolved:**

- ✅ **Authentication Validation (Fixed: December 31, 2025)** - Resolved JWT validation issue. The temporary debug bypass code in `backend/main.py` `get_current_user()` function has been replaced with proper Supabase Auth API validation using `supabase.auth.get_user(token.credentials)`. Authentication now works correctly for all users without bypassing security.
- ✅ **Snapshot System Database Errors (Fixed: December 31, 2025)** - Resolved three critical issues preventing snapshot creation:
  1. Budget total constraint violation - Fixed hardcoded value in database function from 700000000 (7 MNOK) to 70000000000 (700 MNOK) to match CHECK constraint
  2. Integer type error - Added int() conversion for duration before passing to database (backend/main.py:745)
  3. Timeline format mismatch - Converted frontend baseline timeline format to match backend format for consistency (history-panel.tsx:131-169)
- ✅ **AI Agent Offer Format (Fixed: December 31, 2025)** - Updated all three vendor agent prompts (Bjørn Eriksen, Kari Andersen, Per Johansen) with CRITICAL RULE requiring confirmation of both cost AND duration before giving formal offers, ensuring offer detection works correctly (docs/AI_AGENT_SYSTEM_PROMPTS.md)

---

### What's Working ✅

**Complete & Operational:**

1. ✅ **Core Application Stability** - The main user flow, from login and session creation to negotiation and offer acceptance, is now stable after extensive debugging.
2. ✅ **User Authentication** - Full Supabase auth with email/password, registration, login, password reset, protected routes. The code uses the correct API-based validation.
3. ✅ **Dashboard** - 3-tier budget visualization (310/390/700 MNOK), WBS package listing, agent panels, tabbed interface.
4. ✅ **AI Negotiation** - Real-time chat with 4 AI agents using Gemini 2.5 Flash, context injection, Norwegian responses.
5. ✅ **Offer Management** - Automatic regex-based offer detection, accept/reject buttons, budget impact preview.
6. ✅ **Budget Tracking** - Real-time updates, validation (≤700 MNOK), duplicate prevention, tier calculations.
7. ✅ **Data Persistence** - Sessions, commitments, and negotiation history saved with RLS policies enforced.
8. ✅ **Chat History Persistence** - Fixed session resumption bug, conversations now correctly load when switching between agents.
9. ✅ **Backend API** - 14 RESTful endpoints, JWT auth, proper error handling, Norwegian error messages.
10. ✅ **Design System** - Professional UI with Tailwind CSS, Shadcn components, complete color palette.
11. ✅ **Static Data** - Complete WBS (15 items) and agent configs (4 agents) with full metadata.
12. ✅ **Documentation** - 50+ comprehensive docs (PRD v2.2, architecture, test plans, troubleshooting, UX specs).
13. ✅ **Critical Path Algorithm** - Full CPM implementation (ES/EF/LS/LF, slack time, critical path identification).
14. ✅ **Database Schema** - 6 tables with triggers, RLS policies, computed columns, indexes, snapshot system.
15. ✅ **Session Completion Flow** - Implemented completion page with results summary and success/error modals.
16. ✅ **Gantt Chart** - Fully functional timeline visualization with critical path highlighting, dependency arrows, and dynamic date calculations based on commitments.
17. ✅ **Precedence Diagram (AON)** - Complete Activity-on-Node network with ReactFlow, ES/EF/LS/LF display, slack calculations, persistent layout (saves positions to localStorage), and reset functionality.
18. ✅ **Shared Timeline Calculator** - Single source of truth for time calculations across all visualizations, dynamically updates based on committed/locked/baseline durations.
19. ✅ **Backend Validation Endpoint** - Fixed /validate endpoint, correctly loads WBS data and provides timeline calculations.
20. ✅ **History/Timeline View** - Complete snapshot visualization system with 3 tabs (Overview/Gantt/Precedence), displays all contract acceptances chronologically, allows comparison of project state at different points in time, includes virtual baseline snapshot showing initial 12 locked contracts.
21. ✅ **Snapshot System** - Auto-creation on vendor contract acceptance, stores complete timeline data (earliest_start/finish, latest_start/finish, slack, critical_path) in JSONB format, version auto-increment trigger, budget state tracking, enables full reconstruction of Gantt and Precedence diagrams at any point in project history.

### What's Partially Working 🟡

**In Progress (40% complete):**

1. 🟡 **Owner Perspective** (40%) - User can chat with owner agent (Anne-Lise Berg), but budget revision acceptance is NOT implemented (no UI button, no backend endpoint, no snapshot creation)

### What's Missing ❌

**Critical for MVP:**

1. ❌ **Owner Perspective Budget Revision** - No UI to accept revised budgets from owner agent, no backend endpoint, no snapshot creation (est: 6-8 hours)

**Recently Completed:**

1. ✅ **History Panel Baseline Snapshot** - COMPLETE via client-side workaround. The frontend now generates a virtual baseline snapshot with backend-compatible format.
2. ✅ **Dependency Validation** - COMPLETE. Users can no longer commit to packages before prerequisites are complete.
3. ✅ **Timeline Validation** - COMPLETE. Users can no longer accept offers that make the project late.
4. ✅ **Snapshot System End-to-End** - COMPLETE. Snapshots are auto-created on contract acceptance, stored with complete timeline data, and displayed in History panel with Gantt/Precedence reconstruction.

**Nice to Have (Future Enhancements):**
6. ❌ **Renegotiation/Uncommit** - Cannot reverse accepted offers, no DELETE endpoint (est: 3-4 hours)
7. ❌ **Export Functionality** - Session/history export endpoint exists, needs frontend UI button (est: 2-3 hours)
8. ❌ **Agent Timeout UI** - No visual countdown for 6-disagreement mechanic (detection works, UI missing) (est: 3 hours)
9. ⚠️ **Mobile Responsiveness** - Desktop-optimized only, limited mobile support (est: 8-12 hours)
10. ❌ **Automated Testing** - No test suite (unit/integration/E2E) (est: 40+ hours)
11. ❌ **Administration Panel** - Teacher/admin dashboard to view all student sessions and results from database (est: 12-16 hours)

---

## 🤝 Contract & Budget Acceptance System - Technical Deep Dive

### ✅ Vendor Contract Acceptance (FULLY IMPLEMENTED)

**Complete 12-Step Data Flow:**

1. **User receives offer** from vendor agent (Bjørn Eriksen, Cathrine Lund, or David Hansen) in chat
2. **Offer detection** via regex parser in chat interface (detects cost, duration, quality)
3. **OfferBox UI renders** with "✓ Godta tilbud" (Accept) and "✗ Avslå" (Reject) buttons
4. **User clicks Accept** → triggers `handleOfferAccepted()` in game page
5. **API call** `POST /api/sessions/{sessionId}/commitments` with offer data:
   ```typescript
   {
     wbs_id: string,           // "1.3.1"
     wbs_name: string,         // "Grunnarbeid"
     agent_id: string,         // "bjorn-eriksen"
     baseline_cost: number,    // Original estimate (øre)
     negotiated_cost: number,  // Agreed price (øre)
     committed_cost: number,   // Final commitment (øre)
     baseline_duration: number,    // Original months
     negotiated_duration: number,  // Agreed months
     quality_level: string     // "budget" | "standard" | "premium"
   }
   ```
6. **Backend validation** (budget ≤ 700 MNOK, no duplicates, valid WBS ID)
7. **Database INSERT** into `wbs_commitments` table (15 fields saved)
8. **Session UPDATE** increments `current_budget_used` in `game_sessions`
9. **Critical path recalculation** via CPM algorithm with updated commitments
10. **Snapshot auto-creation** via `create_contract_snapshot()` database function
11. **Snapshot data saved** (version auto-incremented, timeline states stored as JSONB)
12. **Frontend redirect** to dashboard showing updated budget and commitment list

**Key Database Changes:**

- ✅ `wbs_commitments` table: New row with all contract details
- ✅ `game_sessions.current_budget_used`: Incremented by committed_cost
- ✅ `session_snapshots` table: New snapshot with version N+1

**Snapshot Contains (for History Pane Reconstruction):**

- ✅ Budget state: `budget_committed`, `budget_available`, `budget_total`
- ✅ Contract details: `contract_wbs_id`, `contract_cost`, `contract_duration`, `contract_supplier`
- ✅ Project timeline: `project_end_date`, `days_before_deadline`
- ✅ **Gantt state (JSONB)**: Complete timeline with `earliest_start`, `earliest_finish` dates for ALL 15 WBS items
- ✅ **Precedence state (JSONB)**: Complete timeline with `earliest_start`, `earliest_finish`, `latest_start`, `latest_finish`, `slack` for ALL 15 WBS items
- ✅ Metadata: `version`, `label`, `snapshot_type`, `timestamp`

**History Pane Can Display:**

- ✅ Timeline sidebar with all snapshots (paginated, 10 per page)
- ✅ Snapshot cards showing version, contract details, date
- ✅ **Gantt chart reconstruction** from `gantt_state` JSONB (shows project timeline at that moment)
- ✅ **Precedence diagram reconstruction** from `precedence_state` JSONB (shows ES/EF/LS/LF at that moment)
- ✅ Budget overview with committed/available/total amounts
- ✅ Timeline info with project end date and deadline delta
- ✅ Export all snapshots to JSON

**Files Involved:**

- `frontend/components/chat-interface.tsx` - OfferBox component with Accept button
- `frontend/app/game/[sessionId]/[agentId]/[wbsId]/page.tsx` - handleOfferAccepted()
- `frontend/lib/api/sessions.ts` - createCommitment() API client
- `backend/main.py` - create_commitment() endpoint (lines 602-806)
- `database/migrations/001_complete_schema.sql` - wbs_commitments table
- `database/migrations/002_session_snapshots.sql` - session_snapshots table + triggers
- `frontend/components/history-panel.tsx` - History UI with Gantt/Precedence tabs
- `frontend/components/gantt-chart.tsx` - Gantt reconstruction from snapshot
- `frontend/components/precedence-diagram.tsx` - Precedence reconstruction from snapshot

---

### 🟡 Baseline Snapshot Virtual Implementation (90% COMPLETE)

**Design Decision:**

- Baseline snapshot is **NOT stored in database** (deliberate design choice for simplicity and security)
- Frontend calculates baseline state **on-demand** from wbs.json (12 locked contracts)
- Shows initial state: 390 MNOK committed, 310 MNOK available, 700 MNOK total

**What Currently Works:**

- ✅ wbs.json contains complete data for all 15 WBS items (12 locked + 3 negotiable)
- ✅ Locked items marked with `is_locked: true` flag
- ✅ Shared timeline calculator can generate baseline timeline from locked items
- ✅ History panel UI exists and can display snapshots with 3 tabs (Overview/Gantt/Precedence)
- ✅ History panel correctly renders contract acceptance snapshots from database

**What's Missing:**

- ❌ **No baseline "virtual" snapshot** created in frontend
- ❌ Baseline not shown as version 0 in history timeline sidebar
- ❌ Users cannot see the starting point (12 pre-negotiated contracts) in history view

**Implementation Approach (1-2 hours):**

1. **Create baseline snapshot generator** in `history-panel.tsx`:

   ```typescript
   function createBaselineSnapshot(): Snapshot {
     // Filter locked items from wbs.json
     const lockedItems = wbsItems.filter(item => item.is_locked);

     // Calculate baseline timeline using shared timeline calculator
     const baselineTimeline = calculateTimeline(lockedItems, []);

     return {
       id: 'baseline-virtual',
       session_id: sessionId,
       version: 0,
       label: 'Baseline: 12 Forhåndsinngåtte Kontrakter',
       snapshot_type: 'baseline',
       budget_committed: 39000000000, // 390 MNOK in øre
       budget_available: 31000000000, // 310 MNOK in øre
       budget_total: 70000000000, // 700 MNOK in øre
       contract_wbs_id: null,
       contract_cost: null,
       contract_duration: null,
       contract_supplier: null,
       project_end_date: baselineTimeline.projectEndDate,
       days_before_deadline: baselineTimeline.daysBeforeDeadline,
       gantt_state: baselineTimeline,
       precedence_state: baselineTimeline,
       timestamp: new Date().toISOString(),
       created_at: new Date().toISOString(),
     };
   }
   ```
2. **Modify loadSnapshots()** to prepend virtual baseline:

   ```typescript
   async function loadSnapshots(offset: number, limit: number) {
     // Load database snapshots
     const data = await fetchSnapshotsFromAPI();

     // If first load, add virtual baseline at the beginning
     if (offset === 0) {
       const baseline = createBaselineSnapshot();
       setSnapshots([baseline, ...data.snapshots]);
       setSelectedSnapshot(baseline); // Show baseline by default
     } else {
       setSnapshots(prev => [...prev, ...data.snapshots]);
     }

     setTotalCount(data.total_count + 1); // +1 for virtual baseline
   }
   ```
3. **Update snapshot card styling** to distinguish baseline:

   - Use blue color for baseline badge (vs green for contracts)
   - Show "Versjon 0" prominently
   - Display "12 låste pakker" instead of contract details
4. **Test baseline visualization**:

   - [ ] Baseline appears as first item in timeline sidebar
   - [ ] Baseline is selected by default when opening history panel
   - [ ] Overview tab shows correct budget values (390/310/700 MNOK)
   - [ ] Gantt tab renders 12 locked contracts with correct timeline
   - [ ] Precedence tab shows baseline network with ES/EF/LS/LF values
   - [ ] Baseline snapshot doesn't interfere with contract snapshots

**Files to Modify:**

- `frontend/components/history-panel.tsx` - Add baseline snapshot generation and prepend logic
- `frontend/lib/timeline-calculator.ts` - Ensure calculateTimeline works with locked items only

**Benefits:**

- Users see clear starting point (12 pre-negotiated contracts)
- History timeline shows complete project evolution from baseline to current state
- No database storage needed (calculated on-demand from wbs.json)
- Consistent with design decision to keep baseline out of database

---

### ❌ Owner Budget Revision Acceptance (NOT IMPLEMENTED)

**What Currently Works:**

- ✅ User can navigate to owner agent (Anne-Lise Berg)
- ✅ User can chat with owner agent
- ✅ Owner agent can propose budget increases in chat responses (via AI)
- ✅ Game context includes budget info sent to agent

**What's Missing:**

- ❌ **No OfferBox equivalent** for budget revision offers (no UI to accept/reject)
- ❌ **No backend endpoint** `POST /api/sessions/{sessionId}/budget-revision`
- ❌ **No database table** `budget_revisions` to track revision history
- ❌ **No snapshot creation** for type='budget_revision' events
- ❌ **No session update logic** to modify `available_budget` or `total_budget`

**What Would Be Needed (Estimated 6-8 hours):**

1. **Frontend OfferBox for Budget Revisions** (2 hours)

   - New regex pattern to detect budget revision offers in chat
   - New `BudgetRevisionOfferBox` component with Accept/Reject buttons
   - Handler `handleBudgetRevisionAccepted()`
2. **Backend Endpoint** (2 hours)

   ```python
   @app.post("/api/sessions/{session_id}/budget-revision")
   async def accept_budget_revision(
       session_id: str,
       request: BudgetRevisionRequest
   ):
       # Update game_sessions.available_budget
       # Update game_sessions.total_budget (if applicable)
       # Create budget_revision_snapshot
       # Return updated session
   ```
3. **Database Schema Update** (1 hour)

   - Add `budget_revisions` table (optional, for audit trail)
   - Update `create_budget_revision_snapshot()` function
   - Add fields: `revision_old_budget`, `revision_new_budget`, `revision_justification`
4. **Snapshot Creation** (1 hour)

   - New snapshot type: `'budget_revision'`
   - Store old and new budget amounts
   - Store justification text
   - NO need to recalculate timeline (budget doesn't affect CPM)
5. **History Panel Update** (1-2 hours)

   - Display budget revision snapshots differently (no contract details)
   - Show budget increase amount and justification
   - Add "Budget Revision" badge/icon

**Key Inputs Required for Owner Budget Revision:**

```typescript
{
  revision_amount: number,      // Increase in øre (e.g., 50000000 = 50 MNOK)
  justification: string,        // "Approved due to scope change"
  affects_total_budget: boolean // true = increase total, false = just available
}
```

**Database Effects Would Be:**

- INSERT into `budget_revisions` table (if created)
- UPDATE `game_sessions.available_budget` += revision_amount
- UPDATE `game_sessions.total_budget` += revision_amount (if affects_total_budget=true)
- INSERT into `session_snapshots` with snapshot_type='budget_revision'
- NO wbs_commitments changes
- NO timeline recalculation needed (budget doesn't affect critical path)

---

### 📊 Snapshot Data Requirements Summary

**For Vendor Contract Acceptance (what's captured):**

| Data Category                       | Fields                                          | Purpose                                 |
| ----------------------------------- | ----------------------------------------------- | --------------------------------------- |
| **Contract Info**             | wbs_id, cost, duration, supplier                | Which package, price, timeline, vendor  |
| **Budget State**              | committed, available, total                     | Budget at this moment (in øre)         |
| **Timeline State**            | project_end_date, days_before_deadline          | Project status vs deadline              |
| **Gantt Reconstruction**      | earliest_start{}, earliest_finish{} for all WBS | Render Gantt at this point in time      |
| **Precedence Reconstruction** | es{}, ef{}, ls{}, lf{}, slack{} for all WBS     | Render Precedence at this point in time |
| **Metadata**                  | version, label, snapshot_type, timestamp        | Snapshot tracking                       |

**For Owner Budget Revision (what WOULD be needed):**

| Data Category              | Fields                                                            | Purpose                    |
| -------------------------- | ----------------------------------------------------------------- | -------------------------- |
| **Revision Info**    | old_budget, new_budget, justification                             | Track budget changes       |
| **Budget State**     | committed, available, total                                       | Updated budget amounts     |
| **Timeline State**   | project_end_date, days_before_deadline                            | Same as before (unchanged) |
| **Gantt State**      | Same as previous snapshot                                         | No recalculation needed    |
| **Precedence State** | Same as previous snapshot                                         | No recalculation needed    |
| **Metadata**         | version, label='Budget Revision', snapshot_type='budget_revision' | Tracking                   |

**Note:** Budget revisions do NOT require timeline recalculation because budget doesn't affect critical path (only durations and dependencies do).

---

## ✅ MVP Completion Checklist - Acceptance Flows

**Note:** Baseline snapshot removed from database for simplicity and security. Frontend calculates baseline state from wbs.json on-demand (12 locked contracts showing starting situation: 390 MNOK committed, 310 MNOK available). Frontend creates "virtual" baseline snapshot displayed as version 0 in history panel. Only contract acceptances create database snapshots.

### **Phase 0: Add Baseline Snapshot to History Panel (1-2 hours) - ✅ COMPLETE**

**Note:** This is now complete via a client-side workaround in `frontend/components/history-panel.tsx`. The component now generates a "virtual" baseline snapshot if no snapshots are returned from the backend.

#### 0.1 Create Virtual Baseline Snapshot (1 hour)

- [X] **Add createBaselineSnapshot() logic** (`frontend/components/history-panel.tsx`)
  - [X] Filter locked items from wbsItems: `const lockedItems = wbsItems.filter(item => item.is_locked)`
  - [X] Calculate baseline timeline: `const baselineTimeline = calculateTimeline(lockedItems, [])`
  - [X] Return Snapshot object with all necessary data.

#### 0.2 Modify loadSnapshots() to Include Baseline (30 min)

- [X] **Update loadSnapshots() function** (`frontend/components/history-panel.tsx`)
  - [X] Check if `fetchedSnapshots.length === 0 && offset === 0`
  - [X] If true, create baseline: `const baseline = createBaselineSnapshot()` (logic is inlined)
  - [X] Prepend baseline to snapshots: `setSnapshots([baseline, ...data.snapshots])`
  - [X] Set baseline as default selection: `setSelectedSnapshot(baseline)`
  - [X] Increment total count: `setTotalCount(data.total_count + 1)`

#### 0.3 Update Snapshot Card Styling for Baseline (30 min)

- [X] **Distinguish baseline in timeline sidebar** (`history-panel.tsx`)
  - [X] Check `snapshot.snapshot_type === 'baseline'` in map function
  - [X] Use blue badge color for baseline
  - [X] "Versjon 0" is shown prominently

#### 0.4 Test Baseline Visualization (30 min)

- [X] **Verify baseline appears correctly**
  - [X] Open history panel → baseline appears as first item
  - [X] Baseline is auto-selected on panel open
  - [X] Overview tab shows correct budget
  - [X] Gantt tab renders baseline timeline
  - [X] Precedence tab shows baseline network

---

### **Phase 1: Complete Vendor Contract Acceptance Flow (5-7 hours)**

#### 1.1 Add Dependency Validation (2-3 hours) - ✅ COMPLETE

- [X] **Backend validation logic** (`backend/main.py` line ~654)
  - [X] In `create_commitment()`: Check if all `item.dependencies[]` exist in `wbs_commitments` table
  - [X] Query: `SELECT wbs_id FROM wbs_commitments WHERE session_id = ? AND wbs_id IN (...dependencies)`
  - [X] If missing dependencies, return 400 error with Norwegian message
  - [X] Error format: `{"detail": "Du må først forplikte deg til [1.3.1, 1.3.2] før du kan akseptere denne pakken"}`
- [X] **Test dependency blocking**
  - [X] Try to commit to "1.4.1 Råbygg" before "1.3.1 Grunnarbeid" → should fail
  - [X] Commit to "1.3.1" first → then "1.4.1" should succeed
- [X] **Frontend error display** (already exists in `chat-interface.tsx`)
  - [X] Verify error message shows in red alert box
  - [X] User can go back and negotiate prerequisite packages

#### 1.2 Add Timeline Validation (3-4 hours) - ✅ COMPLETE

- [X] **Backend timeline check** (`backend/main.py` line ~700, before saving commitment)
  - [X] Load all current commitments for session
  - [X] Add new commitment to temporary list
  - [X] Run `calculate_critical_path(wbs_items, temp_commitments, start_date, deadline)`
  - [X] Check if `projected_completion_date > deadline`
  - [X] If late, calculate `days_late = (projected_completion - deadline).days`
  - [X] Return 400 error with timeline impact
  - [X] Error format: `{"detail": "Dette tilbudet vil føre til {days_late} dagers forsinkelse. Fristen er {deadline}, beregnet ferdigstillelse vil bli {projected_completion}. Du må enten forhandle kortere varighet eller be eieren om fristverlengelse."}`
- [X] **Test timeline blocking**
  - [X] Accept offers with total duration > deadline → should fail
  - [X] Error message shows days late and suggests solutions
- [X] **Frontend error display**
  - [X] Verify error shows with timeline details
  - [X] User understands they need to renegotiate or go to owner

#### 1.3 Verify Downstream Updates Work (30 min)

- [ ] **After contract acceptance, verify all systems update:**
  - [ ] `wbs_commitments` table: New row inserted
  - [ ] `game_sessions.current_budget_used`: Incremented correctly
  - [ ] `session_snapshots`: New snapshot created with version N+1
  - [ ] **Gantt Chart**: Reflects new commitment timeline
    - [ ] New committed package shows in grey
    - [ ] Timeline dates updated with new critical path
    - [ ] Red outline on critical path items correct
  - [ ] **Precedence Diagram**: Shows updated timeline
    - [ ] ES/EF/LS/LF values updated for all affected nodes
    - [ ] Slack values recalculated
    - [ ] Critical path highlighting correct
  - [ ] **History Panel**: New snapshot appears
    - [ ] Timeline sidebar shows new version
    - [ ] Can click and view Gantt/Precedence from that snapshot
    - [ ] Budget values correct in snapshot

---

### **Phase 2: Implement Owner Budget Revision Flow (6-8 hours)**

#### 2.1 Frontend: Offer Detection & UI (2 hours)

- [ ] **Regex pattern for budget revision offers** (`chat-interface.tsx`)
  - [ ] Add pattern to detect: "budsjett.*økning.*(\d+)\s*MNOK" or similar
  - [ ] Parse: revision_amount, justification from AI response
  - [ ] Example: "Jeg kan godkjenne en budsjettøkning på 50 MNOK for å dekke uforutsette kostnader"
- [ ] **BudgetRevisionOfferBox component** (new component)
  - [ ] Similar to OfferBox but for budget revisions
  - [ ] Display: Old budget → New budget, increase amount, justification
  - [ ] Buttons: "✓ Godta budsjettøkning" and "✗ Avslå"
  - [ ] Show impact: "Tilgjengelig budsjett: 120 MNOK → 170 MNOK"
- [ ] **Accept handler** (`game/[sessionId]/[agentId]/[wbsId]/page.tsx`)
  - [ ] `handleBudgetRevisionAccepted(revision)` function
  - [ ] Calls new API: `acceptBudgetRevision(sessionId, revision)`

#### 2.2 Backend: Budget Revision Endpoint (2 hours)

- [ ] **New API endpoint** (`backend/main.py`)
  - [ ] `POST /api/sessions/{session_id}/budget-revision`
  - [ ] Request body: `{ revision_amount: number, justification: string, affects_total_budget: boolean }`
  - [ ] Validation: revision_amount > 0, justification not empty
  - [ ] Load current session
  - [ ] Update `available_budget` += revision_amount
  - [ ] Update `total_budget` += revision_amount (if affects_total_budget=true)
  - [ ] Call `create_budget_revision_snapshot()` RPC
  - [ ] Return updated session
- [ ] **API client** (`frontend/lib/api/sessions.ts`)
  - [ ] `acceptBudgetRevision(sessionId, revision)` function
  - [ ] Returns updated session

#### 2.3 Database: Budget Revision Snapshot (1-2 hours)

- [ ] **New database function** (`database/migrations/003_budget_revisions.sql` - new file)
  - [ ] `create_budget_revision_snapshot(p_session_id, p_old_budget, p_new_budget, p_revision_amount, p_justification)`
  - [ ] Insert into `session_snapshots` with:
    - [ ] `snapshot_type = 'budget_revision'`
    - [ ] `label = 'Budsjettøkning: +{revision_amount/1000000} MNOK'`
    - [ ] `budget_committed`: Same as before (no change)
    - [ ] `budget_available`: Updated amount
    - [ ] `budget_total`: Updated amount (if applicable)
    - [ ] `contract_*` fields: NULL (no contract involved)
    - [ ] `gantt_state`: Copy from previous snapshot (timeline unchanged)
    - [ ] `precedence_state`: Copy from previous snapshot (timeline unchanged)
    - [ ] `version`: Auto-incremented
  - [ ] Add custom fields (optional):
    - [ ] `revision_old_budget`: Previous available budget
    - [ ] `revision_new_budget`: New available budget
    - [ ] `revision_justification`: Why it was approved
- [ ] **Run migration**
  - [ ] Apply to Supabase database
  - [ ] Verify function exists: `SELECT * FROM pg_proc WHERE proname = 'create_budget_revision_snapshot'`

#### 2.4 History Panel: Display Budget Revisions (1-2 hours)

- [ ] **Update snapshot card rendering** (`history-panel.tsx`)
  - [ ] Check `snapshot.snapshot_type === 'budget_revision'`
  - [ ] Show different icon: 💰 or 📈 instead of ✓
  - [ ] Label: "Budsjettøkning: +50 MNOK" (instead of contract details)
  - [ ] Show justification in card
  - [ ] No contract cost/duration display
- [ ] **Overview tab**
  - [ ] Show budget change: "Økning fra 310 MNOK til 360 MNOK"
  - [ ] Display justification text
  - [ ] Timeline unchanged message: "Ingen endring i prosjektets tidslinje"
- [ ] **Gantt/Precedence tabs**
  - [ ] Should show same timeline as previous snapshot (budget doesn't affect CPM)

#### 2.5 Test Complete Budget Revision Flow (30 min)

- [ ] **End-to-end test:**
  - [ ] Chat with owner agent (Anne-Lise Berg)
  - [ ] AI responds with budget increase offer
  - [ ] BudgetRevisionOfferBox appears with correct amounts
  - [ ] Click "✓ Godta budsjettøkning"
  - [ ] Session updates with new available budget
  - [ ] Dashboard shows increased budget
  - [ ] New snapshot appears in history panel
  - [ ] Can view snapshot and see budget change
  - [ ] Gantt/Precedence unchanged (as expected)

---

## 🎯 DETAILED IMPLEMENTATION PLAN TO MVP (Updated: December 31, 2025)

### **Current Status Analysis**

**Project Completion: 99% of MVP**

**Recently Completed (Dec 30-31, 2025):**

1. **Authentication Security Fix** (Commit 281f438)

   - Removed hardcoded user bypass in `get_current_user()`
   - Implemented proper JWT validation: `supabase.auth.get_user(token.credentials)`
   - All users now authenticate securely through Supabase Auth API
2. **Dependency Validation** (Commit f8411bc)

   - Backend validation in `backend/main.py` lines 610-635
   - Loads WBS dependencies from wbs.json
   - Checks existing commitments before allowing new ones
   - Returns clear error: "Du må først forplikte deg til følgende avhengige pakker: [X, Y] før du kan akseptere 'Z'."
3. **Timeline Validation** (Commit f8411bc)

   - Backend validation in `backend/main.py` lines 659-703
   - Runs CPM calculation before each commitment
   - Compares projected completion vs deadline (2026-05-15)
   - Blocks commitments that would make project late
   - Error message shows days late and suggests renegotiation
4. **Baseline Snapshot** (Completed Dec 30)

   - Client-side workaround in `frontend/components/history-panel.tsx` lines 106-162
   - Generates virtual baseline snapshot from wbs.json (12 locked contracts)
   - Displays as version 0 in history panel
   - Shows starting state: 390 MNOK committed, 310 MNOK available

**What's Fully Functional:**

- ✅ Authentication & authorization (Supabase + RLS)
- ✅ Dashboard with 3-tier budget display (310/390/700 MNOK)
- ✅ AI negotiation with 4 agents (Gemini 2.5 Flash)
- ✅ Vendor contract acceptance (12-step flow with automatic snapshots)
- ✅ Budget validation (prevents overspending)
- ✅ Dependency validation (prevents invalid dependencies)
- ✅ Timeline validation (prevents late delivery)
- ✅ Critical path algorithm (CPM with ES/EF/LS/LF/slack)
- ✅ Gantt Chart visualization
- ✅ Precedence Diagram (AON network)
- ✅ History panel with snapshot reconstruction
- ✅ Session completion flow
- ✅ Database schema (6 tables, RLS, triggers, computed columns)

**Only 1 Feature Remains:**

- ❌ Owner Perspective Budget Revision Acceptance (6-8 hours)

---

### **IMPLEMENTATION PLAN: Owner Budget Revision Feature**

**Total Estimated Time: 6-8 hours**

This feature allows students to negotiate with the owner agent (Anne-Lise Berg) to increase the available budget when they cannot complete all required work packages within the 310 MNOK constraint.

---

#### **Implementation Task 1: Database Migration - Budget Revision Snapshot Function (1-2 hours)**

**Priority: HIGH - Do this first, as backend depends on it**

**File:** `database/migrations/003_budget_revisions.sql` (NEW FILE)

**Action:** Create new SQL migration file with the following content:

```sql
-- ============================================================================
-- Budget Revision Snapshot Function
-- Creates a snapshot when owner approves budget increase
-- ============================================================================

CREATE OR REPLACE FUNCTION create_budget_revision_snapshot(
    p_session_id UUID,
    p_old_available BIGINT,
    p_new_available BIGINT,
    p_old_total BIGINT,
    p_new_total BIGINT,
    p_revision_amount BIGINT,
    p_justification TEXT
) RETURNS UUID AS $$
DECLARE
    v_snapshot_id UUID;
    v_version INT;
    v_session game_sessions%ROWTYPE;
    v_current_budget_committed BIGINT;
    v_project_end_date DATE;
    v_days_before_deadline INT;
    v_previous_snapshot session_snapshots%ROWTYPE;
BEGIN
    -- Get current session
    SELECT * INTO v_session FROM game_sessions WHERE id = p_session_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Session not found: %', p_session_id;
    END IF;

    -- Calculate next version number
    SELECT COALESCE(MAX(version), 0) + 1 INTO v_version
    FROM session_snapshots
    WHERE session_id = p_session_id;

    -- Get previous snapshot for timeline data (budget doesn't affect timeline)
    SELECT * INTO v_previous_snapshot
    FROM session_snapshots
    WHERE session_id = p_session_id
    ORDER BY version DESC
    LIMIT 1;

    -- Calculate current committed budget (in øre)
    v_current_budget_committed := COALESCE(v_session.current_budget_used, 0) * 100;

    -- Use previous timeline data (budget revision doesn't change project timeline)
    IF v_previous_snapshot IS NOT NULL THEN
        v_project_end_date := v_previous_snapshot.project_end_date;
        v_days_before_deadline := v_previous_snapshot.days_before_deadline;
    ELSE
        -- Fallback if no previous snapshot
        v_project_end_date := '2025-09-29'::DATE;
        v_days_before_deadline := (DATE '2026-05-15' - v_project_end_date);
    END IF;

    -- Insert snapshot
    INSERT INTO session_snapshots (
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
    ) VALUES (
        p_session_id,
        v_version,
        'Budsjettøkning: +' || (p_revision_amount / 100000000)::TEXT || ' MNOK',
        'budget_revision',
        v_current_budget_committed,
        p_new_available,
        p_new_total,
        NULL, -- No contract associated
        NULL,
        NULL,
        NULL,
        v_project_end_date,
        v_days_before_deadline,
        COALESCE(v_previous_snapshot.gantt_state, '{}'::JSONB), -- Copy from previous
        COALESCE(v_previous_snapshot.precedence_state, '{}'::JSONB) -- Copy from previous
    )
    RETURNING id INTO v_snapshot_id;

    RETURN v_snapshot_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION create_budget_revision_snapshot TO authenticated;

-- Add comment
COMMENT ON FUNCTION create_budget_revision_snapshot IS
    'Creates a snapshot when owner agent approves a budget revision. ' ||
    'Timeline data is copied from previous snapshot since budget changes do not affect CPM.';
```

**Deployment Steps:**

1. Open Supabase Dashboard → SQL Editor
2. Paste the SQL above
3. Execute the migration
4. Verify function created: `SELECT proname FROM pg_proc WHERE proname = 'create_budget_revision_snapshot';`

**Success Criteria:**

- ✅ Function exists in database
- ✅ Function returns UUID
- ✅ Can be called by authenticated users

---

#### **Implementation Task 2: Backend API - Budget Revision Endpoint (2 hours)**

**File:** `backend/main.py`

**Action 1:** Add Pydantic model (add after other models, around line 225)

```python
class BudgetRevisionRequest(BaseModel):
    revision_amount: int  # Amount to increase in øre (e.g., 50000000 = 50 MNOK)
    justification: str     # Reason for increase (from AI agent response)
    affects_total_budget: bool = True  # Whether to increase total or just available
```

**Action 2:** Add endpoint (add after other session endpoints, around line 576)

```python
@app.post("/api/sessions/{session_id}/budget-revision", tags=["Sessions"])
def accept_budget_revision(
    session_id: str,
    request: BudgetRevisionRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    """
    Accept a budget revision offer from the owner agent.
    Updates session budget and creates a budget_revision snapshot.
    """
    try:
        # 1. Validate session ownership
        session_response = (
            db.table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )

        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        session = session_response.data

        # 2. Validate revision amount
        if request.revision_amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Budsjettøkning må være positiv"
            )

        if not request.justification or len(request.justification.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Begrunnelse for budsjettøkning er påkrevd"
            )

        # 3. Calculate old and new budgets
        old_available = session["available_budget"]
        old_total = session["total_budget"]

        # Convert from øre to NOK for calculation
        revision_nok = request.revision_amount / 100

        new_available = old_available + revision_nok
        new_total = old_total + revision_nok if request.affects_total_budget else old_total

        # 4. Update session budgets
        db.table("game_sessions").update({
            "available_budget": new_available,
            "total_budget": new_total
        }).eq("id", session_id).execute()

        # 5. Create budget revision snapshot
        try:
            db.rpc(
                "create_budget_revision_snapshot",
                {
                    "p_session_id": session_id,
                    "p_old_available": int(old_available * 100),  # Convert to øre
                    "p_new_available": int(new_available * 100),
                    "p_old_total": int(old_total * 100),
                    "p_new_total": int(new_total * 100),
                    "p_revision_amount": request.revision_amount,
                    "p_justification": request.justification,
                },
            ).execute()
        except Exception as snapshot_error:
            print(f"Warning: Could not create budget revision snapshot: {snapshot_error}")
            import traceback
            traceback.print_exc()

        # 6. Return success with updated budget info
        return {
            "success": True,
            "old_available_budget": old_available,
            "new_available_budget": new_available,
            "old_total_budget": old_total,
            "new_total_budget": new_total,
            "revision_amount_mnok": revision_nok / 1_000_000,
            "message": f"Budsjett økt med {revision_nok / 1_000_000:.0f} MNOK"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error accepting budget revision: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved godkjenning av budsjettøkning"
        )
```

**Testing:**

```bash
# Test with curl (replace TOKEN and SESSION_ID)
curl -X POST http://localhost:8000/api/sessions/{SESSION_ID}/budget-revision \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "revision_amount": 5000000000,
    "justification": "Godkjent på grunn av uforutsette kostnader",
    "affects_total_budget": true
  }'
```

**Success Criteria:**

- ✅ Endpoint returns 200 with success message
- ✅ Session budget updated in database
- ✅ Snapshot created with type='budget_revision'
- ✅ Error handling works (404 for invalid session, 400 for invalid amount)

---

#### **Implementation Task 3: Frontend - Budget Revision Detection & UI (2 hours)**

**File 1:** `frontend/components/chat-interface.tsx`

**Action 1:** Add budget revision regex pattern and interface (around line 30)

```typescript
// Add to existing regex patterns
const budgetRevisionPattern = /budsjett.*?økning.*?(\d+)\s*MNOK/i;

interface BudgetRevisionOffer {
  revision_amount_mnok: number;
  revision_amount_ore: number;
  justification: string;
  old_budget: number;
  new_budget: number;
}

// Budget Revision Offer Box Component
function BudgetRevisionOfferBox({
  offer,
  onAccept,
  onReject,
}: {
  offer: BudgetRevisionOffer;
  onAccept: () => void;
  onReject: () => void;
}) {
  return (
    <div className="my-4 p-4 border-2 border-green-500 bg-green-50 rounded-lg">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">💰</span>
        <h3 className="font-bold text-lg text-green-800">
          Budsjettøkning: +{offer.revision_amount_mnok} MNOK
        </h3>
      </div>

      <div className="space-y-2 text-sm mb-4">
        <div className="flex justify-between">
          <span className="text-gray-600">Nåværende tilgjengelig budsjett:</span>
          <span className="font-semibold">{offer.old_budget.toFixed(0)} MNOK</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Nytt tilgjengelig budsjett:</span>
          <span className="font-semibold text-green-700">
            {offer.new_budget.toFixed(0)} MNOK
          </span>
        </div>
        <div className="pt-2 border-t border-green-200">
          <p className="text-gray-700 italic">{offer.justification}</p>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={onAccept}
          className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
        >
          ✓ Godta budsjettøkning
        </button>
        <button
          onClick={onReject}
          className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
        >
          ✗ Avslå
        </button>
      </div>
    </div>
  );
}
```

**Action 2:** Add budget revision detection logic

```typescript
// Add detection function
const detectBudgetRevision = (text: string): BudgetRevisionOffer | null => {
  const match = text.match(budgetRevisionPattern);
  if (!match) return null;

  const revisionAmountMnok = parseInt(match[1]);
  const revisionAmountOre = revisionAmountMnok * 100000000;

  // Extract justification
  const justificationMatch = text.match(/(?:fordi|på grunn av|grunnet|for å)\s+(.+?)(?:\.|$)/i);
  const justification = justificationMatch
    ? justificationMatch[1]
    : "Godkjent budsjettøkning";

  const oldBudget = gameContext?.available_budget
    ? gameContext.available_budget / 1_000_000
    : 310;
  const newBudget = oldBudget + revisionAmountMnok;

  return {
    revision_amount_mnok: revisionAmountMnok,
    revision_amount_ore: revisionAmountOre,
    justification,
    old_budget: oldBudget,
    new_budget: newBudget,
  };
};

// Add state for accepted budget revisions
const [acceptedBudgetRevisions, setAcceptedBudgetRevisions] = useState<Set<string>>(
  new Set()
);

// In message rendering, add budget revision check
{message.role === "agent" && (
  <>
    {(() => {
      const offer = detectOffer(message.content);
      if (offer && !acceptedOffers.has(message.content)) {
        return <OfferBox offer={offer} onAccept={...} onReject={...} />;
      }

      // Budget revision detection
      const budgetRevision = detectBudgetRevision(message.content);
      if (budgetRevision && !acceptedBudgetRevisions.has(message.content)) {
        return (
          <BudgetRevisionOfferBox
            offer={budgetRevision}
            onAccept={() => handleBudgetRevisionAccept(budgetRevision, message.content)}
            onReject={() => handleBudgetRevisionReject(message.content)}
          />
        );
      }

      return null;
    })()}
  </>
)}
```

**File 2:** `frontend/app/game/[sessionId]/[agentId]/[wbsId]/page.tsx`

**Action:** Add budget revision acceptance handler

```typescript
async function handleBudgetRevisionAccept(
  revision: BudgetRevisionOffer,
  messageContent: string
) {
  try {
    setAcceptedBudgetRevisions((prev) => new Set(prev).add(messageContent));

    const token = await getAuthToken();
    if (!token) {
      alert("Ingen autentiseringstoken funnet");
      return;
    }

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/budget-revision`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          revision_amount: revision.revision_amount_ore,
          justification: revision.justification,
          affects_total_budget: true,
        }),
      }
    );

    if (!response.ok) {
      const error = await response.json();
      alert(`Feil: ${error.detail || "Kunne ikke godkjenne budsjettøkning"}`);
      setAcceptedBudgetRevisions((prev) => {
        const newSet = new Set(prev);
        newSet.delete(messageContent);
        return newSet;
      });
      return;
    }

    const result = await response.json();
    alert(
      `✅ ${result.message}\n\nTilgjengelig budsjett økt fra ${result.old_available_budget / 1_000_000} MNOK til ${result.new_available_budget / 1_000_000} MNOK`
    );

    // Redirect to dashboard
    router.push("/dashboard");
  } catch (error) {
    console.error("Error accepting budget revision:", error);
    alert("En feil oppstod ved godkjenning av budsjettøkning");
    setAcceptedBudgetRevisions((prev) => {
      const newSet = new Set(prev);
      newSet.delete(messageContent);
      return newSet;
    });
  }
}

function handleBudgetRevisionReject(messageContent: string) {
  setAcceptedBudgetRevisions((prev) => new Set(prev).add(messageContent));
}
```

**Success Criteria:**

- ✅ Budget revision offers detected in owner agent responses
- ✅ BudgetRevisionOfferBox renders with correct amounts
- ✅ Accept button calls backend API
- ✅ Success message shows updated budget
- ✅ Redirect to dashboard works

---

#### **Implementation Task 4: History Panel - Display Budget Revisions (1-2 hours)**

**File:** `frontend/components/history-panel.tsx`

**Action 1:** Update snapshot card rendering (around line 250)

```typescript
{snapshots.map((snapshot) => {
  const isBudgetRevision = snapshot.snapshot_type === "budget_revision";
  const isBaseline = snapshot.snapshot_type === "baseline";

  return (
    <div
      key={snapshot.id}
      onClick={() => setSelectedSnapshot(snapshot)}
      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
        selectedSnapshot?.id === snapshot.id
          ? "border-blue-500 bg-blue-50"
          : "border-gray-200 hover:border-gray-300"
      }`}
    >
      {/* Version badge */}
      <div className="flex items-center justify-between mb-2">
        <span
          className={`px-2 py-1 text-xs font-semibold rounded ${
            isBaseline
              ? "bg-blue-100 text-blue-800"
              : isBudgetRevision
              ? "bg-green-100 text-green-800"
              : "bg-gray-100 text-gray-800"
          }`}
        >
          Versjon {snapshot.version}
        </span>
        <span className="text-xs text-gray-500">
          {format(new Date(snapshot.created_at), "d. MMM yyyy HH:mm", {
            locale: nb,
          })}
        </span>
      </div>

      {/* Label */}
      <h3 className="font-semibold text-sm mb-2">{snapshot.label}</h3>

      {/* Budget Revision Details */}
      {isBudgetRevision ? (
        <div className="space-y-1 text-xs text-gray-600">
          <div className="flex items-center gap-1">
            <span className="text-lg">💰</span>
            <span>Budsjettøkning</span>
          </div>
          <div className="pl-6">
            <p>
              Tilgjengelig: {(snapshot.budget_available / 100000000).toFixed(0)}{" "}
              MNOK
            </p>
            <p className="text-gray-500 italic text-xs mt-1">
              Ingen endring i tidslinje
            </p>
          </div>
        </div>
      ) : isBaseline ? (
        <div className="text-xs text-gray-600">
          <p>12 forhåndsinngåtte kontrakter</p>
          <p>390 MNOK forpliktet</p>
        </div>
      ) : (
        <div className="space-y-1 text-xs text-gray-600">
          <p>
            <strong>Pakke:</strong> {snapshot.contract_wbs_id}
          </p>
          <p>
            <strong>Kostnad:</strong>{" "}
            {snapshot.contract_cost
              ? (snapshot.contract_cost / 100000000).toFixed(0)
              : "N/A"}{" "}
            MNOK
          </p>
          <p>
            <strong>Leverandør:</strong> {snapshot.contract_supplier}
          </p>
        </div>
      )}
    </div>
  );
})}
```

**Action 2:** Update Overview tab for budget revisions

```typescript
{/* In Overview tab content */}
{selectedSnapshot?.snapshot_type === "budget_revision" ? (
  <div className="space-y-4">
    <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
      <span className="text-4xl">💰</span>
      <div>
        <h4 className="font-bold text-lg text-green-800">
          Budsjettøkning godkjent
        </h4>
        <p className="text-sm text-gray-600">
          {selectedSnapshot.label}
        </p>
      </div>
    </div>

    <div className="grid grid-cols-2 gap-4">
      <div className="p-4 bg-white border border-gray-200 rounded-lg">
        <p className="text-sm text-gray-500 mb-1">Tilgjengelig budsjett</p>
        <p className="text-2xl font-bold text-green-600">
          {(selectedSnapshot.budget_available / 100000000).toFixed(0)} MNOK
        </p>
      </div>
      <div className="p-4 bg-white border border-gray-200 rounded-lg">
        <p className="text-sm text-gray-500 mb-1">Total budsjett</p>
        <p className="text-2xl font-bold">
          {(selectedSnapshot.budget_total / 100000000).toFixed(0)} MNOK
        </p>
      </div>
    </div>

    <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
      <p className="text-sm font-semibold text-gray-700 mb-2">
        Prosjektets tidslinje
      </p>
      <p className="text-sm text-gray-600">
        📅 Ferdigstillelse: {selectedSnapshot.project_end_date}
      </p>
      <p className="text-sm text-gray-600">
        ⏰ {selectedSnapshot.days_before_deadline} dager før frist
      </p>
      <p className="text-xs text-gray-500 italic mt-2">
        Ingen endring i tidslinje (budsjettøkning påvirker ikke kritisk sti)
      </p>
    </div>
  </div>
) : (
  // Existing contract snapshot rendering
  ...
)}
```

**Success Criteria:**

- ✅ Budget revision snapshots show with green badge and 💰 icon
- ✅ Overview tab shows budget change clearly
- ✅ Gantt/Precedence tabs show unchanged timeline

---

### **TESTING & VERIFICATION PLAN (1-2 hours)**

#### **Test Checklist**

**1. Budget Revision Flow (E2E):**

- [ ] Start new session
- [ ] Navigate to owner agent (Anne-Lise Berg)
- [ ] Request budget increase in chat
- [ ] Verify AI responds with budget offer
- [ ] Verify BudgetRevisionOfferBox appears
- [ ] Click "Godta budsjettøkning"
- [ ] Verify success message
- [ ] Verify redirect to dashboard
- [ ] Verify increased budget displayed
- [ ] Open history panel
- [ ] Verify budget revision snapshot appears
- [ ] Verify Overview/Gantt/Precedence tabs work

**2. Validation Testing:**

- [ ] Dependency validation works (try 1.4.1 before 1.3.1)
- [ ] Timeline validation works (try late offer)
- [ ] Budget validation works (try overspending)
- [ ] Budget revision validation (try negative amount)

**3. Complete User Journey:**

- [ ] Register → Login → Create session
- [ ] Negotiate with 3 vendors
- [ ] Accept 3 contracts
- [ ] Request budget increase
- [ ] Complete session
- [ ] View complete history

**4. Database Verification:**

```sql
-- Check session updated
SELECT available_budget, total_budget FROM game_sessions WHERE id = '{SESSION_ID}';

-- Check snapshot created
SELECT version, snapshot_type, label FROM session_snapshots
WHERE session_id = '{SESSION_ID}' ORDER BY version;
```

---

### **POST-MVP ROADMAP**

**Immediate Priority (10-13 hours):**

1. Export UI (2-3 hours)
2. Renegotiation/Uncommit (3-4 hours)
3. History Panel UX Polish (2-3 hours)
4. Agent Timeout UI (3 hours)

**Medium Priority (20-30 hours):**
5. Mobile Responsiveness (8-12 hours)
6. Administration Panel (12-16 hours)

**Long-term (40+ hours):**
7. Automated Testing (40+ hours)
8. Production Deployment (4-8 hours)

---

### **RECOMMENDED EXECUTION SCHEDULE**

**Today (Dec 31):**

- Task 1: Database migration (1-2 hours)
- Task 2: Backend endpoint (2 hours)

**Tomorrow (Jan 1):**

- Task 3: Frontend UI (2 hours)
- Task 4: History panel (1-2 hours)
- Testing & verification (1-2 hours)

**Total to MVP: 6-8 hours**

---

### **🎓 ACADEMIC ASSESSMENT**

**Strengths:**
✅ Solid architecture (Next.js, FastAPI, PostgreSQL)
✅ Robust validation (dependency, timeline, budget)
✅ Correct CPM implementation
✅ Data persistence with RLS
✅ AI integration with context
✅ Comprehensive documentation

**Grade: A-** (would be A with testing + deployment)

**Recommendation:** Complete owner budget revision to reach 100% MVP, then deploy and pilot with students.

---

### **Phase 3: Polish History Panel UX (Optional - Nice to Have)**

**Note:** Most critical history panel work completed in Phase 0 (baseline snapshot). These are UX enhancements.

- [ ] **Improve snapshot card design** (30 min)
  - [ ] Better visual hierarchy (larger version badge, clearer icons)
  - [ ] Enhanced hover effects and smooth transitions
  - [ ] Better spacing and typography
- [ ] **Enhance pagination UX** (30 min)
  - [ ] Add loading spinner when fetching more snapshots
  - [ ] Smooth scroll animation when new snapshots load
  - [ ] "Loading..." state on "Load More" button
  - [ ] Disable button when no more snapshots
- [ ] **Add filters/search** (1 hour - optional)
  - [ ] Filter by snapshot type (All, Baseline, Contracts, Budget Revisions)
  - [ ] Search by WBS ID or supplier name
  - [ ] Clear filters button
- [ ] **Responsive improvements** (1 hour - optional)
  - [ ] Stack timeline sidebar on mobile (full width)
  - [ ] Collapse snapshot details on small screens
  - [ ] Touch-friendly interactions

---

### **Phase 4: Updated Timeline Estimates**

**Updated MVP Timeline (Critical Path to Completion):**

- Phase 0: Baseline Snapshot: 1-2 hours
- Phase 1: Dependency Validation: 2-3 hours
- Phase 1: Timeline Validation: 3-4 hours
- Phase 2: Owner Budget Revision: 6-8 hours
- **Total to MVP: 12-17 hours** → **10-15 hours** (reduced due to chat history fix completed Dec 23)

**Nice to Have (Post-MVP):**

- Phase 3: History Panel UX Polish: 2-3 hours
- Renegotiation/Uncommit: 3-4 hours
- Export UI: 2-3 hours
- Agent Timeout UI: 3 hours
- **Total Nice to Have: 10-13 hours**

---

### **Key Integration Points - How Data Flows**

```
┌─────────────────────────────────────────────────────────────┐
│                    ACCEPTANCE TRIGGER                        │
│  User clicks "Accept" on vendor offer OR budget revision     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  VALIDATION PHASE                            │
│  1. Dependency check (vendor only)                           │
│  2. Timeline check (vendor only)                             │
│  3. Budget check (both)                                      │
│  → If any fail: BLOCK and return error to user              │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  DATABASE UPDATES                            │
│  Vendor Contract:                                            │
│    - INSERT wbs_commitments                                  │
│    - UPDATE game_sessions.current_budget_used                │
│  Budget Revision:                                            │
│    - UPDATE game_sessions.available_budget                   │
│    - UPDATE game_sessions.total_budget (if applicable)       │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              CRITICAL PATH RECALCULATION                     │
│  Vendor Contract:                                            │
│    - Run calculate_critical_path() with new commitment       │
│    - Returns: ES/EF/LS/LF/slack for ALL WBS items           │
│    - Returns: projected_completion_date, days_before_deadline│
│  Budget Revision:                                            │
│    - SKIP (budget doesn't affect timeline)                   │
│    - Copy timeline from previous snapshot                    │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  SNAPSHOT CREATION                           │
│  Call create_*_snapshot() RPC function:                      │
│    - Auto-increment version (via trigger)                    │
│    - Save budget state (committed/available/total)           │
│    - Save contract details (vendor) or revision (owner)      │
│    - Save gantt_state JSONB (full timeline)                  │
│    - Save precedence_state JSONB (full timeline)             │
│    - Enforce 100 snapshot limit (delete oldest)              │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND VISUALIZATION UPDATES                  │
│  1. Dashboard:                                               │
│     - Budget bars update (committed/available/total)         │
│     - Commitment list refreshes                              │
│  2. Gantt Chart:                                             │
│     - Re-renders with new timeline data                      │
│     - Committed packages show in grey                        │
│     - Timeline shifts based on new durations                 │
│     - Critical path highlighting updates                     │
│  3. Precedence Diagram:                                      │
│     - Nodes update with new ES/EF/LS/LF values              │
│     - Slack values recalculate                               │
│     - Critical path highlighting updates                     │
│  4. History Panel:                                           │
│     - New snapshot appears in timeline sidebar               │
│     - Can click to view Gantt/Precedence from that moment    │
│     - Budget overview shows state at that snapshot           │
└─────────────────────────────────────────────────────────────┘
```

---

### **Critical Dependencies Between Systems**

| System                          | Depends On                        | Why                                     |
| ------------------------------- | --------------------------------- | --------------------------------------- |
| **Gantt Chart**           | Timeline calculation, Commitments | Needs ES/EF dates for all tasks         |
| **Precedence Diagram**    | Timeline calculation, Commitments | Needs ES/EF/LS/LF/slack for all tasks   |
| **History Panel**         | Snapshots                         | Displays historical states              |
| **Snapshots**             | Timeline calculation              | Stores gantt_state and precedence_state |
| **Timeline Validation**   | Timeline calculation              | Must run CPM before allowing commitment |
| **Dependency Validation** | Commitments table                 | Checks if prerequisites exist           |
| **Budget Tracking**       | Commitments, Revisions            | Sums all committed costs                |

**Key Insight:** Timeline calculation is the **single source of truth** that feeds Gantt, Precedence, Snapshots, and Validation. Must run after every commitment or when requested.

---

### File Statistics

- **Frontend:** ~150 source files, ~8,000+ lines of TypeScript/TSX
- **Backend:** ~10 Python files, ~1,200+ lines of code
- **Database:** 6 tables with 7 migration files (~960 lines SQL total)
- **Documentation:** 50+ markdown files, 22 SVG diagrams
- **Data Files:** 2 JSON files (15 WBS items, 4 agent configs)
- **Total Codebase:** ~11,500+ lines (excluding documentation)

### Recommended Next Steps (Priority Order)

**Week 1: Critical Path to MVP (6-11 hours) - ✅ COMPLETE**

1. ✅ **Debug Visualization Data Flow** (2-3 hours) - Fix Gantt/Precedence data binding from /validate endpoint
2. ✅ **Session Completion Flow** (4-6 hours) - Implement completion page with results summary
3. ✅ **Verify Database Import** (1-2 hours) - Confirm all tables and triggers working in production

**Week 2: History & Owner Perspective Completion (4-9 hours) - ✅ VISUALIZATIONS COMPLETE, 🟡 OWNER PERSPECTIVE IN PROGRESS**
4. ✅ **Complete Gantt Chart** (DONE) - Full timeline visualization with critical path, dependencies, dynamic calculations
5. ✅ **Complete Precedence Diagram** (DONE) - Full AON network with ReactFlow, ES/EF/LS/LF, slack, persistent layout
6. ✅ **Fix Backend Validation** (DONE) - Corrected WBS file path, endpoint now returns timeline data
7. **Complete Owner Perspective Budget Revision** (6-8 hours) - Implement budget revision acceptance flow:

- Frontend: BudgetRevisionOfferBox component with Accept/Reject buttons
- Backend: POST /api/sessions/{sessionId}/budget-revision endpoint
- Database: create_budget_revision_snapshot() function with new snapshot type
- History Panel: Display budget revision snapshots with old/new amounts and justification

8. **Polish History Panel UI** (1-2 hours) - Final polish on snapshot cards, improve pagination UX

**Week 3: Polish & Features (7-9 hours)**
9. **Agent Timeout UI** (3 hours) - Visual countdown and lock status display
10. **Export Functionality** (4-6 hours) - Session/history export to JSON

**Week 4+: Quality & Deployment (50+ hours)**
11. **Mobile Responsiveness** (8-12 hours) - Optimize for mobile devices
12. **Automated Testing** (40+ hours) - Unit, integration, and E2E test suite
13. **Production Deployment** (4-8 hours) - Deploy frontend/backend, final testing

**Nice to Have (Future Enhancements)**

- **Renegotiation/Uncommit Feature** (3-4 hours) - DELETE endpoint + uncommit UI to reverse accepted offers

### Updated Timeline Estimates

- **To MVP (Core Features):** 12-17 hours (Owner budget revision + History polish + Dependency validation + Timeline validation)
- **To Enhanced MVP:** 19-26 hours (MVP + Export UI + Uncommit)
- **To Full Feature Set:** 30-39 hours (Enhanced MVP + Agent timeout UI + Mobile responsiveness)
- **To Production Quality:** 70-79 hours (Full feature set + Automated testing + Deployment)
- **With Admin Panel:** 82-95 hours (Production quality + Teacher administration dashboard)

---

## Phase 0: Discovery & Analysis

- [X] **/run-agent-task analyst *workflow-init**
  - *File: `bmm-workflow-status.yaml`*
  - *Status: Done. Initialized the project workflow tracking.*

- **Brainstorming (Completed)**

  - [X] **/run-agent-task analyst *brainstorm "Initial project ideas and scope"**
    - *File: `brainstorming-session-results-2025-12-02.md`*
    - *Defines: General ideas for the project.*
  - [X] **/run-agent-task analyst *brainstorm "User interaction models"**
    - *File: `brainstorming-session-results-user-interactions-2025-12-02.md`*
    - *Defines: Initial concepts for how users will interact with the simulation.*
  - [X] **/run-agent-task analyst *brainstorm "Risk and monitoring strategies"**
    - *File: `brainstorming-session-results-risk-and-monitoring-2025-12-02.md`*
    - *Defines: Potential risks and how to monitor them.*
  - [X] **/run-agent-task architect *brainstorm "Technical Architecture"**
    - *File: `brainstorming-technical-architecture-report.md`*
    - *Defines: The core technology stack (React, FastAPI, SQLite).*
- **Brainstorming (Completed)**

  - [X] **/run-agent-task analyst *brainstorm "Audience and Core Value"**
    - *File: `brainstorming-session-audience-and-core-value-2025-12-07.md`*
    - *Defines: User Personas (Sara, Magnus, Prof. Eriksen, Ingrid), Value Proposition, Success Metrics, Jobs-to-be-Done.*
  - [X] **/run-agent-task analyst *brainstorm "Core Functionality and Scope"**
    - *File: `brainstorming-session-core-functionality-and-scope-2025-12-07.md`*
    - *Defines: MVP features (15 Must-Haves), Simplified Architecture (localStorage + Supabase Auth), Data Flow, localStorage Schema, 3-4 week timeline.*

- [X] **Research**

  - [X] /run-agent-task analyst *research*
    - *File: `research-report-2025-12-07.md`*
    - *Description: Comprehensive research on 3 topics: (1) AI prompt engineering for negotiation agents (2025 best practices, context engineering, tight personas), (2) localStorage limits and offline-first patterns (5-10 MB validated, storage monitoring recommended), (3) Competitive analysis of PM simulation tools (MIT Sloan, Cesim, SimProject, GoVenture—all focus on execution, not planning). Key finding: Our AI negotiation + planning focus + Norwegian context creates unique market position.*
- [X] **Product Brief**

  - [X] /run-agent-task analyst *product-brief*
    - *File: `product-brief.md`*
    - *Description: Concise 2-3 page stakeholder-facing brief synthesizing proposal, brainstorming, PRD, and research. Sections: Vision & Problem, Solution, Target Users (Sara, Magnus, Prof. Eriksen), MVP Scope (15 Must-Haves), Timeline (3-4 weeks), Success Metrics, Unique Value Proposition (vs competitors), Risk Mitigation. Ready for stakeholder approval.*

---

## Phase 1: Planning

- [X] **/run-agent-task pm *prd**
  - *File: `PRD.md`*
  - *Description: Complete Product Requirements Document with 14 sections, 35+ functional requirements, 30+ user stories, technical specs. Updated to v2.0 for POC scope (3 negotiable WBS + 4 AI agents, 310/390/700 MNOK budget model, inflexible time constraint).*
- [X] **/run-agent-task pm *validate-prd**
  - *File: `validation-report-PRD-2025-12-07.md`*
  - *Description: Comprehensive validation checklist with 111 review items across completeness, clarity, consistency, feasibility, alignment, user-centricity, and actionability. Result: 97% pass rate (34/35 items passed).*
- [X] **/run-agent-task ux-designer *create-ux-design**
  - *File: `ux-design-specification.md`*
  - *Description: Complete UX Design Specification with 9 sections: Design Principles, Visual Design System (colors, typography, spacing), Wireframes (Login, Dashboard, Chat, Modals), User Flows (3 detailed flows), Component Specifications (5 components with TSX code), Interaction Patterns, Responsive Design (desktop + tablet), Accessibility (WCAG 2.1 Level A), Implementation Notes (Tailwind, Shadcn, Norwegian strings). Updated to v2.0 for POC scope.*
- [X] **/run-agent-task ux-designer *validate-ux-design**
  - *File: `validation-report-UX-Design-2025-12-07.md`*
  - *Description: UX Design validation with 90+ review items across Visual Design System, Wireframes, User Flows, Components, Interactions, Responsive Design, Accessibility, Implementation Readiness, PRD Alignment. Result: 96% pass rate (119.5/124 items), APPROVED for implementation.*

---

## Phase 2: Solutioning

- [X] **/run-agent-task architect *create-architecture**
  - *File: `architecture.md` (Note: Key decisions captured in `brainstorming-technical-architecture-report.md`)*
  - *Description: Technical architecture validated through research. Stack: React + TypeScript + Tailwind CSS + Shadcn UI (frontend), FastAPI (backend), Supabase PostgreSQL (storage + auth), Gemini 2.5 Flash (AI), Vercel (hosting). Architecture updated to support database-backed sessions for multi-device capability.*
- [X] **/run-agent-task pm *create-epics-and-stories**
  - *File: `epics.md`*
  - *Description: 10 epics broken into 42 user stories totaling 125 story points. Updated to v2.0 for POC scope: 3 negotiable + 12 locked WBS, 4 AI agents (Owner + 3 suppliers), explicit accept/reject flow, budget display (310/390/700). Sprint plan defined for 4-5 weeks. Includes acceptance criteria, technical notes, and traceability to PRD.*
- [X] **/run-agent-task tea *test-design**
  - *File: `test-design.md`*
  - *Description: Comprehensive test strategy with 60%+ coverage target. Includes unit tests (Vitest), integration tests (React Testing Library), E2E tests (Playwright), AI quality testing (50 scenarios), UAT plan (5-10 students), performance testing (Lighthouse), accessibility testing (WCAG 2.1 Level A), security testing. 90+ test cases defined across 8 epics.*
- [X] **/run-agent-task architect *solutioning-gate-check**
  - *File: `solutioning-gate-check.md`*
  - *Description: Final readiness assessment before Phase 3. Result: ✅ GO (Approved to proceed). Documentation 100% complete (Phase 0, 1, 2), architecture validated, 7/7 decision criteria met, medium risk level with mitigation strategies, 90% confidence in 3-4 week delivery. 4 non-critical blockers identified, all resolvable Week 1-2.*
- [X] **API & Database Integration Guide**
  - *File: `API_DATABASE_INTEGRATION_GUIDE.md`*
  - *Description: Comprehensive 2000+ line guide for Gemini API and Supabase PostgreSQL integration. Covers database schema (4 tables), backend API endpoints (11 endpoints), frontend integration patterns, security best practices, complete SQL migrations and code examples.*
- [X] **UX Functional Flows & Visualizations**
  - *Files: `docs/ux/functional_flows/` (7 flow diagrams + 2 visualizations)*
  - *Description: Complete functional flow diagrams (validation rules, budget calculation, AI negotiation, commitment flow, state management, error handling, critical path/timeline) and visualization designs (Gantt chart, precedence diagram). 10 SVG files total.*
  - *Implementation Note: Visualizations will be built using gantt-task-react (Gantt) and ReactFlow (Precedence) libraries, configured to match the designs. See `docs/Precedence-And-Gantt.md` for implementation guide.*
- [X] **WBS Source Data**
  - *File: `docs/data/wbs.pdf`*
  - *Description: Complete Work Breakdown Structure with all 70+ work packages including IDs, names, responsibilities, durations, start/end dates, dependencies, deliverables, and cost estimates (totaling 700 MNOK). Source data ready for conversion to JSON.*

---

## Phase 3: Implementation - **75% COMPLETE** ✅

**Status as of December 16, 2025:**

- ✅ Core POC functionality operational
- ✅ Full AI negotiation loop working
- ⚠️ Missing session completion and some validation features
- ⏸️ Advanced visualizations not implemented

### Sprint 1 - Foundation & Infrastructure (Week 1) - ✅ COMPLETE

- [X] **Supabase Authentication Setup**

  - *Files: `backend/config.py`, `backend/main.py`, `frontend/lib/supabase/`*
  - *Description: Supabase project configured (cmntglldaqrekloixxoc.supabase.co). Email auth enabled. JWT validation with JWKS implemented. Frontend SSR auth library integrated. Environment variables configured.*
- [X] **User Registration & Login**

  - *Files: `frontend/app/auth/`, `frontend/components/sign-up-form.tsx`, `frontend/components/login-form.tsx`*
  - *Description: Complete auth flows with email/password. Registration, login, forgot password, update password pages. Error handling, loading states, redirects to protected pages implemented.*
- [X] **Chat Interface UI (Basic)**

  - *Files: `frontend/components/chat-interface.tsx`, `frontend/app/chat/chat-page-client.tsx`, `frontend/app/chat/page.tsx`*
  - *Description: Chat UI with message display (user/agent bubbles), textarea input, send button, agent selection screen. Scrollable chat window with auto-scroll. Loading states with typing indicator. Simulated responses (not yet connected to backend AI).*
- [X] **AI Agent System Prompts (All 4 Agents)**

  - *File: `docs/AI_AGENT_SYSTEM_PROMPTS.md` (682 lines)*
  - *Description: Complete system prompts for all 4 AI agents with detailed personas, negotiation parameters, and behavioral rules. Owner: Anne-Lise Berg (Municipality - budget approval, NO time extensions). Supplier 1: Bjørn Eriksen (Price/quality negotiation). Supplier 2: Kari Andersen (Time/cost tradeoffs). Supplier 3: Per Johansen (Scope reduction). Includes testing guidelines and 10+ test scenarios per agent.*
- [X] **Prompts Viewer Page**

  - *File: `frontend/app/prompts/page.tsx`*
  - *Description: Server-side page that reads and displays AI_AGENT_SYSTEM_PROMPTS.md as formatted markdown. Uses ReactMarkdown with GitHub-flavored markdown support. Accessible at /prompts with navigation link from homepage.*
- [X] **Backend Dependencies Installation**

  - *File: `backend/requirements.txt`*
  - *Description: All required packages installed including FastAPI, Supabase, python-jose, pydantic-settings, google-generativeai (Gemini API), uvicorn. Ready for implementation.*
- [X] **Static Data Files (JSON conversion)**

  - *Status: COMPLETE. Both wbs.json and agents.json created and deployed.*
  - *Files: `frontend/public/data/wbs.json` (15 WBS items: 3 negotiable + 12 locked, 310/390/700 MNOK structure) and `frontend/public/data/agents.json` (4 AI agents with full configurations).*
  - *Description: WBS data extracted from wbs.pdf with complete metadata (budget, dependencies, critical path, suppliers). Agent configs extracted from AI_AGENT_SYSTEM_PROMPTS.md with capabilities, negotiation styles, and cost multipliers.*
- [X] **Database Schema Creation**

  - *Status: COMPLETE. All SQL migrations written and ready for import.*
  - *Files: `database/migrations/001_complete_schema.sql` (627 lines), `IMPORT_TO_SUPABASE.md` (import guide).*
  - *Description: 5 tables created (game_sessions, wbs_commitments, negotiation_history, agent_timeouts, user_analytics). Includes RLS policies, indexes, triggers, computed columns. Import guide provided.*
  - *⚠️ Verification Needed: Confirm schema has been imported to Supabase production instance.*
- [X] **Backend API Endpoints**

  - *Status: COMPLETE. All core endpoints implemented.*
  - *Files: `backend/main.py` (742 lines, 10 endpoints), `backend/services/gemini_service.py` (222 lines), `backend/prompts/agent_prompts.py` (143 lines).*
  - *Endpoints Implemented:*
    - ✅ GET / (health check)
    - ✅ GET /me (current user)
    - ✅ POST /api/chat (AI chat with Gemini 2.5 Flash)
    - ✅ GET/POST/PUT /api/sessions (session CRUD)
    - ✅ POST /api/sessions/{id}/commitments (create commitment)
    - ✅ GET /api/sessions/{id}/commitments (list commitments)
    - ✅ GET /api/sessions/{id}/history (negotiation history)
  - *Services: Gemini API integration, agent prompts loader, JWT auth, RLS-compliant database client.*

**Sprint 1 Progress:** 10/10 tasks complete (100%). ✅ SPRINT 1 COMPLETE.

---

### Sprint 2-5 - Core Features (Weeks 2-5) - **MOSTLY COMPLETE**

- [X] **Dashboard & Budget Tracking** (Week 2) - ✅ COMPLETE

  - *Status: Fully implemented with comprehensive budget visualization.*
  - *Files: `frontend/app/dashboard/page.tsx`, `frontend/components/budget-display.tsx`, `frontend/components/budget-summary.tsx`, `frontend/components/wbs-item-card.tsx`*
  - *Features Implemented:*
    - ✅ 3-tier budget display (310/390/700 MNOK with color-coded tiers)
    - ✅ WBS list component (3 negotiable highlighted green, 12 locked grayed)
    - ✅ Real-time budget updates after commitments
    - ✅ Status indicators (pending/completed/locked)
    - ✅ Agent information panel with avatars
    - ✅ Budget challenge indicators (35 MNOK deficit warning)
    - ✅ Session creation/retrieval flow
    - ✅ Navigation to negotiation pages
- [X] **AI Negotiation System** (Week 3) - ✅ COMPLETE

  - *Status: Fully operational with Gemini 2.5 Flash integration.*
  - *Files: `backend/services/gemini_service.py`, `frontend/app/game/[sessionId]/[agentId]/[wbsId]/page.tsx`, `frontend/components/chat-interface.tsx`, `frontend/lib/api/chat.ts`*
  - *Features Implemented:*
    - ✅ Gemini service with agent prompts from AI_AGENT_SYSTEM_PROMPTS.md
    - ✅ POST /api/chat endpoint with full context injection (system prompt + conversation history + game state)
    - ✅ Offer detection and parsing (regex-based extraction)
    - ✅ Negotiation history persistence to database
    - ✅ Explicit accept/reject buttons on detected offers
    - ✅ Disagreement tracking (6-disagreement timeout mechanic)
    - ✅ Real-time chat UI with message bubbles
    - ✅ Budget impact preview in sidebar
    - ✅ Auto-redirect after commitment
    - ✅ Chat history persistence and loading (fixed session resumption issue)
- [X] **Plan Management & Validation** (Week 3-4) - ✅ CORE COMPLETE

  - *Status: Core commitment flow fully implemented, session completion added, advanced validations deferred.*
  - *Files: `backend/main.py` (commitments endpoints), `frontend/components/chat-interface.tsx` (offer acceptance)*
  - *Features Implemented:*
    - ✅ Commitment flow with offer acceptance
    - ✅ Budget validation (≤700 MNOK total, ≤310 MNOK available)
    - ✅ Duplicate commitment prevention
    - ✅ Database persistence via POST /api/sessions/{id}/commitments
    - ✅ Session budget updates
    - ✅ Error handling with user feedback
    - ✅ Session completion flow with results page
    - ✅ Automatic snapshot creation on contract acceptance
  - *Nice to Have (Future Development):*
    - ❌ Renegotiation (uncommit) functionality
    - ❌ Dependency validation against WBS structure
    - ❌ Timeline validation (deadline ≤May 15 2026)
    - ❌ Modal confirmations for commitments
- [X] **Visualization Features** (Week 4-5) - ✅ COMPLETE

  - *Status: Fully implemented with shared calculation engine.*
  - *Files: `frontend/components/gantt-chart.tsx`, `frontend/components/precedence-diagram.tsx`, `frontend/lib/timeline-calculator.ts`*
  - *Features Implemented:*
    - **Gantt Chart** (using `gantt-task-react`)
      ✅ Timeline rendering with Month view mode
      ✅ Dynamic date calculations based on commitments
      ✅ Color scheme: Blue (negotiable), Grey (committed/locked)
      ✅ Critical path highlighting with red outline
      ✅ Dependency arrows
      ✅ Uses shared timeline calculator
    - **Precedence Diagram** (using `ReactFlow`)
      ✅ Activity-on-Node (AON) network diagram
      ✅ Zoom, pan, drag interactions
      ✅ Node display: WBS ID, name, ES/EF/LS/LF, slack time
      ✅ Critical path from wbs.json (business definition)
      ✅ Persistent layout saved to localStorage
      ✅ Reset layout button
      ✅ Uses shared timeline calculator
    - **Shared Timeline Calculator** (`lib/timeline-calculator.ts`)
      ✅ CPM algorithm (forward/backward pass)
      ✅ ES/EF/LS/LF calculation
      ✅ Slack/float calculation
      ✅ Dynamic duration selection (committed > locked > baseline)
      ✅ Single source of truth for both diagrams
    - ✅ Tabbed navigation between Gantt and Precedence views
  - *Missing Features:*
    - ❌ History/timeline view (snapshot visualization)
  - *Implementation Time: 8 hours (Dec 22, 2025)*
- [X] **Export & Polish** (Week 5) - ⚠️ PARTIALLY COMPLETE

  - *Status: Some polish complete, export missing.*
  - *Features Implemented:*
    - ✅ Session management (create/retrieve/update)
    - ✅ Design system with comprehensive color palette
    - ✅ Error handling and loading states
    - ✅ Responsive UI components (Tailwind + Shadcn)
    - ✅ Testing scripts (backend/test_chat.py, test_setup.py, etc.)
    - ✅ Troubleshooting documentation (TROUBLESHOOTING_REPORT_DEC_16.md)
    - ✅ Chat history fix (backend RLS + frontend session resume logic)
  - *Missing Features:*
    - ❌ Session export as JSON/PDF
    - ❌ Help documentation modal in UI
    - ❌ Integration testing with Playwright
    - ❌ Agent timeout UI countdown
    - ❌ Session completion page

**Current Progress:** Sprint 2-3 features ~95% complete. Sprint 4-5 features ~85% complete (visualizations done, history panel working). Core negotiation loop fully functional. Vendor contract acceptance fully implemented with automatic snapshot creation. Owner perspective budget revision acceptance NOT yet implemented (requires frontend UI, backend endpoint, and snapshot type).

---

## Phase 4: Testing & Quality Assurance - **NOT STARTED**

- [ ] **Unit Testing (Vitest)**

  - *Description: Backend endpoints (sessions, chat, commitments), frontend components, utility functions (budget validation, critical path calculation). Target: 60%+ coverage.*
- [ ] **Integration Testing (React Testing Library)**

  - *Description: Component interactions (Dashboard updates after commitment), auth flows end-to-end, database operations with RLS policies, API error handling.*
- [ ] **E2E Testing (Playwright)**

  - *Description: Full user journeys (register → login → negotiate with 4 agents → commit 3 packages → validate plan → export session). Error scenarios (budget exceeded, timeline violations). Multi-browser testing.*
- [ ] **AI Quality Testing**

  - *Description: 50 test scenarios per agent using prompts from AI_AGENT_SYSTEM_PROMPTS.md (200 tests total). Verify Owner 100% rejects time extensions, verify supplier negotiation ranges (price floors, concession rates), measure response consistency.*
- [ ] **Performance & Accessibility Testing**

  - *Description: Lighthouse audit (target: 90+ performance score), load testing (50 concurrent users), AI response times (<3 seconds), WCAG 2.1 Level A compliance, keyboard navigation, screen reader testing.*
- [ ] **Security Testing**

  - *Description: JWT validation, Supabase RLS policy verification, input sanitization (XSS/SQL injection prevention), CORS configuration, rate limiting on chat endpoint, API key protection.*

---

## Phase 5: Deployment & Launch - **NOT STARTED**

- [ ] **Database Production Setup**

  - *Description: Run SQL migrations in Supabase production environment. Configure RLS policies. Set up automated backups. Configure connection pooling. Set up monitoring and alerting.*
- [ ] **Backend Deployment (Railway/Render/Fly.io)**

  - *Description: Deploy FastAPI to cloud platform. Configure production environment variables (GEMINI_API_KEY, SUPABASE credentials). Set up HTTPS. Configure CORS for production domain. Set up logging with Sentry. Add rate limiting middleware.*
- [ ] **Frontend Deployment (Vercel)**

  - *Description: Deploy Next.js to Vercel with auto-deploy on git push. Configure environment variables (NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_API_URL). Test auth flow in production. Optimize build. Set up error tracking.*
- [ ] **Production Testing & Launch**

  - *Description: Smoke testing all endpoints in production. Test AI chat with real Gemini API. Test session creation and commitment flow. Monitor logs for errors. Prepare instructor/student documentation. Plan pilot with LOG565 class.*

---

## Overall Progress Summary

- **Phase 0 (Discovery & Analysis):** ✅ 100% Complete (8/8 tasks)
- **Phase 1 (Planning):** ✅ 100% Complete (5/5 tasks)
- **Phase 2 (Solutioning):** ✅ 100% Complete (8/8 tasks)
- **Phase 3 (Implementation):** ✅ ~92% Complete (10/10 Sprint 1 tasks, 4.5/5 Sprint 2-5 themes - visualizations complete, vendor contract acceptance complete, chat history fixed, owner budget revision not yet implemented)
- **Phase 4 (Testing):** ⏸️ Not Started (0/6 test categories)
- **Phase 5 (Deployment):** ⏸️ Not Started (0/4 deployment tasks)

**Key Achievements (Updated December 23, 2025):**

- ✅ Sprint 1 foundation 100% complete
- ✅ All 4 AI agent prompts fully documented (682 lines) and integrated with Gemini API
- ✅ Complete WBS and agent data files (wbs.json, agents.json)
- ✅ Database schema created (6 tables including session_snapshots, RLS policies, triggers)
- ✅ Backend API fully operational (14 endpoints including snapshots, Gemini service, auth with RLS-enforced client)
- ✅ Dashboard with 3-tier budget visualization
- ✅ Full AI negotiation loop (chat, offer detection, accept/reject, persistence)
- ✅ **Chat history persistence** - Fixed critical bug with session resumption (Dec 23, 2025)
- ✅ **Vendor contract acceptance fully implemented** - 12-step data flow from UI to database with validation
- ✅ **Automatic snapshot system** - Creates snapshots on contract acceptance with complete timeline data
- ✅ **History Panel with Gantt/Precedence reconstruction** - Renders snapshots with full ES/EF/LS/LF data
- ✅ **Gantt Chart & Precedence Diagram** - Full visualizations with critical path, shared timeline calculator
- ✅ Auth system fully functional
- ✅ Design system with comprehensive color palette
- ✅ 50+ documentation files including detailed baseline snapshot implementation guide

**Remaining Gaps (MVP Completion):**

1. ✅ **Session Completion Flow** - COMPLETE with results summary page
2. ✅ **Database Import Verification** - COMPLETE, all tables working
3. ✅ **Visualizations** - COMPLETE, Gantt and Precedence fully functional
4. ✅ **Vendor Contract Acceptance** - COMPLETE, full 12-step flow with snapshots
5. ✅ **Chat History Persistence** - COMPLETE, fixed session resumption bug (Dec 23, 2025)
6. ✅ **Baseline Snapshot in History Panel** - COMPLETE via client-side workaround.
7. ✅ **Dependency Validation** - COMPLETE. (2-3 hours)
8. ✅ **Timeline Validation** - COMPLETE. (3-4 hours)
9. ❌ **Owner Perspective Budget Revision** - NOT IMPLEMENTED (no UI, no endpoint, no snapshots) (6-8 hours)

**Nice to Have (If Time Permits):**
10. ❌ **Renegotiation (Uncommit)** - Cannot undo commitments (3-4 hours)
11. ❌ **Export Functionality** - Session export endpoint exists but needs frontend UI (2-3 hours)
12. 🟡 **History Panel UX Polish** - Core working, optional enhancements (2-3 hours)
13. ⏸️ **Agent Timeout UI** - Visual countdown for 6-disagreement timeout (3 hours)
14. ⏸️ **Mobile Responsiveness** - Desktop-first, limited mobile support (8-12 hours)
15. ⏸️ **Help Documentation Modal** - In-app help system (1-2 hours)
16. ❌ **Administration Panel** - Teacher dashboard to view all student sessions/results from database (12-16 hours)
17. ❌ **Automated Testing** - No unit/integration/E2E test suite (40+ hours)

**Next Priority Actions (Critical for MVP - 6-8 hours total):**

1. **Implement Owner Perspective Budget Revision Acceptance** (6-8 hours)
   - Frontend: BudgetRevisionOfferBox component
   - Backend: POST /budget-revision endpoint
   - Database: Budget revision snapshot creation
   - History Panel: Display budget revision snapshots
   - See detailed checklist in Phase 2 of "MVP Completion Checklist" section

---

## BMAD Workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">
