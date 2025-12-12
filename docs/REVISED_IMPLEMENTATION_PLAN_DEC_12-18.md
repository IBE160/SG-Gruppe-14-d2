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
- ❌ Session management (state, localStorage).
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
**Status: Unchanged from original plan.**
1. Create `frontend/public/data/wbs.json`.
2. Create `frontend/public/data/agents.json`.
   *Use the JSON content provided in `docs/IMPLEMENTATION_PLAN_DEC_9-15.md` for both files.*

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
1.  **Create a Zustand store** for client-side session state management: `frontend/lib/store/session-store.ts`. This will hold the game session data loaded from `localStorage`.
    *   `initializeSession`, `loadSession`, `saveSession` functions can be adapted from the original plan and integrated with the store.

#### Task 2.2: Build Dashboard Page (3 hours)
1. **Flesh out `frontend/app/dashboard/page.tsx`**:
   *   This will be a **Server Component**.
   *   It will read the static `wbs.json` and `agents.json` files from the `public` directory using `fs/promises`.
   *   It will render the main layout of the dashboard.
2. **Create `GameSessionProvider` Client Component**:
   *   This component will run on the client and will be responsible for loading the game session from `localStorage` into the Zustand store.
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
*   Fix any bugs found during testing.

---
### Wednesday-Thursday, December 17-18 (Days 6-7): Buffer & Deployment

**Goal:** Deploy the application and prepare for handoff.
*   These days are reserved for bug fixing, addressing feedback, and documentation.
*   Prepare deployment on Vercel (which is straightforward for Next.js apps).
*   Clean up code and add comments where necessary.
