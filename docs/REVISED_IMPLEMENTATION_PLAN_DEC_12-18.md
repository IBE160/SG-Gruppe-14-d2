# Revised Implementation Plan: Nye Hædda Barneskole PM Simulator
## Development Sprint: December 12-18, 2025

**Document Version:** 3.0 (Next.js Adaptation)
**Date:** December 12, 2025
**Target Completion:** December 18, 2025 (EOD)
**Team:** SG-Gruppe-14-d2

**v3.0 Scope & Framework Correction:**
This document replaces the `IMPLEMENTATION_PLAN_DEC_9-15.md`. The original plan was based on a standard React (Vite) framework, which does not match the existing Next.js codebase. This revised plan adapts the original goals and features to be implemented idiomatically within the Next.js 14+ App Router paradigm.

**Architectural Changes:**
- **Frontend Framework:** Next.js 14+ with App Router (instead of `react-router-dom`).
- **Backend API:** Next.js API Routes (`/app/api/...`) will be used for AI chat, simplifying the architecture by removing the need for a separate FastAPI backend.
- **Authentication:** Supabase Auth will be handled via Next.js Server Actions and Middleware for improved security and performance.
- **Component Model:** A mix of Server Components (for data fetching) and Client Components (for interactivity) will be used.
- **Styling:** Tailwind CSS will be used, as configured in the starter project.

---

## Executive Summary

This document provides a revised, actionable implementation plan to build the Nye Hædda Barneskole Project Management Simulator using the existing Next.js codebase. The core features and learning objectives from the original plan are preserved, but the technical execution is updated to align with modern Next.js best practices.

### Current State Assessment (December 12)

**✅ Completed:**
- ✅ Basic Next.js project setup (`create-next-app` starter).
- ✅ Supabase and Tailwind CSS are installed and partially configured.

**❌ Not Started (Critical Path):**
- ❌ All application-specific logic and UI.
- ❌ Supabase Authentication (sign-up, sign-in, protected routes).
- ❌ Gemini AI Integration.
- ❌ Dashboard UI (Budget display, WBS list).
- ❌ Session management (state, Supabase database).
- ❌ Core simulation loop (negotiation, commitment, validation).
- ❌ Static data integration (`wbs.json`, `agents.json`).

---

## Day-by-Day Implementation Plan

### Friday, December 12 (Day 1): Foundation & Authentication

**Goal:** Infrastructure ready, authentication working, static data prepared.

