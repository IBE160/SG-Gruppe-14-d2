# Epics and User Stories
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 1.0
**Date:** 2025-12-07
**Status:** Ready for Sprint Planning
**Total Story Points:** 89 (estimated)

---

## Document Purpose

This document breaks down the Product Requirements Document (PRD) into implementation-ready epics and user stories for sprint planning. Each story includes acceptance criteria, technical notes, and estimated effort.

**Target Audience:**
- Development team (implementation)
- Scrum Master (sprint planning)
- Product Owner (prioritization)

---

## Table of Contents

1. [Epic Summary](#epic-summary)
2. [Epic 1: User Authentication & Onboarding](#epic-1-user-authentication--onboarding)
3. [Epic 2: Project Dashboard & Constraints](#epic-2-project-dashboard--constraints)
4. [Epic 3: WBS Management](#epic-3-wbs-management)
5. [Epic 4: AI Supplier Negotiation](#epic-4-ai-supplier-negotiation)
6. [Epic 5: Plan Management & Commitment](#epic-5-plan-management--commitment)
7. [Epic 6: Plan Validation & Submission](#epic-6-plan-validation--submission)
8. [Epic 7: Session Export & Data Management](#epic-7-session-export--data-management)
9. [Epic 8: Help & Documentation](#epic-8-help--documentation)
10. [Epic 9: Infrastructure & DevOps](#epic-9-infrastructure--devops)
11. [Story Point Estimation Guide](#story-point-estimation-guide)

---

## Epic Summary

| Epic ID | Epic Name | Stories | Story Points | Priority | Week |
|---------|-----------|---------|--------------|----------|------|
| **E1** | User Authentication & Onboarding | 3 | 8 | Must Have | Week 1 |
| **E2** | Project Dashboard & Constraints | 4 | 13 | Must Have | Week 2 |
| **E3** | WBS Management | 5 | 13 | Must Have | Week 2 |
| **E4** | AI Supplier Negotiation | 6 | 21 | Must Have | Week 2-3 |
| **E5** | Plan Management & Commitment | 5 | 13 | Must Have | Week 2 |
| **E6** | Plan Validation & Submission | 4 | 8 | Must Have | Week 3 |
| **E7** | Session Export & Data Management | 3 | 5 | Must Have | Week 4 |
| **E8** | Help & Documentation | 2 | 3 | Should Have | Week 4 |
| **E9** | Infrastructure & DevOps | 4 | 5 | Must Have | Week 1 |
| **TOTAL** | **9 Epics** | **36 Stories** | **89 Points*** | - | **3-4 Weeks** |

***Note:** Sprint planning (Section 11) allocates 95 total points (Week 1: 13, Week 2: 28, Week 3: 34, Week 4: 20), which includes a 6-point buffer for testing, integration overhead, and bug fixes beyond individual story estimates.

---

## Epic 1: User Authentication & Onboarding

**Epic Goal:** Enable users to securely register, log in, and start a new game session.

**Priority:** Must Have (Week 1)

**Dependencies:** Supabase Auth setup (E9)

---

### Story E1.1: User Registration

**As a** new user
**I want to** register with email and password
**So that** I can create an account and access the simulation

**Acceptance Criteria:**
- [ ] User navigates to Login page
- [ ] User clicks "Registrer deg" link
- [ ] User enters email (valid format required)
- [ ] User enters password (min 8 characters)
- [ ] System creates Supabase user account
- [ ] System generates JWT token
- [ ] User redirected to Dashboard
- [ ] Error shown if email already exists

**Technical Notes:**
- Use Supabase `auth.signUp()` API
- Store JWT in localStorage: `supabase_auth_token`
- No user profile table needed (JWT contains user_id)

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-1.1

---

### Story E1.2: User Login

**As a** returning user
**I want to** log in with my email and password
**So that** I can resume or start a new game session

**Acceptance Criteria:**
- [ ] User navigates to Login page
- [ ] User enters email and password
- [ ] System validates credentials via Supabase
- [ ] System retrieves JWT token
- [ ] User redirected to Dashboard
- [ ] Error message shown if credentials invalid: "Feil e-post eller passord"
- [ ] Loading state shown during authentication (spinner on button)

**Technical Notes:**
- Use Supabase `auth.signInWithPassword()` API
- Handle errors: invalid credentials, network timeout
- UX: Button text changes to "Logger inn..." during loading

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-1.2, UX Section 3.1

---

### Story E1.3: Session Initialization

**As a** logged-in user
**I want** the system to automatically load or create a game session
**So that** I can start playing immediately

**Acceptance Criteria:**
- [ ] On Dashboard load, check localStorage for `current_session_id`
- [ ] If session exists → load session data from localStorage
- [ ] If no session → create new session with:
  - `game_id`: UUID
  - `user_id`: from JWT
  - `created_at`: timestamp
  - `status`: 'in_progress'
  - `wbs_items`: loaded from wbs.json (15 items)
  - `suppliers`: loaded from suppliers.json (5 suppliers)
  - `current_plan`: empty object
  - `metrics`: initial values (0 budget, 0 negotiations)
- [ ] Save session to localStorage
- [ ] Render Dashboard with session data

**Technical Notes:**
- localStorage key: `nye_haedda_session_{user_id}`
- Load static files: `/data/wbs.json`, `/data/suppliers.json`
- TypeScript interface: `GameSession` (from PRD Section 8)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-2.1, localStorage schema

---

## Epic 2: Project Dashboard & Constraints

**Epic Goal:** Display project constraints (budget, deadline) and real-time updates as user makes decisions.

**Priority:** Must Have (Week 2)

**Dependencies:** E1 (Session initialization), E9 (Static data files)

---

### Story E2.1: Display Project Constraints

**As a** user
**I want to** see the project budget and deadline prominently
**So that** I understand the constraints I must work within

**Acceptance Criteria:**
- [ ] Constraint panel displays at top of Dashboard
- [ ] Budget shown as: "Budsjett: [used] / 700 MNOK ([percentage]%)"
- [ ] Deadline shown as: "Frist: 15. mai 2026"
- [ ] Budget progress bar visualizes usage (green <97%, yellow 97-100%, red >100%)
- [ ] Projected end date shown if calculable
- [ ] Checkmark ✓ if projected < deadline, X ✗ if late

**Technical Notes:**
- Calculate `used` from `current_plan` entries: sum of all `cost` values
- Calculate `projected_end_date` using critical path (max end_date from plan)
- UX: Progress bar uses Shadcn `<Progress>` component
- Colors: green (#10B981), yellow (#F59E0B), red (#EF4444)

**Story Points:** 5

**Priority:** Must Have

**Reference:** PRD FR-2.2, UX Section 3.2 Constraint Panel

---

### Story E2.2: Real-Time Budget Updates

**As a** user
**I want** the budget to update immediately when I commit a quote
**So that** I can see the impact of my decisions in real-time

**Acceptance Criteria:**
- [ ] When user commits quote → `current_plan` updated in localStorage
- [ ] Budget recalculated: sum all `cost` values
- [ ] Progress bar animates to new percentage (500ms transition)
- [ ] Toast notification shown: "[WBS code] [name] lagt til i plan"
- [ ] If budget >680 MNOK (97%) → warning toast: "⚠️ Budsjett på 97%..."

**Technical Notes:**
- Use React state + localStorage sync
- Animation: `transition: width 500ms ease-in-out` (UX Section 6.1)
- Toast: Shadcn `toast()` API, 3-second auto-dismiss

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-5.3, UX Section 6.1 Real-Time Updates

---

### Story E2.3: Real-Time Timeline Updates

**As a** user
**I want** the projected end date to update when I commit a quote
**So that** I know if I'm on track to meet the May 15, 2026 deadline

**Acceptance Criteria:**
- [ ] When user commits quote → calculate `start_date` and `end_date` based on dependencies
- [ ] Update `projected_end_date` in metrics (max `end_date` from all committed items)
- [ ] Display projected date in constraint panel
- [ ] Show green checkmark if projected ≤ May 15, 2026
- [ ] Show red X if projected > May 15, 2026
- [ ] Warning toast if timeline exceeds deadline

**Technical Notes:**
- Dependency resolution: If WBS 2.1 depends on 1.3.1, start_date = 1.3.1.end_date + 1 day
- Use topological sort for critical path calculation (PRD Appendix B)
- Date formatting: `date-fns` library, Norwegian locale

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-5.4, Critical Path Algorithm

---

### Story E2.4: Quick Stats Display

**As a** user
**I want to** see summary statistics (progress, negotiations count)
**So that** I can track my overall progress

**Acceptance Criteria:**
- [ ] Display below constraint panel: "Fremdrift: [completed] / 15 WBS-oppgaver fullført | [count] forhandlinger"
- [ ] Update `completed` count when WBS item committed
- [ ] Update `negotiation_count` when user sends message to AI
- [ ] Display `renegotiation_count` separately if >0

**Technical Notes:**
- Calculate from `current_plan` (count entries) and `metrics.negotiation_count`
- Text color: gray-600, text-sm (UX Section 3.2)

**Story Points:** 2

**Priority:** Should Have

**Reference:** UX Section 3.2 Quick Stats

---

## Epic 3: WBS Management

**Epic Goal:** Display WBS list, allow selection, view requirements, and show status.

**Priority:** Must Have (Week 2)

**Dependencies:** E1 (Session), E9 (wbs.json)

---

### Story E3.1: Load and Display WBS List

**As a** user
**I want to** see all 15 WBS items in a list
**So that** I can choose which one to work on

**Acceptance Criteria:**
- [ ] WBS list loads from session data (`session.wbs_items`)
- [ ] Display 15 items in scrollable list (max-height: 500px)
- [ ] Each item shows:
  - Status icon (⚪ pending, 🟢 completed)
  - WBS code and name (e.g., "1.3.1 - Grunnarbeid")
  - Baseline estimate (if pending): "Grunnlag: 100 MNOK, 2 måneder"
  - Committed details (if completed): "105 MNOK, 2.5 måneder | Bjørn Eriksen"
- [ ] Button: "Kontakt Leverandør" (pending) or "Reforhandle" (completed)

**Technical Notes:**
- WBS items sorted by code (1.1, 1.3.1, 2.1, etc.)
- Status determined by checking `current_plan[wbs_code]` existence
- Icons: Lucide `Circle` (pending), `CheckCircle` (completed)

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-3.1, UX Section 3.2 WBS List

---

### Story E3.2: WBS Item Selection

**As a** user
**I want to** click "Kontakt Leverandør" on a WBS item
**So that** I can start negotiating for that item

**Acceptance Criteria:**
- [ ] User clicks "Kontakt Leverandør" button
- [ ] System navigates to Supplier Selection page (or modal)
- [ ] Display WBS item details: code, name, description, requirements (F-codes, K-codes)
- [ ] Show 3-5 available suppliers (from suppliers.json)
- [ ] User selects supplier → navigate to Chat page

**Technical Notes:**
- Route: `/wbs/:wbs_code/suppliers`
- Pass `wbs_code` as URL param or React Router state
- Supplier selection: Radio buttons or card selection UI

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-4.1, UX Section 4.1 User Flow

---

### Story E3.3: View WBS Requirements

**As a** user
**I want to** view detailed requirements for a WBS item
**So that** I can negotiate informed by technical specs

**Acceptance Criteria:**
- [ ] WBS item detail page shows:
  - Full description (from wbs.json)
  - Technical requirements (F-codes, K-codes)
  - Dependencies (prerequisite WBS items)
  - Baseline estimate (cost, duration)
- [ ] Requirements formatted clearly (bullet list)
- [ ] Link to download full kravspec PDF (if available)

**Technical Notes:**
- Requirements stored in `wbs.json`: `requirements: ["F-003", "K-023"]`
- Map F/K codes to descriptions (static mapping in frontend)
- UX: Expandable accordion for requirements (Shadcn Accordion component)

**Story Points:** 2

**Priority:** Should Have

**Reference:** PRD FR-3.2

---

### Story E3.4: WBS Status Indicators

**As a** user
**I want** clear visual indicators of which WBS items are completed
**So that** I can track my progress at a glance

**Acceptance Criteria:**
- [ ] Pending items: Gray circle icon (⚪), gray text
- [ ] Completed items: Green checkmark icon (🟢), darker text
- [ ] Hover state: Background highlight (gray-100)
- [ ] Completed items show commitment details below name

**Technical Notes:**
- CSS: `transition: background-color 200ms` for hover
- Icon size: w-5 h-5 (20px)
- Text hierarchy: WBS code (font-medium), details (text-xs, gray-600)

**Story Points:** 2

**Priority:** Must Have

**Reference:** UX Section 5.4 WBS Item Component

---

### Story E3.5: WBS Filtering (Optional)

**As a** user
**I want to** filter WBS items by status (pending/completed)
**So that** I can focus on remaining tasks

**Acceptance Criteria:**
- [ ] Dropdown or tabs: "Alle" | "Venter" | "Fullført"
- [ ] Filter updates list dynamically
- [ ] Default: "Alle" (show all 15 items)

**Technical Notes:**
- Client-side filtering (no backend)
- Store filter state in React component state

**Story Points:** 3

**Priority:** Could Have (Post-MVP)

**Reference:** N/A (enhancement)

---

## Epic 4: AI Supplier Negotiation

**Epic Goal:** Enable realistic chat-based negotiation with AI supplier personas.

**Priority:** Must Have (Week 2-3)

**Dependencies:** E3 (WBS selection), E9 (FastAPI backend, Gemini API)

**CRITICAL PATH:** Week 3 prompt engineering

---

### Story E4.1: Chat Interface UI

**As a** user
**I want** a clean chat interface to communicate with suppliers
**So that** I can negotiate naturally via text

**Acceptance Criteria:**
- [ ] Chat page displays:
  - Header: Supplier name, role, WBS item
  - Back button: "← Tilbake til Oversikt"
  - Chat window: Scrollable, auto-scroll to bottom
  - Message input: Textarea with "Send" button
  - Document sidebar: Links to WBS, kravspec, project description
- [ ] Chat window height: calc(100vh - 300px)
- [ ] Messages render in bubbles (user: right, AI: left)
- [ ] Timestamps shown (optional)

**Technical Notes:**
- Route: `/wbs/:wbs_code/chat/:supplier_id`
- Chat window: Shadcn `<ScrollArea>` component
- Messages: Array in React state, persisted to localStorage

**Story Points:** 5

**Priority:** Must Have

**Reference:** PRD FR-4.2, UX Section 3.3 Chat Page

---

### Story E4.2: Send Message to AI

**As a** user
**I want to** type and send messages to the AI supplier
**So that** I can request quotes and negotiate

**Acceptance Criteria:**
- [ ] User types message in textarea
- [ ] User clicks "Send" or presses Enter
- [ ] Message appears immediately in chat (optimistic UI)
- [ ] Message sent to FastAPI backend `/api/chat` endpoint
- [ ] Backend proxies to Gemini 2.5 API with system prompt
- [ ] AI response appears in chat (1-3 second delay)
- [ ] Loading indicator: "Bjørn ser gjennom spesifikasjonene..." (typing bubble)

**Technical Notes:**
- POST `/api/chat`: `{ wbs_code, supplier_id, message, chat_history }`
- Response: `{ message, offer: { cost, duration } | null }`
- Store message in `session.chat_logs` (localStorage)

**Story Points:** 5

**Priority:** Must Have

**Reference:** PRD FR-4.3, UX Section 6.2 Loading States

---

### Story E4.3: AI Offer Detection and Display

**As a** user
**I want** AI offers to be clearly highlighted
**So that** I can easily accept them

**Acceptance Criteria:**
- [ ] AI response parsed for cost and duration (regex or structured output)
- [ ] If offer detected → "Godta" button appears below AI message
- [ ] Button shows offer details: "Godta: 105 MNOK, 2.5 måneder"
- [ ] Button styling: Green background (green-600), white text
- [ ] If no offer → no button shown

**Technical Notes:**
- Backend extracts offer from AI response (structured JSON output preferred)
- Regex fallback: `/(\d+)\s*MNOK.*?(\d+(?:\.\d+)?)\s*måneder/i`
- Store `offer` object in message metadata

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-5.1, UX Section 5.5 Chat Message with Offer

---

### Story E4.4: AI Prompt Engineering (System Prompts)

**As a** developer
**I want** detailed system prompts for each supplier
**So that** AI negotiations feel realistic and challenging

**Acceptance Criteria:**
- [ ] Create 5 system prompts using template from Research Report Section 1.4:
  - Bjørn Eriksen (Totalentreprenør)
  - Kari Andersen (Rørlegger)
  - Per Johansen (Elektriker)
  - Silje Henriksen (Arkitekt)
  - Tor Kristoffersen (Maler)
- [ ] Each prompt includes:
  - Role and identity
  - Personality and communication style (tone, voice, philosophy)
  - Hidden negotiation parameters (initial_margin, concession_rate, patience)
  - Task instructions (7-step process)
  - Reasoning structure (internal)
  - Output format (Norwegian, cost/duration format)
- [ ] Test each prompt with 10 sample negotiations
- [ ] Tune concession_rate and patience based on test results

**Technical Notes:**
- Store prompts in `/backend/prompts/{supplier_id}.md`
- Load dynamically in FastAPI `/api/chat` endpoint
- Use Gemini 2.5 Flash (fast, cost-effective for MVP)

**Story Points:** 8 (CRITICAL PATH, HIGH COMPLEXITY)

**Priority:** Must Have

**Reference:** Research Report Section 1.4, PRD FR-4.4

---

### Story E4.5: Negotiation History Persistence

**As a** user
**I want** my chat history saved
**So that** I can review past negotiations and the AI remembers context

**Acceptance Criteria:**
- [ ] All messages stored in `session.chat_logs` array
- [ ] Each message: `{ timestamp, wbs_code, supplier_id, sender: 'user'|'ai', message, offer }`
- [ ] When reopening chat → load history from localStorage
- [ ] AI receives full chat history in API call (context for negotiation)
- [ ] History persists across page refreshes

**Technical Notes:**
- localStorage update on every message send/receive
- Limit history sent to AI: Last 20 messages (token limit management)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-4.5

---

### Story E4.6: Document Sidebar

**As a** user
**I want** quick access to project documents while chatting
**So that** I can reference requirements during negotiation

**Acceptance Criteria:**
- [ ] Sidebar displays (desktop only, 200px width):
  - 📄 WBS (link opens WBS item detail in modal or new tab)
  - 📄 Kravspesifikasjon (link to PDF or embedded text)
  - 📄 Prosjektbeskrivelse (link to project overview)
- [ ] Links styled: Blue text, underline on hover
- [ ] On tablet: Sidebar hidden, floating button shows "📄 Dokumenter" modal

**Technical Notes:**
- Desktop: Fixed sidebar (UX Section 3.3)
- Tablet: Modal with document links (UX Section 7.3)
- Icons: Lucide `FileText`

**Story Points:** 3

**Priority:** Should Have

**Reference:** UX Section 3.3 Document Sidebar

---

## Epic 5: Plan Management & Commitment

**Epic Goal:** Allow users to commit quotes to their plan and manage renegotiations.

**Priority:** Must Have (Week 2)

**Dependencies:** E4 (AI negotiation)

---

### Story E5.1: Commit Quote to Plan

**As a** user
**I want to** accept an AI offer and add it to my project plan
**So that** I can track my budget and timeline

**Acceptance Criteria:**
- [ ] User clicks "Godta" button on AI offer
- [ ] Confirmation modal appears with:
  - WBS item name
  - Supplier name
  - Cost
  - Duration
  - Message: "Dette vil oppdatere prosjektplanen din. Fortsette?"
  - Buttons: "Avbryt" | "Bekreft"
- [ ] User clicks "Bekreft" → plan updated:
  - Calculate `start_date` based on dependencies
  - Calculate `end_date` = start_date + duration
  - Add entry to `current_plan[wbs_code]`: `{ supplier_id, cost, duration, start_date, end_date }`
  - Add entry to `plan_history`: `{ timestamp, action: 'commit', wbs_code, supplier_id, cost, duration }`
- [ ] System message in chat: "✅ Tilbud godtatt og forpliktet til plan"
- [ ] Dashboard updates (budget, timeline, WBS status)
- [ ] Toast notification: "1.3.1 Grunnarbeid lagt til i plan"

**Technical Notes:**
- Modal: Shadcn `<Dialog>` component (UX Section 3.4)
- Dependency resolution: Check `wbs_items[wbs_code].dependencies`
- Update localStorage: `session.current_plan`, `session.plan_history`, `session.metrics`

**Story Points:** 5

**Priority:** Must Have

**Reference:** PRD FR-5.1, UX Section 3.4 Confirmation Modal

---

### Story E5.2: Renegotiation (Remove from Plan)

**As a** user
**I want to** remove a committed WBS item from my plan
**So that** I can renegotiate if I need to reduce budget or time

**Acceptance Criteria:**
- [ ] User clicks "Reforhandle" button on completed WBS item
- [ ] Confirmation modal: "Dette vil fjerne [WBS name] fra planen. Fortsette?"
- [ ] User clicks "Bekreft" → plan updated:
  - Remove entry from `current_plan[wbs_code]`
  - Add entry to `plan_history`: `{ action: 'remove', wbs_code, reason: 'renegotiation' }`
  - Update metrics: `budget_used -= cost`, `renegotiation_count += 1`
- [ ] WBS item status changes: 🟢 → ⚪
- [ ] Chat reopens with history preserved
- [ ] Dashboard updates (budget reduced, timeline recalculated)

**Technical Notes:**
- Preserve chat history (don't clear messages)
- Recalculate dependencies: If WBS 2.1 depended on 1.3.1, 2.1 start_date must be recalculated
- Toast: "1.3.1 Grunnarbeid fjernet fra plan. Du kan nå reforhandle."

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-6.1, UX Section 4.2 Renegotiation Flow

---

### Story E5.3: Plan History Tracking

**As a** user
**I want** a record of all my plan changes
**So that** I can review my decision-making process

**Acceptance Criteria:**
- [ ] `plan_history` array stores all actions:
  - `commit`: User accepted offer
  - `remove`: User renegotiated
- [ ] Each entry: `{ timestamp, action, wbs_code, supplier_id, cost, duration }`
- [ ] History viewable in export JSON (not necessarily in UI for MVP)

**Technical Notes:**
- Stored in `session.plan_history`
- Future enhancement: Timeline visualization of plan changes

**Story Points:** 1

**Priority:** Must Have

**Reference:** PRD Section 8 Data Requirements

---

### Story E5.4: Dependency Validation on Commit

**As a** user
**I want** the system to prevent me from committing a WBS item if dependencies aren't met
**So that** my plan is logically valid

**Acceptance Criteria:**
- [ ] Before commit, check `wbs_items[wbs_code].dependencies`
- [ ] If dependency not committed → show error modal:
  - "Kan ikke forplikte [WBS name] før [dependency name] er fullført"
  - Button: "Tilbake"
- [ ] If dependency met → proceed with commit

**Technical Notes:**
- Dependencies stored in wbs.json: `dependencies: ["1.3.1"]`
- Check: `current_plan["1.3.1"]` exists before allowing commit of WBS 2.1

**Story Points:** 2

**Priority:** Should Have

**Reference:** PRD Appendix B WBS Structure

---

### Story E5.5: Visual Feedback on Commitment

**As a** user
**I want** immediate visual feedback when I commit a quote
**So that** I feel confident my action was successful

**Acceptance Criteria:**
- [ ] Button shows loading spinner during commit (200ms)
- [ ] Modal closes with fade animation (200ms)
- [ ] Dashboard budget bar animates to new value (500ms slide)
- [ ] WBS item icon changes ⚪ → 🟢 with fade (200ms)
- [ ] Toast appears top-right (300ms slide-in)
- [ ] Total feedback time: ~1 second from click to completion

**Technical Notes:**
- Animations: CSS transitions (UX Section 9.3)
- Toast: Auto-dismiss after 3 seconds
- Ensure all state updates before animations start (no flicker)

**Story Points:** 2

**Priority:** Must Have

**Reference:** UX Section 6.1 Real-Time Updates, 9.3 Animations

---

## Epic 6: Plan Validation & Submission

**Epic Goal:** Validate user's plan against constraints and provide feedback.

**Priority:** Must Have (Week 3)

**Dependencies:** E5 (Plan management)

---

### Story E6.1: Submit Plan for Validation

**As a** user
**I want to** submit my completed plan for validation
**So that** I can find out if I successfully met the constraints

**Acceptance Criteria:**
- [ ] "Send Inn Plan" button visible in Dashboard sidebar
- [ ] Button enabled only when all 15 WBS items committed
- [ ] User clicks button → loading overlay appears: "Validerer..."
- [ ] System validates:
  - Budget: total_cost ≤ 700 MNOK (with 3% tolerance: ≤721 MNOK)
  - Timeline: projected_end_date ≤ May 15, 2026
- [ ] Validation completes (<1 second)
- [ ] Show success or error modal

**Technical Notes:**
- Validation runs client-side (no backend call needed)
- Calculate total_cost: sum of all `current_plan[].cost`
- Calculate projected_end_date: max `end_date` from `current_plan`
- Tolerance: Research suggests ±3% acceptable (PRD NFR)

**Story Points:** 3

**Priority:** Must Have

**Reference:** PRD FR-7.1, UX Section 6.2 Loading States

---

### Story E6.2: Validation Success Modal

**As a** user
**I want** a celebratory message when I succeed
**So that** I feel accomplished

**Acceptance Criteria:**
- [ ] Success modal displays:
  - Title: "🎉 Plan Godkjent!"
  - Message: "Gratulerer! Du har lykkes med å fullføre planleggingsfasen."
  - Stats table:
    - Total Kostnad: [cost] MNOK
    - Fullføringsdato: [date]
    - Tid Brukt: [minutes] minutter
    - Forhandlinger: [count]
    - Reforhandlinger: [count]
  - Buttons: "Eksporter Økt" (primary), "Start Nytt Spill" (secondary)
- [ ] Modal cannot be closed without action (no X button)

**Technical Notes:**
- Stats calculated from `session.metrics` and `session.created_at`
- Time calculation: `Math.round((Date.now() - created_at) / 60000)` minutes
- Modal: Full-screen overlay, centered (UX Section 3.6)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-7.2, UX Section 3.6 Success Modal

---

### Story E6.3: Validation Error Modal

**As a** user
**I want** clear feedback on why my plan failed
**So that** I know what to fix

**Acceptance Criteria:**
- [ ] Error modal displays:
  - Title: "❌ Planvalidering Mislyktes"
  - Error list:
    - "Budsjett overskredet med [amount] MNOK (Total: [total], Grense: 700)"
    - "Prosjektet forsinket til [date] (Frist: 15. mai 2026)"
  - Suggestions:
    - "Vurder å reforhandle disse kostbare oppgavene:"
    - List of 3 most expensive WBS items
  - Button: "Tilbake til Planlegging"
- [ ] Modal closes → user returned to Dashboard

**Technical Notes:**
- Calculate overage: `total_cost - 700` MNOK
- Sort WBS items by cost descending, take top 3
- Error messages: Red icon (XCircle), bold text (UX Section 3.5)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-7.3, UX Section 3.5 Validation Error Modal, 4.3 Recovery Flow

---

### Story E6.4: Validation Logic (Critical Path)

**As a** developer
**I want** robust validation logic with edge case handling
**So that** validation is accurate and fair

**Acceptance Criteria:**
- [ ] Budget validation:
  - Pass: total_cost ≤ 700 MNOK
  - With tolerance: total_cost ≤ 721 MNOK (3%)
  - Calculate: `const total = Object.values(current_plan).reduce((sum, item) => sum + item.cost, 0)`
- [ ] Timeline validation:
  - Pass: projected_end_date ≤ May 15, 2026
  - Calculate critical path (longest path through dependencies)
  - Edge case: Circular dependencies should not exist (validated in wbs.json)
- [ ] Completeness validation:
  - All 15 WBS items must be in `current_plan`
  - Edge case: Partial plans not allowed (button disabled until complete)

**Technical Notes:**
- Use date-fns for date comparison: `isBefore(projected_date, new Date('2026-05-15'))`
- Critical path: Topological sort + longest path (PRD Appendix B)
- Unit tests: Test with edge cases (700.01 MNOK, May 14 vs May 16)

**Story Points:** 1

**Priority:** Must Have

**Reference:** PRD FR-7.4, Critical Path Algorithm

---

## Epic 7: Session Export & Data Management

**Epic Goal:** Allow users to export their session data and manage storage.

**Priority:** Must Have (Week 4)

**Dependencies:** E6 (Plan validation)

---

### Story E7.1: Export Session as JSON

**As a** user
**I want to** download my session data as a JSON file
**So that** I can review my work or submit it for grading

**Acceptance Criteria:**
- [ ] "Eksporter Økt" button available:
  - In success modal (after validation pass)
  - In Dashboard sidebar (at any time)
- [ ] User clicks button → JSON file downloads:
  - Filename: `nye_haedda_session_[timestamp].json`
  - Content: Full `GameSession` object (all fields from localStorage)
- [ ] JSON includes:
  - `wbs_items`, `suppliers`, `current_plan`, `plan_history`, `chat_logs`, `metrics`
- [ ] File size: ~50-100 KB (compressed chat history)

**Technical Notes:**
- Use `JSON.stringify(session, null, 2)` for readable formatting
- Trigger download: `<a href="data:text/json;charset=utf-8,{json}" download="{filename}" />`
- No backend needed (client-side download)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-8.1, Export Format Specification

---

### Story E7.2: Clear Session Data

**As a** user
**I want to** start a new game session
**So that** I can play again with a fresh start

**Acceptance Criteria:**
- [ ] "Start Nytt Spill" button in success modal
- [ ] Confirmation dialog: "Dette vil slette nåværende økt. Er du sikker?"
- [ ] User confirms → clear localStorage:
  - Delete `current_session_id`
  - Delete session data
- [ ] Redirect to Dashboard → new session initialized
- [ ] Optional: Prompt to export before clearing

**Technical Notes:**
- `localStorage.removeItem('nye_haedda_session_{user_id}')`
- After clearing, trigger E1.3 (Session Initialization)

**Story Points:** 2

**Priority:** Must Have

**Reference:** PRD FR-8.2

---

### Story E7.3: Storage Quota Monitoring

**As a** user
**I want** to be warned if storage is running low
**So that** I can export sessions before data is lost

**Acceptance Criteria:**
- [ ] On app load, check localStorage usage:
  - Calculate: `JSON.stringify(localStorage).length`
  - Limit: 5,000,000 bytes (5 MB)
  - Percentage: `(used / limit) * 100`
- [ ] If >80% full → show warning toast:
  - "⚠️ Lagring 80% full. Vurder å eksportere og slette gamle økter."
  - Button: "Eksporter Nå"
- [ ] If >95% full → show error modal:
  - "Lagring nesten full. Eksporter økt og start ny."
  - Button: "Eksporter og Slett"

**Technical Notes:**
- Run check on Dashboard mount (useEffect)
- Research recommendation: Add storage monitoring (Research Report Section 2.5)

**Story Points:** 1

**Priority:** Should Have

**Reference:** Research Report Recommendation 2

---

## Epic 8: Help & Documentation

**Epic Goal:** Provide users with guidance and support.

**Priority:** Should Have (Week 4)

**Dependencies:** None

---

### Story E8.1: In-App Help Documentation

**As a** user
**I want** access to help documentation
**So that** I can learn how to use the simulation

**Acceptance Criteria:**
- [ ] "Hjelp" button in Dashboard sidebar
- [ ] Clicking opens modal or new page with:
  - How to play (step-by-step guide)
  - Tips for negotiation
  - FAQ (common issues)
- [ ] Content in Norwegian
- [ ] Keyboard shortcut: Press `?` to open help

**Technical Notes:**
- Store content in Markdown: `/docs/help.md`
- Render with React Markdown component
- Modal: Shadcn Dialog (scrollable)

**Story Points:** 2

**Priority:** Should Have

**Reference:** PRD FR-9.1

---

### Story E8.2: Tooltips and Onboarding

**As a** first-time user
**I want** tooltips explaining key features
**So that** I understand how to get started

**Acceptance Criteria:**
- [ ] First-time user (no previous session) → show onboarding tour:
  - Tooltip 1: "Dette er ditt budsjett. Hold deg under 700 MNOK."
  - Tooltip 2: "Velg en WBS-oppgave for å starte forhandling."
  - Tooltip 3: "Chat med AI-leverandører for å få pristilbud."
- [ ] Tooltips dismissible (X button)
- [ ] Tour skippable: "Hopp over" button

**Technical Notes:**
- Use library: `react-joyride` or `intro.js`
- Store `onboarding_completed` flag in localStorage
- Tour triggers once per user

**Story Points:** 1

**Priority:** Could Have (Post-MVP)

**Reference:** N/A (enhancement)

---

## Epic 9: Infrastructure & DevOps

**Epic Goal:** Set up technical infrastructure for development and deployment.

**Priority:** Must Have (Week 1)

**Dependencies:** None (blocking other epics)

---

### Story E9.1: Static Data File Preparation

**As a** developer
**I want** WBS and supplier data in JSON format
**So that** I can load them into the application

**Acceptance Criteria:**
- [ ] Extract WBS from proposal PDF → `wbs.json`:
  - 15 items with: `{ code, name, description, baseline_cost, baseline_duration, dependencies, requirements }`
- [ ] Create supplier personas → `suppliers.json`:
  - 5 suppliers with: `{ id, name, company, role, personality, specialties, initial_margin, concession_rate, patience }`
- [ ] Files stored in `/public/data/` (accessible via `/data/wbs.json`)
- [ ] Validate JSON structure (no syntax errors)

**Technical Notes:**
- Manual extraction from PDF (no automation needed for MVP)
- JSON schema validation (TypeScript interfaces)
- Baseline costs should total ~650-680 MNOK (leaving room for negotiation upwards)

**Story Points:** 1 (manual work, not coding)

**Priority:** Must Have (CRITICAL PATH—blocks Week 2 frontend)

**Reference:** PRD Section 8 Data Requirements, Research Report

---

### Story E9.2: Supabase Auth Setup

**As a** developer
**I want** Supabase authentication configured
**So that** users can register and log in

**Acceptance Criteria:**
- [ ] Create Supabase project (free tier)
- [ ] Enable Email auth provider
- [ ] Configure redirect URLs (localhost for dev, Vercel for prod)
- [ ] Store Supabase credentials in `.env`:
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`
- [ ] Test: Register new user → JWT token received

**Technical Notes:**
- No database tables needed (JWT-based auth only)
- Frontend: `@supabase/supabase-js` library
- Security: ANON_KEY is safe to expose (public API key)

**Story Points:** 1

**Priority:** Must Have (blocks E1)

**Reference:** PRD Section 7 Technical Requirements

---

### Story E9.3: FastAPI Backend Deployment

**As a** developer
**I want** FastAPI backend deployed to Vercel
**So that** AI chat proxy works in production

**Acceptance Criteria:**
- [ ] FastAPI app structure:
  - `/api/health`: Health check endpoint
  - `/api/chat`: AI chat proxy (POST)
  - `/api/validate`: Plan validation (POST, optional—can be client-side)
- [ ] Deploy to Vercel (serverless functions)
- [ ] Environment variables:
  - `GEMINI_API_KEY` (Google AI Studio)
  - `SUPABASE_URL`, `SUPABASE_ANON_KEY` (for optional server-side auth check)
- [ ] Test: POST to `/api/chat` → Gemini response received

**Technical Notes:**
- Vercel requires `vercel.json` config for FastAPI routing
- Gemini API: Use `google-generativeai` Python library
- CORS: Allow frontend origin (localhost + Vercel domain)

**Story Points:** 2

**Priority:** Must Have (blocks E4)

**Reference:** PRD Section 7.4 API Specifications

---

### Story E9.4: Frontend Deployment (Vercel)

**As a** developer
**I want** React frontend deployed to Vercel
**So that** users can access the app

**Acceptance Criteria:**
- [ ] Next.js app (or Vite React) deployed to Vercel
- [ ] Environment variables set in Vercel dashboard:
  - `VITE_SUPABASE_URL`
  - `VITE_SUPABASE_ANON_KEY`
  - `VITE_BACKEND_URL` (FastAPI URL)
- [ ] Production URL: `nye-haedda.vercel.app` (or similar)
- [ ] Test: Open URL → Login page loads

**Technical Notes:**
- Auto-deploy on git push (Vercel GitHub integration)
- Build command: `npm run build`
- Output directory: `dist/` (Vite) or `.next/` (Next.js)

**Story Points:** 1

**Priority:** Must Have (Week 4 for production, Day 1 for dev setup)

**Reference:** PRD Section 7 Technical Requirements

---

## Story Point Estimation Guide

**Story Points = Complexity × Effort × Uncertainty**

**1 Point:** Trivial task, 1-2 hours, no uncertainty
- Example: Add environment variable, update text label

**2 Points:** Simple task, 2-4 hours, low uncertainty
- Example: Create basic UI component, add validation check

**3 Points:** Moderate task, 4-8 hours, some uncertainty
- Example: Implement modal with logic, integrate API endpoint

**5 Points:** Complex task, 1-2 days, moderate uncertainty
- Example: Build chat interface, create visualization

**8 Points:** Very complex task, 2-3 days, high uncertainty
- Example: AI prompt engineering, critical path algorithm

**13 Points:** Epic-level task, 3-5 days, very high uncertainty
- Example: Full feature (usually broken down into smaller stories)

**Total Velocity:** Assuming 1 developer, 8 hours/day, 5 days/week = 40 hours/week

**Week 1:** ~20-25 points (setup overhead)
**Week 2-3:** ~25-30 points per week (full velocity)
**Week 4:** ~15-20 points (testing, polish, buffer)

**Total: 89 points ≈ 3.5-4 weeks** ✅

---

## Sprint Planning Recommendation

### Sprint 1 (Week 1): Foundation
**Goal:** Infrastructure, auth, static data ready

**Stories:**
- E9.1: Static data preparation (1 pt)
- E9.2: Supabase auth setup (1 pt)
- E9.3: FastAPI backend deployment (2 pt)
- E9.4: Frontend deployment (1 pt)
- E1.1: User registration (3 pt)
- E1.2: User login (3 pt)
- E1.3: Session initialization (2 pt)

**Total:** 13 points

---

### Sprint 2 (Week 2): Dashboard & WBS
**Goal:** Core UI, WBS display, budget tracking

**Stories:**
- E2.1: Display project constraints (5 pt)
- E2.2: Real-time budget updates (3 pt)
- E2.3: Real-time timeline updates (3 pt)
- E2.4: Quick stats display (2 pt)
- E3.1: Load and display WBS list (3 pt)
- E3.2: WBS item selection (3 pt)
- E3.3: View WBS requirements (2 pt)
- E3.4: WBS status indicators (2 pt)
- E4.1: Chat interface UI (5 pt)

**Total:** 28 points

---

### Sprint 3 (Week 3): AI Negotiation & Plan Management
**Goal:** AI chat working, commitment flow, validation

**Stories:**
- E4.2: Send message to AI (5 pt)
- E4.3: AI offer detection (3 pt)
- **E4.4: AI prompt engineering (8 pt)** ← CRITICAL PATH
- E4.5: Negotiation history (2 pt)
- E4.6: Document sidebar (3 pt)
- E5.1: Commit quote to plan (5 pt)
- E5.2: Renegotiation (3 pt)
- E5.3: Plan history tracking (1 pt)
- E5.4: Dependency validation (2 pt)
- E5.5: Visual feedback (2 pt)

**Total:** 34 points (HIGH—may need to defer E4.6, E5.3 to Week 4)

---

### Sprint 4 (Week 4): Validation, Export, Polish
**Goal:** Plan submission, export, testing, launch

**Stories:**
- E6.1: Submit plan for validation (3 pt)
- E6.2: Validation success modal (2 pt)
- E6.3: Validation error modal (2 pt)
- E6.4: Validation logic (1 pt)
- E7.1: Export session as JSON (2 pt)
- E7.2: Clear session data (2 pt)
- E7.3: Storage quota monitoring (1 pt)
- E8.1: In-app help documentation (2 pt)
- **Testing & Bug Fixes** (5 pt buffer)

**Total:** 20 points

---

## Appendix: Traceability Matrix

| Epic | PRD Section | UX Design Section | Research Report |
|------|-------------|------------------|-----------------|
| E1 | FR-1 (Auth) | 3.1 (Login Page) | N/A |
| E2 | FR-2 (Constraints) | 3.2 (Dashboard) | N/A |
| E3 | FR-3 (WBS) | 3.2 (WBS List), 5.4 (Component) | N/A |
| E4 | FR-4 (Chat) | 3.3 (Chat Page), 5.5 (Message) | Section 1 (AI Prompts) |
| E5 | FR-5 (Commit), FR-6 (Renegotiate) | 3.4 (Modal), 4.2 (Flow) | N/A |
| E6 | FR-7 (Validation) | 3.5 (Error), 3.6 (Success), 4.3 (Flow) | N/A |
| E7 | FR-8 (Export) | N/A | Section 2 (localStorage) |
| E8 | FR-9 (Help) | N/A | N/A |
| E9 | Section 7 (Tech Stack) | 9 (Implementation) | Sections 2-3 |

---

**Document Status:** Complete and ready for sprint planning.

**Next Steps:**
1. Review with development team
2. Refine story point estimates based on team velocity
3. Assign stories to sprints
4. Begin Sprint 1 (Week 1)

**End of Epics and User Stories**