#### Task 1.1: Supabase Environment Setup (1 hour)
**Status: Unchanged from original plan.**
1. Ensure Supabase project is created and API keys are available.
2. Create a `.env.local` file in the `frontend` directory.
3. Add your Supabase URL and ANON key to `.env.local`:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://[your-project-id].supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=[your-anon-key]
   ```
4. **Important:** Add `.env.local` to the `frontend/.gitignore` file if it's not already there.

#### Task 1.2: Prepare Static Data Files (1 hour)
**Status: Updated for v2.0 POC scope.**
1. Create `frontend/public/data/wbs.json`.
   - **15 total WBS items:** 3 marked as `negotiable: true`, 12 marked as `negotiable: false, status: "contracted"`
   - Reference: `docs/SCOPE_CHANGE_TASKS.md` for budget breakdown
2. Create `frontend/public/data/agents.json`.
   - **4 agents** (1 Owner + 3 Suppliers) as specified in `docs/AI_AGENT_SYSTEM_PROMPTS.md`
   - **Owner:** Anne-Lise Berg (Municipality)
     - `time_extension_allowed: false` (CRITICAL: 100% rejection of time extensions)
     - Can approve budget increases with strong argumentation
   - **Supplier 1:** Bjørn Eriksen (Grunnarbeid) - Price/quality negotiation
   - **Supplier 2:** Kari Andersen (Fundamentering) - Time/cost trade-offs
   - **Supplier 3:** Per Johansen (Råbygg) - Scope reduction proposals

#### Task 1.3: Create Supabase Clients (1 hour)
1. **Client Component Client:** Create `frontend/lib/supabase/client.ts`. This client is for use in Client Components.
   ```typescript
   import { createBrowserClient } from '@supabase/ssr'

   export function createClient() {
     return createBrowserClient(
       process.env.NEXT_PUBLIC_SUPABASE_URL!,
       process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
     )
   }
   ```
2. **Server Action/API Route Client:** Create `frontend/lib/supabase/server.ts`. This is for server-side logic.
   ```typescript
   import { createServerClient, type CookieOptions } from '@supabase/ssr'
   import { cookies } from 'next/headers'

   export function createClient(cookieStore: ReturnType<typeof cookies>) {
     return createServerClient(
       process.env.NEXT_PUBLIC_SUPABASE_URL!,
       process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
       {
         cookies: {
           get(name: string) {
             return cookieStore.get(name)?.value
           },
           set(name: string, value: string, options: CookieOptions) {
             cookieStore.set({ name, value, ...options })
           },
           remove(name: string, options: CookieOptions) {
             cookieStore.set({ name, value: '', ...options })
           },
         },
       }
     )
   }
   ```

#### Task 1.4: Implement Authentication Flow (2 hours)
1. **Create Login Page:** Create `frontend/app/login/page.tsx`. This will be a simple page with a form for email and password.
2. **Create Auth Server Actions:** Create `frontend/app/auth/actions.ts` to handle sign-in, sign-up, and sign-out logic.
   ```typescript
   'use server';
   import { createClient } from '@/lib/supabase/server';
   import { cookies } from 'next/headers';
   import { redirect } from 'next/navigation';

   export async function signIn(formData: FormData) {
     // ... sign in logic using supabase.auth.signInWithPassword
     // redirect to /dashboard on success
   }

   export async function signUp(formData: FormData) {
     // ... sign up logic using supabase.auth.signUp
     // redirect to /dashboard on success
   }
   ```
3. **Modify Login Page:** The form on `app/login/page.tsx` will call these server actions.
4. **Create Protected Dashboard Page:** Create an empty `frontend/app/dashboard/page.tsx`.
5. **Create Middleware for Protected Routes:** Create `frontend/middleware.ts` to protect the `/dashboard` route and redirect unauthenticated users to `/login`.

---

### Saturday, December 13 (Day 2): Dashboard & Data Display

**Goal:** A logged-in user can see the main dashboard with budget and WBS information.

#### Task 2.1: Session Management Hooks (1 hour)
1.  **Create a Zustand store** for client-side session state management: `frontend/lib/store/session-store.ts`. This will hold the game session data fetched from Supabase database via API calls.
    *   `initializeSession`, `loadSession`, `saveSession` functions will use Supabase client to interact with `game_sessions` table (see `docs/SCOPE_CHANGE_TASKS.md` Section 5.4 for schema).

#### Task 2.2: Build Dashboard Page (3 hours)
1. **Flesh out `frontend/app/dashboard/page.tsx`**:
   *   This will be a **Server Component**.
   *   It will read the static `wbs.json` and `agents.json` files from the `public` directory using `fs/promises`.
   *   It will render the main layout of the dashboard.
2. **Create `GameSessionProvider` Client Component**:
   *   This component will run on the client and will be responsible for loading the game session from Supabase database (via API call to `GET /api/sessions`) into the Zustand store.
   *   It will wrap the main content of the dashboard page.
3. **Create `ConstraintPanel` Component**:
   *   Create `frontend/components/dashboard/constraint-panel.tsx`.
   *   This Client Component will subscribe to the session store and display the current budget and timeline.
4. **Create `WBSList` Component**:
   *   Create `frontend/components/dashboard/wbs-list.tsx`.
   *   This Client Component will display the list of WBS items, showing their status (pending, contracted) based on the session store data.

---

### Sunday, December 14 (Day 3): AI Integration & Chat

**Goal:** User can select a WBS item, choose a supplier, and negotiate with a Gemini-powered AI agent.

#### Task 3.1: Create Chat API Route (3 hours)
1. **Create the API Route:** Create the file `frontend/app/api/chat/route.ts`.
2. **Implement Gemini Logic:**
   *   This route will receive a POST request with the chat history, WBS code, and supplier ID.
   *   It will read the `agents.json` and `wbs.json` data to construct the system prompt for the Gemini model, just like in the original Python backend plan.
   *   It will use the `google-generativeai` npm package to call the Gemini API.
   *   It will parse the AI's response to extract any formal offers (cost/duration) and send the reply back to the client.

#### Task 3.2: Build Chat Page and Components (3 hours)
1. **Create Chat Page:** Create `frontend/app/dashboard/chat/[wbsCode]/[supplierId]/page.tsx`. This page will fetch the relevant WBS item and supplier details.
2. **Create `SupplierModal` Component:** Create `frontend/components/dashboard/supplier-modal.tsx`. This modal will appear when a user clicks "Kontakt Leverandør" on the WBS list.
3. **Create `ChatWindow` Component:** Create `frontend/components/chat/chat-window.tsx`.
   *   This is the main interactive client component for the chat.
   *   It will manage the state of the conversation (messages, user input, loading state).
   *   The "Send" button will call our `/api/chat` API route.
   *   It will display messages and any offers from the AI, along with an "Accept Offer" button.

---

### Monday, December 15 (Day 4): Core Simulation Loop

**Goal:** Implement the logic for committing to offers, renegotiating, and validating the final plan.

#### Task 4.1: Implement Commitment & Renegotiation (4 hours)
1. **Create `sessionActions.ts` Server Actions:**
   *   `commitOffer(wbsCode, supplierId, cost, duration)`: This action will update the game session state, add the item to the `current_plan`, and recalculate metrics. It will include dependency validation.
   *   `renegotiate(wbsCode)`: This action will remove an item from the `current_plan`, preparing it for a new negotiation.
2. **Update `ChatWindow`:** The "Accept Offer" button will now call the `commitOffer` server action. Upon success, it should show a confirmation and redirect the user back to the dashboard.
3. **Update `WBSList`:** The "Reforhandle" button will call the `renegotiate` server action.

#### Task 4.2: Implement Plan Validation & Submission (3 hours)
1. **Create `ValidationModal` Component:** Create `frontend/components/dashboard/validation-modal.tsx` to display success or failure messages.
2. **Create `validatePlan` Server Action:**
   *   This action will be called when the user clicks a "Submit Plan" button on the dashboard.
   *   It will perform the validation logic (budget, timeline, completeness) from the original plan.
   *   It will return a result object indicating success or a list of errors.
3. **Update Dashboard Page:** The dashboard will have a "Submit Plan" button that calls the `validatePlan` action and displays the `ValidationModal` with the results.

---

### Tuesday, December 16 (Day 5): Finalizing & Polish

**Goal:** Ensure the application is stable, looks good, and is ready for user testing.

#### Task 5.1: Styling and UI Polish (4 hours)
*   Review all pages and components, applying Tailwind CSS classes to match the UX mockups and ensure a clean, professional look.
*   Add loading spinners, disabled states, and toast notifications for a better user experience.

#### Task 5.2: Implement Session Export (2 hours)
*   Create a simple "Export Session" button in the validation success modal that stringifies the session state from the store and triggers a file download.

#### Task 5.3: End-to-End Testing (2 hours)
*   Manually run through the entire simulation loop: Register -> Login -> Negotiate -> Commit -> Renegotiate -> Submit -> Validate -> Export.
*   **Critical v2.0 test cases:**
    - ✅ Negotiate with Owner AI, request time extension → Verify 100% rejection with explanation
    - ✅ Negotiate with Owner AI, request budget increase with strong argument → Verify conditional approval
    - ✅ Negotiate with 3 suppliers to stay within 310 MNOK available budget
    - ✅ Verify explicit accept/reject flow (two buttons: "✓ Godta" and "✗ Avslå")
    - ✅ Verify no automatic acceptance of offers (user must click button)
    - ✅ Verify budget display shows 3-tier breakdown: 310 available, 390 locked, 700 total
    - ✅ Verify WBS list shows 3 negotiable (blue) and 12 locked (gray) items
*   Fix any bugs found during testing.

---

### Wednesday, December 17 (Day 6): Visualization Features - Epic 10

**Goal:** Implement Gantt Chart, Precedence Diagram, and History/Timeline views.

#### Task 6.1: Gantt Chart View (E10.1) (4 hours)
1. **Create Gantt Component:** Create `frontend/components/visualization/gantt-chart.tsx`.
   *   Install charting library (e.g., Recharts or react-gantt-timeline).
   *   Read session data from Zustand store (15 WBS items: 3 negotiable + 12 locked).
   *   Render task bars:
       - Blue bars for 3 negotiable items (interactive)
       - Gray bars for 12 locked items (read-only)
       - Red 3px border for critical path tasks
   *   Timeline header: January 2025 - May 2026.
   *   "Idag" marker: Vertical red dashed line.
   *   Zoom slider (50%-200%) and view mode dropdown (Dag/Uke/Måned).
2. **Add Critical Path Highlighting:**
   *   Calculate critical path using longest path algorithm.
   *   Highlight critical tasks with red border.
3. **Export to PNG:**
   *   Use html2canvas to export current Gantt view as PNG.

#### Task 6.2: Precedence Diagram View (E10.2) (3 hours)
1. **Create Precedence Component:** Create `frontend/components/visualization/precedence-diagram.tsx`.
   *   Install network diagram library (e.g., react-flow or Cytoscape.js).
   *   Read WBS dependencies from static data + session commitments.
   *   Render nodes (rectangles) showing WBS code, name, duration, cost.
   *   Draw dependency arrows connecting nodes.
   *   Highlight critical path (red borders, red arrows).
2. **Add Interaction:**
   *   Hover on node → Highlight incoming/outgoing arrows.
   *   Click on node → Modal with WBS details.
3. **Layout Controls:**
   *   Layout dropdown: "Venstre→Høyre" / "Topp→Bunn".
   *   Pan/zoom controls.

#### Task 6.3: History/Timeline View (E10.3) (3 hours)
1. **Create History Component:** Create `frontend/components/visualization/history-timeline.tsx`.
   *   Implement overlay panel (slides in from right).
   *   Left sidebar: Event timeline (chronological list of commits/removals/negotiations).
   *   Right panel: Before/after comparison with side-by-side mini Gantt charts.
2. **Version Storage:**
   *   Create `session_snapshots` table in Supabase (or use `plan_history` in JSON format).
   *   Store up to 50 versions per session.
   *   Each snapshot includes: current_plan, metrics, timestamp, action.
3. **Comparison Features:**
   *   Show budget change, timeline change, cascade effects.
   *   Navigation: "← Forrige versjon", "Neste versjon →", "Sammenlign med nåværende".
4. **Export History:**
   *   Download version history as JSON.

---

### Thursday, December 18 (Day 7): Integration, Testing & Deployment

**Goal:** Integrate all Epic 10 features, test thoroughly, and deploy.

#### Task 7.1: Navigation Integration (2 hours)
1. **Add Navigation Tabs:**
   *   Update main navigation to include:
       - 📊 Dashbord
       - 📈 Gantt-diagram
       - 🔀 Presedensdiagram
       - 🕒 Historikk (button in header)
2. **State Persistence:**
   *   Save current view tab in localStorage or URL params.
   *   Restore view on page reload.
3. **Real-time Sync:**
   *   When commitment made on Dashboard → Update Gantt/Precedence in real-time (via database subscription or polling).

#### Task 7.2: End-to-End Testing with Visualization (3 hours)
*   Manually run through entire simulation loop including all visualization views:
    - Register → Login → Dashboard → Negotiate → Commit → **View Gantt** → **View Precedence** → **View History** → Submit → Validate → Export.
    - ✅ Verify Gantt shows 3 blue (negotiable) + 12 gray (locked) bars.
    - ✅ Verify critical path highlighted in red in both Gantt and Precedence.
    - ✅ Verify History shows before/after comparison when commitment made.
    - ✅ Test zoom, filters, layout modes in all visualization views.
    - ✅ Test export to PNG for Gantt and Precedence.
*   Fix any bugs found during testing.

#### Task 7.3: Deployment & Documentation (3 hours)
*   Deploy to Vercel.
*   Clean up code and add comments.
*   Update README.md with Epic 10 features documentation.
