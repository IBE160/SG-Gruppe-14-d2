# Product Requirements Document (PRD)
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 2.0
**Date:** 2025-12-11
**Status:** Updated for Scaled-Down POC Scope
**Product Owner:** [To be assigned]
**Technical Lead:** [To be assigned]

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-07 | BMAD System | Initial PRD based on Phase 0 brainstorming |
| 1.1 | 2025-12-08 | BMAD System | Added visualization features (Gantt, precedence diagram, history/timeline) |
| 2.0 | 2025-12-11 | BMAD System | **MAJOR SCOPE CHANGE:** Scaled down to 3 negotiable suppliers/WBS packages, 4 AI agent roles (Owner + 3 suppliers), new budget model (310 MNOK available, 390 MNOK locked), inflexible time constraint |

---

## Table of Contents

1. [Product Overview](#1-product-overview)
2. [Goals and Objectives](#2-goals-and-objectives)
3. [Target Users](#3-target-users)
4. [User Stories](#4-user-stories)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Technical Requirements](#7-technical-requirements)
8. [Data Requirements](#8-data-requirements)
9. [API Specifications](#9-api-specifications)
10. [UI/UX Requirements](#10-uiux-requirements)
11. [Success Metrics](#11-success-metrics)
12. [Scope Definition](#12-scope-definition)
13. [Dependencies and Assumptions](#13-dependencies-and-assumptions)
14. [Glossary](#14-glossary)

---

## 1. Product Overview

### 1.1 Product Name
**Nye Hædda Barneskole - Project Management Simulation** (working title)

### 1.2 Product Vision
An AI-powered educational simulation that teaches LOG565 Project Management students realistic negotiation and planning skills by having them act as Project Manager for the "Nye Hædda Barneskole" construction project. Students negotiate with AI-driven supplier personas to gather project estimates, make trade-off decisions under strict constraints, and experience the iterative nature of real-world project planning.

### 1.3 Problem Statement
Traditional project management education suffers from a critical theory-practice gap. Students learn frameworks (WBS, Gantt charts, critical path) through lectures and case studies, but case studies provide pre-determined data, eliminating the most valuable real-world skill: **gathering and validating project data through negotiation with stakeholders who have conflicting interests.**

Students graduate understanding how to create a project plan but not how to obtain the realistic estimates that go into it. They've never practiced:
- Negotiating with a stubborn supplier who gives inflated quotes
- Making trade-offs between cost, time, and quality
- Validating estimates against project requirements
- Experiencing the iterative back-and-forth of real planning

### 1.4 Solution Overview
An interactive, browser-based simulation where students:
1. Act as Project Manager for a real LOG565 case study (Hædda Barneskole construction project)
2. Negotiate with **4 AI agents** in distinct roles:
   - **3 Supplier agents** (each with unique negotiation capabilities: price flexibility, time/cost trade-offs, scope reduction)
   - **1 Owner agent** (Municipality - can adjust budget with strong argumentation, but **CANNOT extend time**)
3. Gather cost and duration estimates for **3 negotiable WBS packages** (3 of 5 on critical path)
4. Work within a challenging budget constraint: **310 MNOK available** for the 3 negotiable packages (390 MNOK already locked for 12 other contracted suppliers)
5. Commit estimates to a project plan through **active user choice** (explicit Accept/Reject for every offer)
6. Navigate **3 main negotiation strategies**:
   - **Reduced quality** → negotiate with supplier for lower cost
   - **Reduced scope** → negotiate with owner to remove features
   - **Shorter time for higher cost** → negotiate with supplier, then owner if budget exceeded
7. Validate the plan against strict constraints (700 MNOK total budget, **inflexible 15-month deadline** ending May 15, 2026)
8. Renegotiate when early decisions prove unsustainable (iterative planning)
9. Export complete session history (all chat logs, all plan changes) as a portfolio artifact

**Session Duration:** 45-60 minutes (single-session, time-efficient)

**Key Scope Change (v2.0):** This is a **Proof of Concept (POC)** focusing on AI agent negotiation mechanics. The remaining 12 WBS packages are pre-contracted and non-negotiable, allowing students to experience realistic negotiation complexity without overwhelming scope.

### 1.5 Key Differentiators

| Feature | Nye Hædda Simulation | Traditional Case Studies | Generic PM Simulations |
|---------|----------------------|--------------------------|------------------------|
| **Data Source** | Student must negotiate to gather estimates | Pre-determined data provided | Static estimates given |
| **AI Behavior** | Dynamic personas (stubborn, flexible, data-driven) | N/A (paper-based) | Scripted, predictable |
| **Learning Focus** | Negotiation, validation, trade-offs | Analysis of completed decisions | Tool mechanics, execution phase |
| **Iteration** | Required (renegotiation when over budget) | Linear (one-pass analysis) | Limited or none |
| **Realism** | Real LOG565 case, authentic documents | Generic or historical cases | Abstract scenarios |
| **Feedback** | Real-time (immediate budget/timeline updates) | Delayed (exam results) | End-of-simulation only |

### 1.6 Success Criteria (POC)
- ✅ **70%+ completion rate** - Students can successfully negotiate all 3 packages (POC scope is more manageable)
- ✅ **60%+ renegotiation rate** - Students experience iterative planning (higher rate due to budget challenge)
- ✅ **40-50 min completion time** - Time-efficient, focused on core negotiation (reduced from 45-60 due to smaller scope)
- ✅ **4.0+/5.0 satisfaction** - Students find AI negotiation realistic and valuable
- ✅ **80%+ Owner interaction rate** - Students engage with Owner AI for budget negotiation
- ✅ **100% time rejection rate** - Owner AI successfully rejects ALL time extension requests (validates inflexible constraint)

---

## 2. Goals and Objectives

### 2.1 Pedagogical Goals

**PG-1: Bridge Theory-Practice Gap**
- Students apply PM frameworks (WBS, critical path, constraint management) to realistic, dynamic scenarios
- Success Metric: 70%+ of students report "this helped me understand planning better than case studies"

**PG-2: Develop Soft Skills**
- Students practice negotiation, persuasion, stakeholder management
- Success Metric: 60%+ of students demonstrate ≥3 distinct negotiation strategies (evidence-based arguments, trade-off proposals, alternative solutions)

**PG-3: Experience Iterative Planning**
- Students learn planning is a cyclical process (plan → validate → renegotiate), not a one-time template exercise
- Success Metric: 40%+ of students renegotiate at least one WBS item

**PG-4: Build Practical Confidence**
- Students gain tangible proof of capability: "I managed a 700 MNOK project within constraints"
- Success Metric: 70%+ of students report increased confidence in PM abilities

### 2.2 Business Goals

**BG-1: Product-Market Fit**
- Validate demand for AI-powered PM simulations in Norwegian business schools
- Success Metric: 30%+ of LOG565 instructors at Norwegian universities adopt within 1 year

**BG-2: User Adoption**
- Achieve critical mass of users for feedback and iteration
- Success Metric: 200+ students complete simulation in first semester

**BG-3: Educational Impact**
- Demonstrate measurable learning outcomes
- Success Metric: Positive correlation (r≥0.3) between simulation completion and exam performance on planning questions

**BG-4: Technical Viability**
- Prove simplified architecture (localStorage + AI) is sustainable
- Success Metric: <2 NOK per session (AI API costs), 99%+ uptime

### 2.3 Non-Goals (Out of Scope for POC)

- ❌ Execution phase simulation (monitoring, controlling, risk management during construction)
- ❌ Multiplayer/collaborative mode
- ❌ Instructor analytics dashboard (students export JSON, instructors review manually)
- ❌ Mobile native app (responsive web app is sufficient)
- ❌ Integration with LMS (Canvas, Blackboard) - students access directly via URL
- ❌ Multiple scenarios (only Hædda Barneskole for POC)
- ❌ **Negotiating all 15 WBS packages** - POC focuses on 3 negotiable packages only
- ❌ **Contract signing** - No formal contract creation, only commitment to plan
- ❌ **Automatic offer acceptance** - All offers require explicit user action (Accept/Reject)

---

## 3. Target Users

### 3.1 Primary User Persona: Sara - The Academic Student

**Demographics:**
- Age: 22-25
- Currently enrolled in LOG565 Project Management 2
- Norwegian business school student (BI, NHH, NTNU)
- Limited real-world PM experience
- High technical comfort with digital tools

**Context of Use:**
- Uses simulation as coursework assignment (required or optional)
- Completes in one sitting (45-60 minutes) between classes or at home
- Submits exported JSON + reflection essay to instructor

**Pain Points:**
- "I know PERT theory but have never negotiated with a real contractor"
- "All case studies give me the numbers - I never learn how to GET those numbers"
- "I don't know if my practice plans are realistic until the exam"

**Success Criteria:**
- Complete realistic project plan within constraints
- Develop concrete negotiation strategies
- Generate portfolio artifact for coursework
- Gain confidence for exams and job interviews

---

### 3.2 Secondary User Persona: Magnus - The Career Switcher

**Demographics:**
- Age: 28-35
- Professional with 3-5 years in different field (engineering, finance)
- Taking LOG565 as part of executive education or part-time master's
- Works full-time, time-constrained

**Context of Use:**
- Uses simulation on weekends or evenings
- Wants focused, efficient practice (under 1 hour)
- May use exported session in job interview discussions

**Pain Points:**
- "I need practical skills fast - I have a full-time job"
- "I've coordinated projects but never been THE project manager"
- "Generic simulations don't feel like real negotiations"

**Success Criteria:**
- Complete in <60 minutes
- Experience realistic negotiation scenarios
- Build portfolio piece for interviews
- Develop PM mental models

---

### 3.3 Stakeholder Persona: Professor Eriksen - The Instructor

**Demographics:**
- Age: 40-60
- Academic or industry professional teaching LOG565
- 15+ years PM experience
- Moderate technical comfort

**Context of Use:**
- Assigns simulation as homework or in-class activity
- Reviews exported JSON files manually (or uses class discussion)
- Uses as complement to traditional case studies

**Pain Points:**
- "Students can't apply theory to messy real-world scenarios"
- "I can't provide personalized feedback to 60 students"
- "Traditional role-plays require too much setup"

**Success Criteria:**
- Students produce discussion-worthy artifacts
- Higher engagement and satisfaction
- Minimal integration friction (no LMS setup needed)
- Students demonstrate improved skills

---

### 3.4 Tertiary User Persona: Ingrid - The Self-Learner

**Demographics:**
- Age: 25-40
- Not enrolled in LOG565 but interested in PM
- Self-taught via books, YouTube, online certs
- Preparing for career change or job interviews

**Context of Use:**
- Discovers simulation via search or social media
- Uses to validate PM knowledge
- May replay to experiment with strategies

**Pain Points:**
- "Have I actually learned anything useful, or just memorized definitions?"
- "No one gives me feedback on practice plans"
- "Free PM resources are too generic"

**Success Criteria:**
- Validate skills in realistic scenario
- Generate concrete examples for interviews
- Build confidence in PM abilities

---

## 4. User Stories

### 4.1 Epic: Authentication & Onboarding

**US-1.1: User Registration**
- **As** Sara (student)
- **I want to** register with my university email
- **So that** my simulation session is associated with my identity and I can submit it for coursework
- **Acceptance Criteria:**
  - User can register with email and password
  - Password must be ≥8 characters
  - Email verification sent via Supabase
  - User cannot access simulation until email is verified
  - Registration errors are clearly displayed (e.g., "Email already exists")

**US-1.2: User Login**
- **As** Magnus (career switcher)
- **I want to** log in with my credentials
- **So that** I can resume my session if I refresh the page or return later
- **Acceptance Criteria:**
  - User can log in with verified email and password
  - JWT token stored in localStorage
  - Token persists across page refreshes
  - User redirected to Dashboard after successful login
  - Invalid credentials show clear error: "Incorrect email or password"

**US-1.3: Session Resume**
- **As** Sara
- **I want to** automatically resume my in-progress session when I log back in
- **So that** I don't lose my progress if I close the browser
- **Acceptance Criteria:**
  - On login, if in-progress session exists in localStorage, load it
  - Dashboard shows current state (budget used, WBS items completed)
  - All chat history preserved
  - User sees confirmation: "Resuming session from [timestamp]"

---

### 4.2 Epic: Project Dashboard & Overview

**US-2.1: View Project Constraints**
- **As** Sara
- **I want to** see the budget limit (700 MNOK) and deadline (May 15, 2026) prominently
- **So that** I constantly remember the constraints I must meet
- **Acceptance Criteria:**
  - Dashboard displays "Budget: X / 700 MNOK" with progress bar
  - Dashboard displays "Deadline: May 15, 2026"
  - Dashboard displays "Projected End Date: [calculated date]"
  - Budget progress bar is color-coded: green (<680), yellow (680-700), red (>700)
  - Timeline is color-coded: green (before May 15), red (after May 15)

**US-2.2: Track Real-Time Progress**
- **As** Magnus
- **I want to** see my current budget and timeline update immediately after committing a quote
- **So that** I know if I'm on track or need to adjust
- **Acceptance Criteria:**
  - After commitment, budget updates within 1 second
  - Projected end date recalculates based on critical path
  - Quick stats show: "X / 15 WBS items completed"
  - Quick stats show: "X total negotiations"
  - No page refresh required (optimistic UI update)

**US-2.3: View WBS Items**
- **As** Sara
- **I want to** browse all WBS items and see their status (negotiable vs locked)
- **So that** I can decide which items to negotiate and understand the overall project
- **Acceptance Criteria:**
  - **15 total WBS items** displayed in hierarchical or flat list
  - **3 negotiable items** clearly highlighted (e.g., blue border, "Kan forhandles" badge)
  - **12 locked items** shown as gray/disabled with "Kontraktfestet" badge
  - Each negotiable item shows: WBS code (e.g., 1.3.1), name (e.g., "Grunnarbeid"), status
  - Status indicators for negotiable items: ⚪ Pending, 🟢 Completed
  - Locked items show: Pre-committed cost, duration, contractor name (read-only)
  - User can click negotiable item to expand details (description, dependencies, baseline estimate)
  - User CANNOT interact with locked items (no "Contact Supplier" button)

---

### 4.3 Epic: Supplier Selection & Chat

**US-3.1: Browse Suppliers and Owner**
- **As** Sara
- **I want to** see which negotiation partners are available (3 suppliers + 1 owner)
- **So that** I can choose the right partner for my negotiation goal
- **Acceptance Criteria:**
  - Clicking "Kontakt Leverandør" on a negotiable WBS item shows **3 relevant suppliers**
  - Supplier cards show: Name, role (e.g., "Totalentreprenør"), specialty, negotiation strength (e.g., "Kan redusere pris")
  - **Owner card** always visible with label: "Eier (Kommunen)" and negotiation power: "Kan øke budsjett (men ikke tid)"
  - User can select: Supplier (for cost/time/quality negotiation) OR Owner (for budget/scope adjustments)
  - User can view persona summary for each partner

**US-3.2: Initiate Chat**
- **As** Magnus
- **I want to** start a conversation with a supplier
- **So that** I can request a quote for a WBS item
- **Acceptance Criteria:**
  - Clicking "Start Chat" opens chat interface
  - Chat header shows: Supplier name, WBS item context
  - Chat window is empty (ready for first message)
  - User can type and send messages immediately

**US-3.3: Negotiate via Chat**
- **As** Sara
- **I want to** have a back-and-forth conversation with the AI supplier
- **So that** I can negotiate cost and duration
- **Acceptance Criteria:**
  - User types message, clicks Send
  - Message appears in chat (right-aligned, blue bubble)
  - AI responds within 3 seconds (95th percentile)
  - AI message appears (left-aligned, gray bubble)
  - All messages logged to localStorage
  - Chat history preserved if user leaves and returns
  - User can reference earlier messages by scrolling

**US-3.4: Reference Project Documents During Chat**
- **As** Sara
- **I want to** quickly access the Requirements Specification while negotiating
- **So that** I can find evidence to support my arguments
- **Acceptance Criteria:**
  - Document sidebar visible while chatting (or accessible via button)
  - Links to: wbs.pdf, krav-spec.pdf, project-description.pdf
  - Documents open in new tab or embedded viewer
  - User can keep document open while typing in chat (split screen)

---

### 4.4 Epic: Owner (Municipality) Negotiation

**US-4.1: Request Budget Increase from Owner**
- **As** Sara
- **I want to** negotiate with the Owner AI to increase the available budget
- **So that** I can accept a supplier's higher-cost offer when necessary
- **Acceptance Criteria:**
  - "Kontakt Eier" button visible when user needs budget approval
  - Chat interface opens with Owner AI (Kommunaldirektør persona)
  - User can request budget increase with argumentation
  - Owner AI evaluates arguments and responds within character:
    - Weak argument → "Vi har allerede stramme rammer. Kan dere finne billigere løsning?"
    - Strong argument → "Jeg forstår. Vi kan godkjenne [X] MNOK ekstra, men dette krever god dokumentasjon."
  - Owner AI has concession_rate (3-5% increases max per round)
  - Budget increase logged to plan_history

**US-4.2: Attempt Time Extension (Always Rejected)**
- **As** Magnus
- **I want to** try requesting a timeline extension from the Owner
- **So that** I can see if there's flexibility (learning that there isn't)
- **Acceptance Criteria:**
  - User can request time extension in Owner chat
  - Owner AI **ALWAYS rejects** with consistent explanation:
    - "Tidsfristen er ufravikelig. Skolen må stå klar til skolestart i august."
    - "Samfunnskostnaden ved forsinkelse er høyere enn økt budsjett."
  - Owner AI suggests alternatives: "Vurder å redusere scope eller akseptere høyere kostnad for raskere levering."
  - System prompt ensures 100% rejection rate for time extension requests

**US-4.3: Negotiate Scope Reduction**
- **As** Sara
- **I want to** propose removing features/scope to reduce cost
- **So that** I can stay within budget by simplifying the project
- **Acceptance Criteria:**
  - User proposes scope reduction (e.g., "Kan vi fjerne [feature]?")
  - Owner AI evaluates impact and responds:
    - If critical feature → "Dette er helt nødvendig for skolen. Ikke mulig."
    - If non-critical → "Vi kan vurdere dette. Hvor mye sparer det?"
  - Scope reduction approved → baseline_cost reduces, logged to plan_history
  - User can then re-negotiate with supplier based on reduced scope

---

### 4.5 Epic: Plan Management

**US-5.1: Accept Quote with Explicit User Action**
- **As** Magnus
- **I want to** explicitly accept or reject a negotiated offer
- **So that** I maintain full control over commitments (no automatic acceptance)
- **Acceptance Criteria:**
  - When AI makes an offer (e.g., "105 MNOK, 2.5 months"), **TWO buttons appear**: "✓ Godta" (Accept) and "✗ Avslå" (Reject)
  - **CRITICAL:** User must actively click one button - NO automatic acceptance ever
  - Clicking "Godta" shows confirmation modal with full terms:
    - WBS item, Supplier/Owner name, Cost, Duration
    - "Dette vil oppdatere prosjektplanen din. Er du sikker?"
  - User has final confirmation step before commitment
  - Clicking "Avslå" returns to chat with message: "Tilbudet ble avslått. Du kan fortsette å forhandle."
  - Plan entry created in localStorage
  - Dashboard updates immediately
  - WBS item status changes to 🟢 Completed
  - Chat shows system message: "✅ Offer accepted and committed to plan"

**US-5.2: View Current Plan**
- **As** Sara
- **I want to** see all my committed WBS items in one place
- **So that** I can review my overall plan and budget
- **Acceptance Criteria:**
  - Dashboard or dedicated tab shows current plan
  - Each committed item shows: WBS code, name, cost, duration, supplier, start date, end date
  - Table is sortable (by cost, date, WBS code)
  - Total cost and projected end date displayed prominently

**US-5.3: Renegotiate Item**
- **As** Sara
- **I want to** go back and renegotiate a committed WBS item
- **So that** I can reduce costs after realizing my plan is over budget
- **Acceptance Criteria:**
  - User clicks "Renegotiate" button on completed WBS item
  - Confirmation modal: "This will uncommit this item. Continue?"
  - User confirms
  - Plan entry removed from current_plan (or marked inactive)
  - Uncommit action logged to plan_history
  - Dashboard recalculates budget and timeline immediately
  - Chat interface reopens with full conversation history preserved
  - User can continue negotiating from where they left off

---

### 4.6 Epic: Validation & Submission

**US-6.1: Continuous Validation Feedback**
- **As** Magnus
- **I want to** see warnings if my plan is approaching limits
- **So that** I can proactively adjust before final submission
- **Acceptance Criteria:**
  - After each commitment, system checks: budget >680 MNOK or timeline >5 days before deadline
  - If close to limits, yellow warning banner: "⚠️ Budget at 95% - limited flexibility remaining"
  - Warnings are non-blocking (user can continue)

**US-6.2: Submit Plan for Validation**
- **As** Sara
- **I want to** submit my completed plan for final validation
- **So that** I can find out if I successfully met all constraints
- **Acceptance Criteria:**
  - "Submit Plan" button enabled when ≥1 WBS item committed
  - Clicking button triggers full validation:
    - **Completeness:** All 3 negotiable WBS items committed? (12 locked items already committed)
    - **Budget:** Total cost (3 negotiable + 12 locked) ≤700 MNOK?
    - **Timeline:** Projected end date ≤May 15, 2026 (inflexible)?
    - **Dependencies:** All dependencies satisfied?
  - Validation runs in <1 second

**US-6.3: Receive Clear Error Feedback**
- **As** Sara
- **I want to** see exactly what's wrong if my plan fails validation
- **So that** I know how to fix it
- **Acceptance Criteria:**
  - Error modal shows all validation failures
  - Budget error: "❌ Budget exceeded by 50 MNOK. Total: 750 MNOK (Limit: 700)"
  - Timeline error: "❌ Project delayed until May 20, 2026. Deadline: May 15, 2026"
  - Suggestions provided: "Renegotiate these high-cost items: 2.1 (250 MNOK), 3.4 (180 MNOK)"
  - User can close modal and return to planning

**US-6.4: Celebrate Success**
- **As** Magnus
- **I want to** see a clear success message when my plan passes validation
- **So that** I feel a sense of accomplishment
- **Acceptance Criteria:**
  - Success modal displays: "🎉 Plan Approved!"
  - Final stats shown: Total cost, completion date, time spent, negotiation count, renegotiation count
  - "Export Session" button available
  - "Start New Game" button available
  - Session status updated to "completed" in localStorage

---

### 4.7 Epic: Export & Persistence

**US-7.1: Export Complete Session**
- **As** Sara
- **I want to** download my complete session history as a file
- **So that** I can submit it for coursework or save it for my portfolio
- **Acceptance Criteria:**
  - "Export Session" button available on success screen
  - Clicking downloads JSON file: `nye-haedda-session-{user_id}-{game_id}.json`
  - JSON includes:
    - User metadata (user_id, game_id, timestamps)
    - Complete chat_logs (every message)
    - Complete plan_history (every commit/uncommit)
    - Final current_plan
    - Metrics (budget, timeline, negotiation counts)
    - Validation result
  - File is valid JSON (parseable)
  - File size typically 200-500 KB

**US-7.2: Save Progress Automatically**
- **As** Magnus
- **I want to** have my session auto-saved after every action
- **So that** I don't lose progress if my browser crashes
- **Acceptance Criteria:**
  - Every user action (send message, commit quote, uncommit) saves to localStorage immediately
  - No explicit "Save" button needed
  - If browser crashes and user reopens, session is intact
  - localStorage key: `nye-haedda-session-{user_id}`

---

### 4.8 Epic: Help & Support

**US-8.1: Access Help Documentation**
- **As** Ingrid (self-learner)
- **I want to** access help documentation if I'm confused
- **So that** I can understand how the simulation works
- **Acceptance Criteria:**
  - "Help" button visible on Dashboard
  - Clicking opens modal with:
    - Simulation overview (what is this?)
    - How to negotiate (tips)
    - How to commit quotes
    - How to validate plan
    - FAQ section
  - Help modal closeable without losing state

**US-8.2: Report Issues**
- **As** Sara
- **I want to** report a bug or incorrect AI response
- **So that** the developers can improve the simulation
- **Acceptance Criteria:**
  - "Report Issue" link in footer or Help modal
  - Opens simple form or links to GitHub Issues
  - User can describe problem and attach session ID

---

## 5. Functional Requirements

### 5.1 Authentication & User Management

**FR-1.1: User Registration**
- **Priority:** Must Have
- **Description:** Users can create an account using email and password via Supabase Auth
- **Detailed Requirements:**
  - Email must be valid format (regex validation)
  - Password must be ≥8 characters, contain at least 1 number
  - Email verification required before first login
  - Duplicate email shows error: "Email already registered"
  - Registration form has "Already have an account? Login" link
- **Dependencies:** Supabase Auth SDK
- **Acceptance Test:**
  - User enters valid email + password → account created, verification email sent
  - User enters duplicate email → error displayed
  - User enters weak password → error: "Password must be at least 8 characters"

---

**FR-1.2: User Login**
- **Priority:** Must Have
- **Description:** Users can log in with verified email and password
- **Detailed Requirements:**
  - JWT token generated by Supabase on successful login
  - Token stored in localStorage['auth-token']
  - Token persists across browser sessions (until user logs out or token expires)
  - Invalid credentials → error: "Incorrect email or password"
  - Unverified email → error: "Please verify your email first"
- **Acceptance Test:**
  - User enters correct credentials → logged in, redirected to Dashboard
  - User enters wrong password → error displayed, not logged in

---

**FR-1.3: User Logout**
- **Priority:** Must Have
- **Description:** Users can log out, clearing session data
- **Detailed Requirements:**
  - Logout button in header (user menu dropdown)
  - Clicking logout:
    - Clears auth token from localStorage
    - (Optional) Clears session data (prompt user to export first)
    - Redirects to login page
- **Acceptance Test:**
  - User clicks Logout → redirected to login, cannot access Dashboard without re-login

---

### 5.2 Session Management

**FR-2.1: Create New Game Session**
- **Priority:** Must Have
- **Description:** User can start a new simulation session
- **Detailed Requirements:**
  - "Start New Game" button on Dashboard (if no active session)
  - Clicking creates new session object in localStorage:
    ```javascript
    {
      user_id: from JWT,
      game_id: UUID,
      created_at: ISO timestamp,
      status: "in_progress",
      wbs_items: loaded from /data/wbs.json,
      suppliers: loaded from /data/suppliers.json,
      chat_logs: [],
      plan_history: [],
      current_plan: {},
      metrics: {total_budget_used: 0, projected_end_date: null, ...}
    }
    ```
  - If active session exists, prompt: "You have an in-progress session. Resume or start new?"
  - Starting new session archives old session (optional: move to `nye-haedda-archive-{game_id}`)
- **Acceptance Test:**
  - User clicks "Start New Game" → session created in localStorage, Dashboard loads with 0/700 MNOK budget

---

**FR-2.2: Resume Session**
- **Priority:** Must Have
- **Description:** On login, user automatically resumes in-progress session
- **Detailed Requirements:**
  - On Dashboard load, check localStorage for `nye-haedda-session-{user_id}`
  - If exists and status="in_progress", load session
  - Dashboard displays current state (budget used, completed WBS items, chat history)
  - User sees confirmation message: "Resuming session from [created_at]"
- **Acceptance Test:**
  - User logs in with in-progress session → Dashboard shows current progress
  - User logs in with no session → "Start New Game" screen

---

**FR-2.3: Auto-Save Session**
- **Priority:** Must Have
- **Description:** Session automatically saves to localStorage after every user action
- **Detailed Requirements:**
  - After every action (send message, commit quote, uncommit), call `saveSession()`
  - `saveSession()` serializes session object to JSON and writes to localStorage
  - No user-visible "Save" button (automatic)
  - Session persists across page refreshes
- **Acceptance Test:**
  - User sends chat message, refreshes page → message still visible
  - User commits quote, closes browser, reopens → commitment still in plan

---

### 5.3 Dashboard & Information Display

**FR-3.1: Display Project Constraints**
- **Priority:** Must Have
- **Description:** Dashboard prominently displays budget limit and deadline
- **Detailed Requirements:**
  - Constraint panel shows:
    - "Budget: X / 700 MNOK" with horizontal progress bar
    - "Deadline: May 15, 2026"
    - "Projected End Date: [calculated or TBD]"
  - Progress bar color:
    - Green: 0-680 MNOK
    - Yellow: 680-700 MNOK
    - Red: >700 MNOK
  - Projected end date color:
    - Green: before May 15, 2026
    - Red: after May 15, 2026
- **Acceptance Test:**
  - User with 500 MNOK committed sees green progress bar at 71%
  - User with 750 MNOK committed sees red progress bar at 107%

---

**FR-3.2: Display WBS Items (3 Negotiable + 12 Locked)**
- **Priority:** Must Have
- **Description:** Dashboard displays all 15 WBS items with clear distinction between negotiable and locked
- **Detailed Requirements:**
  - WBS items loaded from `/data/wbs.json` (static file)
  - **15 total items:** 3 marked `negotiable: true`, 12 marked `negotiable: false, status: "contracted"`
  - Display format: List or tree view (hierarchical if parent_id exists)
  - **3 Negotiable items styling:**
    - Blue border or highlight
    - Badge: "Kan forhandles" or blue dot indicator
    - WBS code (e.g., "1.3.1"), Name (e.g., "Grunnarbeid")
    - Status icon: ⚪ Pending (not in current_plan) or 🟢 Completed (in current_plan)
    - "Kontakt Leverandør" button (if pending) or "Reforhandle" button (if completed)
  - **12 Locked items styling:**
    - Gray background, lower opacity (60%)
    - Badge: "Kontraktfestet" or lock icon 🔒
    - Show pre-committed values: Cost, Duration, Contractor name
    - **NOT clickable** - no interaction, no expansion
  - Clicking negotiable item expands details:
    - Description
    - Dependencies
    - Baseline estimate (reference only)
    - If completed: Committed cost, duration, supplier, dates
- **Acceptance Test:**
  - User sees 15 WBS items total: 3 highlighted as negotiable (blue), 12 grayed out as locked
  - 3 negotiable items show ⚪ Pending initially
  - 12 locked items show pre-committed cost/duration/contractor (read-only)
  - After committing negotiable 1.3.1, it shows 🟢 Completed with values
  - User cannot click or interact with locked items

---

**FR-3.3: Real-Time Metrics Update**
- **Priority:** Must Have
- **Description:** Dashboard metrics update immediately after commitment/uncommitment
- **Detailed Requirements:**
  - After commitment:
    - Recalculate `total_budget_used = SUM(current_plan.*.cost)`
    - Recalculate `projected_end_date = calculateCriticalPath(current_plan, wbs_items)`
    - Update Quick Stats: "X / 15 WBS items completed"
  - Update happens client-side (no API call needed)
  - UI updates within 1 second (optimistic update)
- **Acceptance Test:**
  - User commits 105 MNOK quote → budget immediately shows 105/700 MNOK
  - User uncommits quote → budget immediately recalculates

---

### 5.4 Supplier and Owner Interaction

**FR-4.1: Display Negotiation Partner Directory (3 Suppliers + 1 Owner)**
- **Priority:** Must Have
- **Description:** Users can browse available negotiation partners: 3 suppliers + 1 owner
- **Detailed Requirements:**
  - **Suppliers** loaded from `/data/suppliers.json` (static file) - **3 total**
  - **Owner** loaded from `/data/owner.json` or embedded in suppliers.json with `type: "owner"`
  - When user clicks "Kontakt Leverandør" on negotiable WBS item X, show:
    - **3 Supplier cards** where `specialty` includes X
    - **1 Owner card** always available (for budget/scope negotiation)
  - **Supplier card shows:**
    - Name (e.g., "Bjørn Eriksen")
    - Role (e.g., "Totalentreprenør for Grunnarbeid")
    - Persona summary (e.g., "Kan forhandle pris og kvalitet")
    - Negotiation capability badge: "Pris" / "Tid/Kostnad" / "Scope"
    - "Start Chat" button
  - **Owner card shows:**
    - Name: "Kommunaldirektør [Name]" (e.g., "Anne-Lise Berg")
    - Role: "Eier (Kommunen)"
    - Persona summary: "Kan øke budsjett, men ikke tid"
    - Warning badge: "⏰ Tiden kan IKKE forlenges"
    - "Kontakt Eier" button
- **Acceptance Test:**
  - User clicks "Kontakt Leverandør" for WBS 1.3.1 → sees 3 supplier cards + 1 owner card
  - Owner card always shows time constraint warning

---

**FR-4.2: Chat Interface**
- **Priority:** Must Have
- **Description:** Users can send messages to AI suppliers and receive responses
- **Detailed Requirements:**
  - Chat window components:
    - Header: Supplier name, role, WBS item context
    - Message list: Scrollable, auto-scroll to latest
    - Input: Multi-line text area + Send button
  - Message display:
    - User messages: Right-aligned, blue bubble
    - AI messages: Left-aligned, gray bubble
    - System messages: Center-aligned, small gray text
  - Message flow:
    1. User types message, clicks Send
    2. Message immediately appears in chat (optimistic update)
    3. Message logged to `session.chat_logs`
    4. POST to `/api/chat/message` with context
    5. AI response received (typically 1-3 seconds)
    6. AI message logged to `session.chat_logs`
    7. AI message appears in chat
  - Typing indicator: "Bjørn is reviewing the specifications..." while waiting for AI
  - All messages persisted in localStorage
- **Acceptance Test:**
  - User sends "I need a quote for Grunnarbeid" → message appears in chat
  - AI responds within 3 seconds → response appears in chat
  - User refreshes page → full chat history still visible

---

**FR-4.3: AI Response Generation**
- **Priority:** Must Have
- **Description:** Backend generates AI responses based on supplier persona and negotiation state
- **Detailed Requirements:**
  - Backend receives:
    - Supplier data (id, system_prompt, hidden_params)
    - WBS item data (id, name, baseline_cost, baseline_duration)
    - Chat history (all previous messages for this WBS + supplier)
    - User message
  - Backend constructs prompt:
    - Supplier system_prompt (persona)
    - WBS context
    - Relevant requirements (from static requirements.json or embedded in prompt)
    - Conversation history
    - Negotiation rules (hidden minimum cost/duration from supplier.hidden_params)
  - Backend calls Gemini API (via PydanticAI)
  - Backend extracts structured offer if present (regex or structured output):
    - Example: "I can do 105 MNOK for 2.5 months" → {cost: 105, duration: 2.5}
  - Backend returns:
    ```json
    {
      "response": "Based on current market rates, I estimate...",
      "offer": {cost: 120, duration: 3} or null,
      "timestamp": "ISO timestamp"
    }
    ```
- **Acceptance Test:**
  - User sends message → AI responds with persona-appropriate answer
  - AI references WBS baseline: "The baseline estimate was 100 MNOK..."
  - AI respects hidden minimums: Will not accept <88 MNOK if min_cost_multiplier=0.88 and baseline=100

---

**FR-4.4: Offer Extraction**
- **Priority:** Must Have
- **Description:** System detects when AI makes a structured offer
- **Detailed Requirements:**
  - AI response analyzed for patterns:
    - Cost: "[number] MNOK" or "[number] million NOK"
    - Duration: "[number] months" or "[number] mnd"
  - Extracted values stored in chat_log entry: `extracted_offer: {cost, duration}`
  - If offer detected, "Accept Offer" button appears below AI message
  - Button shows extracted values: "Accept: 105 MNOK, 2.5 months"
- **Acceptance Test:**
  - AI says "I can do 105 MNOK for 2.5 months" → "Accept Offer" button appears
  - User clicks button → commitment flow triggers

---

**FR-4.5: Owner AI Agent (Municipality) - Budget and Scope Negotiation**
- **Priority:** Must Have
- **Description:** Owner AI agent represents municipality, can adjust budget but NEVER time
- **Detailed Requirements:**
  - Owner persona: Kommunaldirektør (e.g., "Anne-Lise Berg")
  - Owner has distinct system prompt (stored in `/backend/prompts/owner.md`)
  - **Negotiation Powers:**
    - ✅ **Can approve budget increases** (with strong user argumentation)
    - ✅ **Can approve scope reductions** (removing non-critical features)
    - ❌ **CANNOT extend time** under ANY circumstances (system prompt enforces this)
  - **Budget Negotiation Flow:**
    1. User requests budget increase: "Vi trenger 15 MNOK ekstra for å sikre kvalitet på grunnarbeidet"
    2. Owner evaluates argumentation quality (via AI reasoning)
    3. Weak argument → Rejection: "Vi har allerede stramme rammer. Kan dere finne billigere løsning?"
    4. Strong argument → Conditional approval: "Jeg forstår. Vi kan godkjenne 10 MNOK ekstra, men dette krever god dokumentasjon i prosjektrapporten."
    5. Budget increase: `available_budget += approved_amount`
    6. Logged to plan_history: `{action: "budget_increase", amount: 10, approved_by: "owner"}`
  - **Time Negotiation Flow (Always Rejected):**
    1. User requests time extension: "Kan vi få 2 ekstra måneder?"
    2. Owner **ALWAYS responds** with inflexible rejection:
       - "Tidsfristen er ufravikelig. Skolen må stå klar til skolestart i august."
       - "Samfunnskostnaden ved forsinkelse er høyere enn økt budsjett."
    3. Owner suggests alternatives: "Vurder å redusere scope eller akseptere høyere kostnad for raskere levering."
    4. **CRITICAL:** System prompt must enforce 100% rejection rate for time extension requests
  - **Scope Reduction Flow:**
    1. User proposes scope reduction: "Kan vi fjerne utendørs lekeplass for å spare kostnader?"
    2. Owner evaluates criticality (via system prompt with predefined critical features list)
    3. If critical → Rejection: "Dette er helt nødvendig for skolen. Ikke mulig."
    4. If non-critical → Approval: "Vi kan vurdere dette. Hvor mye sparer det? Send meg et oppdatert tilbud."
    5. Scope reduction approved → `wbs_item.baseline_cost *= reduction_factor`
- **Hidden Parameters (Owner):**
  ```json
  {
    "max_budget_increase_per_round": 0.03-0.05,  // 3-5% of available budget
    "total_max_budget_increase": 0.15,  // Can approve up to 15% total increase
    "time_extension_allowed": false,  // ALWAYS false
    "patience": 5,  // Will engage for 5+ rounds of negotiation
    "argumentation_quality_threshold": 0.7  // Requires strong arguments
  }
  ```
- **Acceptance Test:**
  - User requests budget increase with good argument → Owner approves 3-5% increase
  - User requests budget increase with weak argument → Owner rejects, suggests alternatives
  - User requests time extension → Owner ALWAYS rejects with standard explanation
  - Owner chat includes personality: professional, budget-conscious, firm on deadlines

---

### 5.5 Plan Management

**FR-5.1: Commit Quote to Plan**
- **Priority:** Must Have
- **Description:** User can accept an AI offer and commit it to the project plan
- **Detailed Requirements:**
  - User clicks "Accept Offer" button
  - Confirmation modal shows:
    - WBS item: "1.3.1 - Grunnarbeid"
    - Supplier: "Bjørn Eriksen"
    - Cost: 105 MNOK
    - Duration: 2.5 months
    - "This will update your project plan. Confirm?"
  - User clicks Confirm
  - System calculates start_date based on dependencies:
    - If no dependencies: start_date = project start (e.g., Jan 15, 2025)
    - If dependencies exist: start_date = MAX(dependency end dates)
  - System calculates end_date: start_date + duration
  - System creates plan_history entry:
    ```javascript
    {
      timestamp: now(),
      action: "commit",
      wbs_item: "1.3.1",
      supplier: "bjorn-eriksen",
      cost: 105,
      duration: 2.5,
      start_date: "2025-01-15",
      end_date: "2025-04-01"
    }
    ```
  - System updates current_plan:
    ```javascript
    current_plan["1.3.1"] = {
      supplier: "bjorn-eriksen",
      cost: 105,
      duration: 2.5,
      start_date: "2025-01-15",
      end_date: "2025-04-01",
      committed_at: now()
    }
    ```
  - System recalculates metrics:
    - `total_budget_used = SUM(current_plan.*.cost)`
    - `projected_end_date = calculateCriticalPath(current_plan, wbs_items)`
  - System saves session to localStorage
  - Dashboard updates (budget, timeline, WBS status)
  - Chat shows system message: "✅ Offer accepted and committed to plan"
- **Acceptance Test:**
  - User accepts offer → plan updates, dashboard shows new budget, WBS item marked complete

---

**FR-5.2: Uncommit and Renegotiate**
- **Priority:** Must Have
- **Description:** User can uncommit a plan entry and renegotiate
- **Detailed Requirements:**
  - User clicks "Renegotiate" button on completed WBS item
  - Confirmation modal: "This will remove this item from your plan and recalculate your budget/timeline. Continue?"
  - User clicks Confirm
  - System creates plan_history entry:
    ```javascript
    {
      timestamp: now(),
      action: "uncommit",
      wbs_item: "1.3.1"
    }
    ```
  - System removes item from current_plan: `delete current_plan["1.3.1"]`
  - System increments `metrics.renegotiation_count++`
  - System recalculates metrics
  - System saves session
  - Dashboard updates
  - Chat interface reopens with full history preserved
  - User can continue negotiation
- **Acceptance Test:**
  - User uncommits 1.3.1 (105 MNOK) → budget decreases by 105 MNOK
  - Chat history still visible with all previous messages

---

### 5.6 Validation & Submission

**FR-6.1: Real-Time Validation (Soft Warnings)**
- **Priority:** Must Have
- **Description:** System shows warnings when plan approaches limits
- **Detailed Requirements:**
  - After each commitment, check:
    - If total_budget_used >680 MNOK (>97%): Show yellow banner: "⚠️ Budget at 97% capacity"
    - If projected_end_date <5 days before May 15, 2026: Show yellow banner: "⚠️ Timeline has minimal buffer"
  - Warnings are non-blocking (user can continue)
  - Banner dismissible but reappears on next commitment if still over threshold
- **Acceptance Test:**
  - User commits quote bringing budget to 690 MNOK → yellow warning appears

---

**FR-6.2: Plan Validation (Hard Errors)**
- **Priority:** Must Have
- **Description:** System validates plan against all constraints on submission
- **Detailed Requirements:**
  - User clicks "Submit Plan" button
  - System runs validation checks:
    1. **Completeness:** `Object.keys(current_plan).length === wbs_items.length` (all 15 items committed: 3 negotiable by user + 12 pre-committed locked)
    2. **Budget:** `total_budget_used <= 700` (sum of 3 negotiable + 12 locked)
    3. **Timeline:** `projected_end_date <= new Date('2026-05-15')`
    4. **Dependencies:** For each committed item, all dependencies are committed and end before this item starts
  - If any check fails, collect errors array
  - Return validation result:
    ```javascript
    {
      valid: false,
      errors: [
        {type: "budget", message: "Budget exceeded by 50 MNOK", current: 750, limit: 700},
        {type: "completeness", message: "Only 14/15 WBS items committed"}
      ],
      warnings: []
    }
    ```
- **Acceptance Test:**
  - User submits plan with 750 MNOK total → validation fails with budget error
  - User submits plan with all items <700 MNOK, on time → validation passes

---

**FR-6.3: Validation Error Display**
- **Priority:** Must Have
- **Description:** User sees clear, actionable error messages on failed validation
- **Detailed Requirements:**
  - Error modal displays:
    - Title: "❌ Plan Validation Failed"
    - Error list:
      - Budget error: "Budget exceeded by 50 MNOK. Total: 750 MNOK (Limit: 700 MNOK)"
      - Timeline error: "Project delayed until May 20, 2026. Deadline: May 15, 2026."
      - Completeness: "Missing WBS items: 3.2, 4.1"
    - Suggestions section: "Consider renegotiating these high-cost items: 2.1 (250 MNOK), 3.4 (180 MNOK)"
    - "Back to Planning" button (closes modal)
  - Errors should be specific and actionable (not generic "Plan failed")
- **Acceptance Test:**
  - User submits over-budget plan → sees exact amount over and suggestions

---

**FR-6.4: Success State**
- **Priority:** Must Have
- **Description:** User sees congratulations screen when plan passes validation
- **Detailed Requirements:**
  - Success modal displays:
    - Title: "🎉 Plan Approved!"
    - Final stats:
      - "Total Cost: 698 MNOK (within 700 MNOK budget)"
      - "Completion Date: May 10, 2026 (5 days before deadline)"
      - "Time Spent: 47 minutes"
      - "Total Negotiations: 23"
      - "Renegotiations: 3"
    - Buttons:
      - "Export Session" (primary)
      - "Start New Game" (secondary)
      - "Take Survey" (optional feedback)
  - Session status updated to "completed" in localStorage
  - `session.completed_at = now()`
- **Acceptance Test:**
  - User submits valid plan → success modal appears with accurate stats

---

### 5.7 Export & Data Management

**FR-7.1: Export Session as JSON**
- **Priority:** Must Have
- **Description:** User can download complete session history as JSON file
- **Detailed Requirements:**
  - "Export Session" button available on success screen (and optionally in dashboard menu)
  - Clicking button generates JSON export:
    ```javascript
    {
      // Metadata
      export_version: "1.0",
      exported_at: ISO timestamp,

      // Game info
      user_id, game_id, created_at, completed_at, status,

      // Complete logs
      chat_logs: [/* every message */],
      plan_history: [/* every commit/uncommit */],

      // Final state
      final_plan: current_plan,
      metrics: {...},

      // Context
      wbs_items: [/* reference data */],

      // Validation
      validation: {valid: true, errors: []}
    }
    ```
  - File downloaded with name: `nye-haedda-session-{user_id}-{game_id}.json`
  - File size typically 200-500 KB
  - JSON is valid and human-readable (pretty-printed with 2-space indent)
- **Acceptance Test:**
  - User clicks Export → JSON file downloads
  - Opening file in text editor shows valid JSON with all session data

---

**FR-7.2: localStorage Management**
- **Priority:** Must Have
- **Description:** Session data is stored efficiently in browser localStorage
- **Detailed Requirements:**
  - localStorage key: `nye-haedda-session-{user_id}`
  - Data structure: JSON string (serialized session object)
  - Auto-save after every action
  - Check localStorage quota before saving (catch QuotaExceededError)
  - If quota exceeded, prompt user: "Storage full. Please export and clear old sessions."
  - On logout, optionally prompt: "Export your session before logging out?"
- **Acceptance Test:**
  - User completes 100+ message negotiation → session still saves (typical session <500 KB)

---

### 5.8 Static Data & Documents

**FR-8.1: WBS Data Loading (3 Negotiable + 12 Locked)**
- **Priority:** Must Have
- **Description:** WBS items loaded from static JSON file with negotiable/locked distinction
- **Detailed Requirements:**
  - File location: `/public/data/wbs.json`
  - File structure:
    ```json
    [
      {
        "id": "1.3.1",
        "name": "Grunnarbeid",
        "description": "Site preparation and excavation...",
        "baseline_cost": 105,
        "baseline_duration": 60,
        "dependencies": ["1.2"],
        "negotiable": true,
        "on_critical_path": true,
        "suggested_suppliers": ["bjorn-eriksen", "supplier-2", "supplier-3"]
      },
      {
        "id": "1.2",
        "name": "Arkitekt",
        "description": "Architectural design...",
        "baseline_cost": 25,
        "baseline_duration": 20,
        "dependencies": [],
        "negotiable": false,
        "status": "contracted",
        "contractor": "Locked Contractor AS",
        "committed_cost": 25,
        "committed_duration": 20
      }
      // ... 15 total items (3 negotiable, 12 locked)
    ]
    ```
  - **3 negotiable items:** `negotiable: true`, on critical path
  - **12 locked items:** `negotiable: false, status: "contracted"`, pre-committed values
  - Loaded on session initialization
  - Stored in `session.wbs_items`
- **Acceptance Test:**
  - Dashboard displays all 15 WBS items from wbs.json
  - 3 items are interactive, 12 are read-only with pre-committed values

---

**FR-8.2: Supplier and Owner Data Loading (3 Suppliers + 1 Owner)**
- **Priority:** Must Have
- **Description:** Supplier and Owner personas loaded from static JSON files
- **Detailed Requirements:**
  - File location: `/public/data/suppliers.json` and `/public/data/owner.json` (or combined)
  - **File structure (suppliers.json):**
    ```json
    [
      {
        "id": "bjorn-eriksen",
        "name": "Bjørn Eriksen",
        "type": "supplier",
        "role": "Totalentreprenør for Grunnarbeid",
        "specialty": ["1.3.1"],
        "persona_summary": "Kan forhandle pris og kvalitet",
        "negotiation_capability": "price_quality",
        "system_prompt": "You are Bjørn Eriksen, a general contractor...",
        "hidden_params": {
          "initial_margin": 1.20,
          "min_cost_multiplier": 0.88,
          "concession_rate": 0.05,
          "patience": 3
        }
      },
      {
        "id": "supplier-2",
        "name": "Kari Andersen",
        "type": "supplier",
        "role": "Entreprenør for Fundamentering",
        "specialty": ["1.3.2"],
        "negotiation_capability": "time_cost_tradeoff",
        "hidden_params": {
          "initial_margin": 1.15,
          "time_reduction_cost_multiplier": 1.30
        }
      },
      {
        "id": "supplier-3",
        "name": "Per Johansen",
        "type": "supplier",
        "role": "Entreprenør for Råbygg",
        "specialty": ["1.4.1"],
        "negotiation_capability": "scope_reduction"
      }
      // 3 suppliers total
    ]
    ```
  - **File structure (owner.json):**
    ```json
    {
      "id": "owner-municipality",
      "name": "Anne-Lise Berg",
      "type": "owner",
      "role": "Kommunaldirektør",
      "persona_summary": "Kan øke budsjett, men ikke tid",
      "system_prompt": "You are Anne-Lise Berg, representing the municipality...",
      "hidden_params": {
        "max_budget_increase_per_round": 0.05,
        "total_max_budget_increase": 0.15,
        "time_extension_allowed": false,
        "patience": 5
      }
    }
    ```
  - Loaded on session initialization
  - Stored in `session.suppliers` and `session.owner`
  - `system_prompt` and `hidden_params` sent to backend API (not displayed to user)
- **Acceptance Test:**
  - Supplier directory shows 3 suppliers + 1 owner
  - Owner card shows time constraint warning

---

**FR-8.3: Document Access**
- **Priority:** Must Have
- **Description:** Users can access project documents (WBS, requirements, project description)
- **Detailed Requirements:**
  - Files location: `/public/docs/`
    - `wbs.pdf`
    - `krav-spec.pdf`
    - `project-description.pdf`
  - Document sidebar or "Resources" tab
  - Clicking document link opens in new tab or embedded PDF viewer
  - User can access documents while chat interface is open (multi-window or split screen)
- **Acceptance Test:**
  - User clicks "Requirements Specification" → krav-spec.pdf opens

---

### 5.9 Visualization & Analysis

**FR-9.1: Gantt Chart View**
- **Priority:** Must Have
- **Description:** Display project timeline as an interactive Gantt chart showing task durations, dependencies, and critical path
- **Detailed Requirements:**
  - Accessible via "Gantt-diagram" tab in main navigation
  - Timeline header: Shows months from project start (Jan 2025) to deadline (May 2026)
  - Task bars display:
    - **Completed tasks:** Green bars with 100% fill
    - **In-progress tasks:** Yellow/orange bars with progress percentage (e.g., "45%")
    - **Planned tasks:** Gray outlined bars
    - **Critical path tasks:** Red outline/border (3px)
  - Each task bar shows:
    - WBS ID and name on left
    - Duration in days
    - Start and end dates on hover
  - Dependency arrows:
    - Gray arrows for normal dependencies
    - Red dashed arrows for critical path
  - "Today" marker: Blue vertical dashed line showing current date
  - Milestone markers: Diamond shapes (e.g., for Inspeksjon)
  - Interactive controls:
    - View modes: Month / Week / Day
    - Zoom slider (50% to 200%)
    - Filters: Toggle critical path, dependencies, milestones
  - Legend showing color coding
  - Export button: "Eksporter Gantt (PNG)"
  - **Real-time updates:** Chart re-renders when plan changes (new commitments, renegotiations)
- **Data Source:**
  - `session.current_plan` (committed WBS items with start_date, end_date, duration, cost)
  - Critical path calculation: Topological sort + longest path algorithm
- **Acceptance Test:**
  - User commits 1.4.1 Råbygg (90 days, starts April 15) → Gantt shows yellow bar from April 15 to July 14
  - User clicks Month view → timeline shows monthly grid
  - Critical path tasks have red outline

---

**FR-9.2: Precedence Diagram (AON Network)**
- **Priority:** Must Have
- **Description:** Display Activity-on-Node (AON) network diagram showing task dependencies, critical path, and slack times
- **Detailed Requirements:**
  - Accessible via "Presedensdiagram" tab in main navigation
  - Network nodes (rectangular boxes) for each WBS task:
    - **Node content:**
      - WBS ID and name (top)
      - Duration in days
      - Cost in MNOK
      - Status: Fullført ✓ / Pågår ⏳ / Planlagt
      - Slack time (bottom, e.g., "Slack: 0 dager" for critical path)
    - **Node styling:**
      - Green fill + green border: Completed
      - Yellow fill + orange border: In-progress
      - White fill + gray border: Planned
      - Red thick border (4px): Critical path nodes
  - Arrows showing dependencies:
    - Gray arrows (2px): Normal dependencies
    - Red thick arrows (3px): Critical path
  - START node (circle) and END node (after final task)
  - Layout modes:
    - Left→Right (default)
    - Top→Bottom
    - Hierarchical
  - Interactive controls:
    - Filter: "Kun kritisk sti" (show only critical path nodes)
    - Toggle: Show earliest/latest start times
    - Toggle: Show slack times (checked by default)
  - Info panels at bottom:
    - **Critical Path Summary (red):** Number of tasks, total duration, end date
    - **Parallel Paths (blue):** Non-critical tasks with slack times
    - **Progress Stats (green):** X/15 completed, Y in-progress, Z remaining
    - **Network Statistics (yellow):** Total nodes, dependencies, criticality %
  - Export button: "Eksporter Diagram (PNG)"
  - **Real-time updates:** Network recalculates when plan changes
- **Algorithms:**
  - Critical path: Topological sort + longest path (same as Gantt)
  - Slack calculation: `slack = latest_finish - earliest_finish`
  - Auto-layout: Dagre or force-directed layout
- **Acceptance Test:**
  - User commits all critical path tasks → red border appears on nodes
  - Parallel task 1.5.1 Elektrisk shows "Slack: 15 dager"
  - Filter "Kun kritisk sti" → only 8 critical nodes visible

---

**FR-9.3: History/Timeline View**
- **Priority:** Should Have
- **Description:** Version control system showing all plan changes over time with before/after comparison
- **Detailed Requirements:**
  - Accessible via "🕒 Historikk" button in top-right navigation (all views)
  - Opens side panel overlaying current view
  - **Left sidebar (400px):**
    - Timeline list of all events (commits, uncommits, negotiations)
    - Each event shows:
      - Version number badge (1, 2, 3...)
      - Event type icon (💬 negotiation, ✓ commit, 🔄 uncommit, ⚠️ validation)
      - Title: "Forhandling med [Supplier]" or "Fullført: [WBS ID]"
      - Key changes: Old value → New value
      - Timestamp: Relative (e.g., "30 min siden") or absolute
    - Filter buttons: All / Negotiations / Plan changes
    - Current event highlighted in blue
    - Vertical timeline line connecting events
  - **Right panel (comparison view):**
    - Split screen: "Før (Versjon X)" vs "Etter (Versjon Y)"
    - Toggle views: Gantt (default) / Precedence / Table
    - Summary stats at top:
      - Before: Total cost, End date (with ✓ or ❌)
      - After: Total cost, End date (with ✓ or ❌)
    - **Gantt comparison:**
      - Timeline showing changed tasks
      - Red bar: Old values (removed)
      - Green bar: New values (added)
      - Savings indicator: "-X MNOK, -Y dager"
      - Collapsed section for unchanged tasks
    - **Cascade effects panel (blue):**
      - Numbered list (1-5) showing impacts:
        - End date change
        - Budget change
        - Critical path change
        - Dependent task shifts
        - Validation status change
    - **Change summary stats:**
      - Economic impact: +/- X MNOK (Y%)
      - Time impact: +/- X dager (Y%)
  - **Action buttons:**
    - "◄ Gå til Versjon X" (navigate to specific version)
    - "Sammenlign andre versjoner" (select different versions to compare)
    - "✓ Bruk Versjon Y (nåværende)" (confirm current version)
  - **Export:**
    - "📥 Eksporter fullstendig historikk (JSON)"
    - "📊 Generer endringsrapport (PDF)"
  - Close button: "✕ Lukk historikk" (top right, red)
- **Data Structure:**
  ```javascript
  session.version_history = [
    {
      version: 1,
      timestamp: "2025-03-15T10:00:00Z",
      action: "commit",
      wbs_id: "1.3.1",
      changes: {cost: 105, duration: 60},
      snapshot: {current_plan: {...}, total_budget_used: 105, projected_end_date: "..."}
    },
    // ... all versions
  ]
  ```
- **Storage Limit:** Keep last 50 versions (auto-prune older versions)
- **Acceptance Test:**
  - User commits 5 WBS items → history shows 5 events
  - User clicks event 3 → comparison shows version 2 vs version 3
  - User clicks "Eksporter historikk" → JSON file downloads with all versions

---

**FR-9.4: Navigation Between Views**
- **Priority:** Must Have
- **Description:** Seamless navigation between Dashboard, Gantt, Precedence, and History views
- **Detailed Requirements:**
  - Main navigation tabs (always visible in header):
    - 📊 Dashbord
    - 📈 Gantt-diagram
    - 🔀 Presedensdiagram
  - 🕒 Historikk button in top-right (opens overlay panel on any view)
  - Active tab highlighted with blue background
  - All views share same header, user menu, help button
  - View state persists:
    - Gantt zoom level, scroll position
    - Precedence layout mode, filter settings
    - History selected version
  - All views update in real-time when plan changes
- **Acceptance Test:**
  - User navigates Dashboard → Gantt → Precedence → all show consistent data
  - User commits new WBS item → all views update immediately

---

## 6. Non-Functional Requirements

### 6.1 Performance

**NFR-1.1: AI Response Time**
- **Requirement:** AI responses must appear within 3 seconds (95th percentile)
- **Rationale:** Maintain immersion and engagement; delays break flow
- **Measurement:** Log `response_time = timestamp(AI response) - timestamp(user message)` in chat_logs
- **Target:** <3 seconds for 95% of requests, <5 seconds for 99%
- **Mitigation if violated:**
  - Use Gemini Flash instead of Pro for faster responses
  - Show typing indicator to set expectations
  - Optimize prompt length

**NFR-1.2: Dashboard Load Time**
- **Requirement:** Dashboard must render within 2 seconds on initial load
- **Target:** <2 seconds (First Contentful Paint), <3 seconds (Time to Interactive)
- **Measurement:** Lighthouse performance audit
- **Mitigation:**
  - Lazy load non-critical components
  - Use Vercel CDN for static assets
  - Optimize bundle size (code splitting)

**NFR-1.3: Validation Calculation Time**
- **Requirement:** Plan validation must complete within 1 second
- **Target:** <1 second for 15 WBS items
- **Rationale:** Instant feedback is critical for UX
- **Mitigation:**
  - Optimize critical path algorithm
  - Run validation client-side (no network round-trip)

---

### 6.2 Scalability

**NFR-2.1: Concurrent Users**
- **Requirement:** Support 100+ concurrent users without degradation
- **Target:** 100 simultaneous chat requests handled with <5 second response time
- **Measurement:** Load testing with simulated users
- **Mitigation:**
  - Stateless backend (easy horizontal scaling on Vercel)
  - Gemini API rate limits handled with queuing

**NFR-2.2: Data Storage per User**
- **Requirement:** Session data must fit within localStorage limits (5 MB per domain)
- **Target:** Typical session <500 KB (10x under limit)
- **Measurement:** Measure session JSON size after 100+ message simulation
- **Mitigation:**
  - If approaching limit, prompt user to export and start new session
  - Compress chat_logs if needed (remove redundant data)

---

### 6.3 Reliability

**NFR-3.1: System Uptime**
- **Requirement:** 99%+ uptime
- **Target:** <7.2 hours downtime per month
- **Measurement:** Vercel uptime monitoring
- **Mitigation:**
  - Use Vercel's enterprise SLA
  - Status page for known issues

**NFR-3.2: Data Persistence**
- **Requirement:** Session data must persist across browser restarts
- **Target:** 100% of sessions resumable if browser reopens within 7 days
- **Rationale:** Users may pause mid-session
- **Mitigation:**
  - localStorage persists until manually cleared
  - Remind users to export before clearing cache

**NFR-3.3: Error Recovery**
- **Requirement:** Graceful handling of all errors (no unhandled exceptions)
- **Target:** 0 unhandled errors causing white screen or crash
- **Measurement:** Sentry error tracking
- **Mitigation:**
  - Try-catch blocks around all critical operations
  - User-friendly error messages (never show stack traces)
  - "Retry" buttons for recoverable errors

---

### 6.4 Security

**NFR-4.1: Authentication Security**
- **Requirement:** User credentials protected according to industry standards
- **Implementation:** Supabase Auth handles password hashing (bcrypt), secure token generation (JWT)
- **Compliance:** GDPR-compliant (Supabase EU region)

**NFR-4.2: Data Privacy**
- **Requirement:** User session data is private and not shared
- **Implementation:**
  - Session data stored in user's own browser (localStorage)
  - Backend does not store session data (stateless)
  - Exported JSON includes user_id but no personally identifiable information beyond email
- **Compliance:** No PII stored beyond email (required for auth)

**NFR-4.3: Input Sanitization**
- **Requirement:** User inputs sanitized to prevent XSS attacks
- **Implementation:**
  - React escapes all rendered user content by default
  - Chat messages rendered as text (not HTML)
  - No `dangerouslySetInnerHTML` used

---

### 6.5 Usability

**NFR-5.1: Mobile Responsiveness**
- **Requirement:** Application must be usable on tablets (10+ inch screens)
- **Target:** Fully functional on iPad and similar tablets
- **Not Required (MVP):** Mobile phone support (<7 inch screens) - complex chat interface is difficult on small screens
- **Measurement:** Manual testing on iPad, Samsung Tab
- **Implementation:** Tailwind CSS responsive breakpoints

**NFR-5.2: Browser Compatibility**
- **Requirement:** Support latest 2 versions of major browsers
- **Target Browsers:**
  - Chrome 120+
  - Firefox 120+
  - Safari 17+
  - Edge 120+
- **Not Supported:** Internet Explorer (deprecated)
- **Measurement:** Manual testing, BrowserStack

**NFR-5.3: Accessibility**
- **Requirement:** Basic WCAG 2.1 Level A compliance
- **Target:**
  - Keyboard navigation (tab, enter, escape)
  - Screen reader compatibility (ARIA labels)
  - Sufficient color contrast (4.5:1 for text)
- **Measurement:** Lighthouse accessibility audit, manual screen reader testing
- **Implementation:**
  - Semantic HTML
  - Shadcn UI components (accessible by default)
  - Focus indicators on interactive elements

---

### 6.6 Maintainability

**NFR-6.1: Code Quality**
- **Requirement:** Code must be readable, well-documented, and follow standards
- **Implementation:**
  - TypeScript for type safety
  - ESLint + Prettier for code formatting
  - Component-level comments for complex logic
  - README with setup instructions

**NFR-6.2: Testability**
- **Requirement:** Critical functions must have unit tests
- **Target:** 70%+ code coverage for core logic (validation, critical path calculation)
- **Implementation:**
  - Vitest for unit tests
  - React Testing Library for component tests
  - Critical functions: `validatePlan()`, `calculateCriticalPath()`, `saveSession()`

---

### 6.7 Localization

**NFR-7.1: Language**
- **Requirement:** All UI text and AI responses in Norwegian (Bokmål)
- **Implementation:**
  - UI strings in Norwegian
  - AI system prompts specify: "Respond in Norwegian"
  - Static documents (WBS, requirements) already in Norwegian
- **Future:** English version can be added with i18n library (not MVP)

**NFR-7.2: Currency & Dates**
- **Requirement:** Display monetary values in NOK, dates in European format
- **Implementation:**
  - Currency: "105 MNOK" (Millioner Norske Kroner)
  - Dates: "15. mai 2026" (dd. MMMM yyyy)
  - Use Norwegian locale for number/date formatting

---

## 7. Technical Requirements

### 7.1 Frontend Technology Stack

**TR-1.1: Framework & Language**
- **Framework:** React 18+ with Next.js 14+ (App Router)
- **Language:** TypeScript 5+
- **Build Tool:** Next.js built-in (webpack/turbopack)
- **Package Manager:** npm or yarn

**TR-1.2: UI Libraries**
- **Styling:** Tailwind CSS 3+
- **Component Library:** Shadcn UI (copy-paste components, built on Radix UI)
- **Icons:** Lucide React or Heroicons
- **Fonts:** System fonts or Google Fonts (Inter, Open Sans)

**TR-1.3: State Management**
- **Session Data:** localStorage (direct read/write, no library needed)
- **UI State:** React Context API or Zustand (lightweight)
- **Form State:** React Hook Form (if complex forms needed)

**TR-1.4: Utilities**
- **Date Manipulation:** date-fns or day.js (lightweight)
- **UUID Generation:** `crypto.randomUUID()` (native browser API)
- **JSON Handling:** Native `JSON.parse/stringify`

---

### 7.2 Backend Technology Stack

**TR-2.1: Framework & Language**
- **Framework:** FastAPI 0.100+ (Python 3.11+)
- **Language:** Python 3.11+
- **ASGI Server:** Uvicorn (for local dev) or Vercel serverless (production)

**TR-2.2: AI Integration**
- **Library:** PydanticAI (for structured AI interactions)
- **AI Provider:** Google Gemini 2.5 Flash (preferred for MVP: 1-3 sec response time, cost-effective) or Pro (fallback if quality insufficient)
- **API Key:** Stored in environment variable (`GEMINI_API_KEY`)

**TR-2.3: Dependencies**
- **pydantic:** For request/response validation
- **python-dotenv:** For environment variables
- **httpx:** For async HTTP requests (if needed)

---

### 7.3 Authentication

**TR-3.1: Supabase Auth**
- **Service:** Supabase Auth (hosted, managed)
- **Region:** EU (for GDPR compliance)
- **Authentication Methods:** Email + Password only (MVP)
- **SDK:** `@supabase/supabase-js` (frontend), `supabase-py` (backend if needed)
- **Token Format:** JWT (signed by Supabase, verified client-side and server-side)

**TR-3.2: JWT Handling**
- **Storage:** localStorage['auth-token']
- **Expiration:** Configurable (default 1 hour, refresh token for longer sessions)
- **Validation:** Every backend API call validates JWT in Authorization header

---

### 7.4 Deployment & Hosting

**TR-4.1: Hosting Platform**
- **Platform:** Vercel
- **Frontend:** Static site generation (SSG) where possible, server-side rendering (SSR) where needed
- **Backend:** Vercel Serverless Functions (FastAPI endpoints)
- **Region:** EU (closest to Norwegian users)

**TR-4.2: Environment Variables**
- **Frontend (.env.local):**
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Backend (.env):**
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_KEY` (for server-side operations)
  - `GEMINI_API_KEY`

**TR-4.3: CI/CD**
- **Deployment:** Git-based (push to `main` branch triggers auto-deploy)
- **Preview Deploys:** Every pull request gets preview URL (Vercel feature)
- **Rollback:** Instant rollback via Vercel dashboard

---

### 7.5 Monitoring & Analytics

**TR-5.1: Error Tracking**
- **Tool:** Sentry (optional for MVP, recommended post-MVP)
- **Coverage:** Frontend errors, backend exceptions
- **Alerts:** Notify on critical errors (>10 errors/min)

**TR-5.2: Performance Monitoring**
- **Tool:** Vercel Analytics (built-in)
- **Metrics:** Page load time, API response time, Core Web Vitals

**TR-5.3: User Analytics**
- **Tool:** PostHog or Plausible (privacy-friendly, GDPR-compliant)
- **Events Tracked:**
  - Session started
  - Message sent
  - Quote committed
  - Plan validated (success/failure)
  - Session exported
- **No PII:** Track events without collecting personal data

---

## 8. Data Requirements

### 8.1 localStorage Schema (Complete)

**Key:** `nye-haedda-session-{user_id}`

**Schema:**
```typescript
interface GameSession {
  // Metadata
  user_id: string;              // From JWT
  game_id: string;              // UUID
  created_at: string;           // ISO 8601 timestamp
  completed_at: string | null;  // ISO 8601 or null if in_progress
  status: 'in_progress' | 'completed' | 'abandoned';

  // Static reference data (loaded from JSON files)
  wbs_items: WBSItem[];
  suppliers: Supplier[];

  // Dynamic session data
  chat_logs: ChatMessage[];
  plan_history: PlanHistoryEntry[];
  current_plan: Record<string, PlanEntry>;

  // Real-time metrics
  metrics: {
    total_budget_used: number;          // Sum of current_plan costs
    projected_end_date: string | null;  // ISO 8601 date or null
    negotiation_count: number;          // Total user messages sent
    renegotiation_count: number;        // Number of uncommit actions
    time_spent_seconds: number;         // Calculated from created_at
  };
}

interface WBSItem {
  id: string;                    // e.g., "1.3.1"
  name: string;                  // e.g., "Grunnarbeid"
  description: string;
  baseline_cost: number;         // MNOK
  baseline_duration: number;     // months
  dependencies: string[];        // WBS IDs
  suggested_suppliers: string[]; // Supplier IDs
}

interface Supplier {
  id: string;                    // e.g., "bjorn-eriksen"
  name: string;                  // e.g., "Bjørn Eriksen"
  role: string;                  // e.g., "Totalentreprenør"
  specialty: string[];           // WBS IDs this supplier handles
  persona_summary: string;
  system_prompt: string;         // Full AI prompt (sent to backend only)
  hidden_params: {
    min_cost_multiplier: number;     // e.g., 0.88
    min_duration_multiplier: number; // e.g., 0.92
  };
}

interface ChatMessage {
  timestamp: string;             // ISO 8601
  wbs_item: string;              // WBS ID
  supplier: string;              // Supplier ID
  sender: 'user' | 'ai' | 'system';
  message: string;
  extracted_offer?: {
    cost: number;
    duration: number;
  };
}

interface PlanHistoryEntry {
  timestamp: string;
  action: 'commit' | 'uncommit';
  wbs_item: string;
  supplier?: string;
  cost?: number;
  duration?: number;
  start_date?: string;           // ISO 8601 date
  end_date?: string;
}

interface PlanEntry {
  supplier: string;
  cost: number;
  duration: number;
  start_date: string;            // ISO 8601 date
  end_date: string;
  committed_at: string;          // ISO 8601 timestamp
}
```

---

### 8.2 Static Data Files

**File: `/public/data/wbs.json`**
- **Content:** Array of 15 WBS items for Hædda Barneskole project
- **Schema:** `WBSItem[]` (see above)
- **Source:** Extracted from `wbs.pdf` (manual data entry)
- **Size:** ~5-10 KB
- **Update Frequency:** Static (no updates post-launch for MVP)

**File: `/public/data/suppliers.json`**
- **Content:** Array of 5-10 supplier personas
- **Schema:** `Supplier[]` (see above)
- **Source:** Manually defined during prompt engineering
- **Size:** ~20-30 KB (system_prompts are verbose)
- **Update Frequency:** Updated during testing/tuning phase

**File: `/public/docs/wbs.pdf`**
- **Content:** Original WBS document (from LOG565 case)
- **Size:** ~1-2 MB
- **Access:** Direct download or embedded PDF viewer

**File: `/public/docs/krav-spec.pdf`**
- **Content:** Requirements specification (from LOG565 case)
- **Size:** ~1-2 MB

**File: `/public/docs/project-description.pdf`**
- **Content:** Project description (from LOG565 case)
- **Size:** ~500 KB - 1 MB

---

### 8.3 Export Data Format

**File Name:** `nye-haedda-session-{user_id}-{game_id}.json`

**Schema:**
```typescript
interface ExportData {
  // Metadata
  export_version: string;        // e.g., "1.0"
  exported_at: string;           // ISO 8601

  // Game info
  user_id: string;
  game_id: string;
  created_at: string;
  completed_at: string | null;
  status: string;

  // Complete logs
  chat_logs: ChatMessage[];
  plan_history: PlanHistoryEntry[];

  // Final state
  final_plan: Record<string, PlanEntry>;

  // Metrics
  metrics: {
    total_cost: number;
    completion_date: string;
    time_spent_minutes: number;
    negotiation_count: number;
    renegotiation_count: number;
  };

  // Context (for instructors/reviewers)
  wbs_items: WBSItem[];

  // Validation result
  validation: {
    valid: boolean;
    errors: Array<{type: string; message: string}>;
    warnings: Array<{type: string; message: string}>;
  };
}
```

---

## 9. API Specifications

### 9.1 Overview

**Base URL (Production):** `https://nye-haedda.vercel.app`
**Base URL (Development):** `http://localhost:8000` (Backend), `http://localhost:3000` (Frontend)

**Authentication:** JWT token in `Authorization: Bearer {token}` header (for endpoints that require auth)

**Content-Type:** `application/json`

**Note on API Prefix:** Current MVP implementation does not use `/api` prefix. Endpoints are at root level (e.g., `/negotiate` instead of `/api/negotiate`). This can be standardized in a future release by adding an API router prefix in FastAPI.

---

### 9.2 Endpoints

#### 9.2.1 GET /wbs

**Purpose:** Retrieve WBS items parsed from PDF

**Authentication:** None (MVP)

**Request:** None

**Response:**
```json
[
  {
    "id": "1.0",
    "name": "Grunnarbeid",
    "status": "Not Started"
  },
  ...
]
```

**Error Response:**
```json
{
  "error": "wbs.pdf not found at the expected path."
}
```

---

#### 9.2.2 POST /negotiate

**Purpose:** Send user message to AI supplier persona, receive AI response

**Authentication:** None (MVP)

**Request:**
```json
{
  "persona_id": "contractor",
  "message": "Can you reduce the cost for this task?"
}
```

**Supported Persona IDs:** `contractor`, `architect`, `hvac`

**Response (Success - 200 OK):**
```json
{
  "text": "As the General Contractor, we focus on delivering value. Let's discuss your budget and find an optimal solution.",
  "sender": "ai"
}
```

**Implementation Notes:**
- Current MVP uses simple keyword-based responses (not AI-powered yet)
- Backend matches keywords in user message to generate appropriate responses
- Future implementation will integrate Gemini API for dynamic AI negotiations
- Response is stateless (no session stored server-side)

---

#### 9.2.3 POST /validate (Optional - Can Be Client-Side - Not Yet Implemented)

**Purpose:** Validate project plan against constraints

**Authentication:** Optional

**Request:**
```json
{
  "current_plan": {
    "1.3.1": {"cost": 105, "duration": 2.5, "start_date": "2025-01-15", "end_date": "2025-04-01"},
    "2.1": {"cost": 200, "duration": 3, "start_date": "2025-04-01", "end_date": "2025-07-01"}
  },
  "wbs_items": [
    {"id": "1.3.1", "dependencies": ["1.2"]},
    {"id": "2.1", "dependencies": ["1.3.1"]}
  ]
}
```

**Response (Success - 200 OK):**
```json
{
  "valid": false,
  "errors": [
    {
      "type": "budget",
      "message": "Budget exceeded by 50 MNOK",
      "current": 750,
      "limit": 700
    },
    {
      "type": "timeline",
      "message": "Project delayed until May 20, 2026",
      "current": "2026-05-20",
      "limit": "2026-05-15"
    }
  ],
  "warnings": []
}
```

**Implementation Notes:**
- This endpoint is optional - validation can be done entirely client-side (faster, no network latency)
- Server-side validation is useful for instructor trust (they can validate exported JSON)

---

#### 9.2.4 GET /health (Not Yet Implemented)

**Purpose:** Health check endpoint

**Authentication:** None

**Response (Success - 200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2025-12-07T12:34:56Z",
  "version": "1.0.0"
}
```

---

## 10. UI/UX Requirements

### 10.1 Design Principles

**DP-1: Clarity Over Cleverness**
- UI should be immediately understandable (no hidden features)
- Labels and buttons use clear, action-oriented language
- Example: "Submit Plan" not "Finish", "Renegotiate" not "Undo"

**DP-2: Enterprise Aesthetic**
- Professional, clean design (not gamified or playful)
- Suitable for academic/professional context
- Color scheme: Neutral grays, blues, greens (avoid bright/flashy colors)
- Typography: Sans-serif, high readability (Inter, Open Sans)

**DP-3: Immediate Feedback**
- All user actions have instant visual response
- Button clicks show loading state
- Form submissions show success/error immediately
- Dashboard updates in real-time (no manual refresh)

**DP-4: Progressive Disclosure**
- Don't overwhelm users with all information at once
- WBS item details hidden until clicked (expand/collapse)
- Advanced features (e.g., export) appear after completion

---

### 10.2 Page Layouts

#### 10.2.1 Login/Register Page

**Layout:**
- Centered form on neutral background
- Logo/title at top: "Nye Hædda Barneskole - Project Management Simulation"
- Form fields:
  - Email input (with validation)
  - Password input (with show/hide toggle)
  - "Login" button (primary CTA)
  - "Don't have an account? Register" link
- Error messages appear above form (red text)

**Responsive:**
- Form width: 400px desktop, 90% mobile
- Single column layout

---

#### 10.2.2 Dashboard (Main Game View)

**Layout (Desktop):**
```
+--------------------------------------------------+
| Header: Logo | User Menu (Logout)                |
+--------------------------------------------------+
| Constraint Panel:                                |
|   Budget: [========>    ] 450 / 700 MNOK (64%)   |
|   Deadline: May 15, 2026                         |
|   Projected End: April 10, 2026 ✓                |
+--------------------------------------------------+
| Quick Stats: 8/15 WBS Completed | 32 Negotiations|
+--------------------------------------------------+
| WBS List                      | [Submit Plan]    |
| ⚪ 1.1 Prosjektering          | [Help]           |
| 🟢 1.3.1 Grunnarbeid          |                  |
|     105 MNOK, 2.5 mnd         |                  |
|     [Renegotiate]             |                  |
| ⚪ 2.1 Råbygg                 |                  |
|     [Contact Supplier]        |                  |
+--------------------------------------------------+
```

**Layout (Mobile/Tablet):**
- Stack vertically: Constraint Panel → Quick Stats → WBS List
- Collapsible sections to save space

---

#### 10.2.3 Negotiation/Chat Page

**Layout (Desktop):**
```
+--------------------------------------------------+
| Header: [< Back to Dashboard] | Bjørn Eriksen -  |
|         Totalentreprenør | WBS 1.3.1 Grunnarbeid |
+--------------------------------------------------+
| Chat Window                | Document Sidebar   |
| (scrollable)               | 📄 WBS              |
|                            | 📄 Requirements     |
| User: Quote?               | 📄 Project Desc     |
| AI: 120 MNOK, 3 months     |                    |
| User: Too high...          |                    |
| AI: 105 MNOK, 2.5 months   |                    |
|   [Accept: 105 MNOK, 2.5]  |                    |
+--------------------------------------------------+
| [Message Input]                    | [Send]      |
+--------------------------------------------------+
```

**Chat Message Styles:**
- User messages: Right-aligned, blue background (#3B82F6), white text
- AI messages: Left-aligned, gray background (#E5E7EB), black text
- System messages: Center-aligned, small gray text, italic

---

### 10.3 Component Specifications

#### 10.3.1 Button Styles

**Primary Button** (e.g., "Submit Plan", "Send", "Accept Offer")
- Background: Blue (#3B82F6)
- Text: White, bold
- Hover: Darker blue (#2563EB)
- Disabled: Gray (#9CA3AF), cursor not-allowed

**Secondary Button** (e.g., "Cancel", "Back")
- Background: White
- Border: Gray (#D1D5DB)
- Text: Gray (#374151)
- Hover: Light gray background

**Danger Button** (e.g., "Renegotiate", "Uncommit")
- Background: Red (#EF4444)
- Text: White
- Hover: Darker red (#DC2626)

---

#### 10.3.2 Form Inputs

**Text Input:**
- Border: Gray (#D1D5DB), 2px
- Focus: Blue border (#3B82F6)
- Error state: Red border (#EF4444)
- Placeholder: Gray text (#9CA3AF)

**Text Area (Chat Input):**
- Height: 60px (expandable)
- Border: Same as text input
- Max height: 200px (with scrollbar)

---

#### 10.3.3 Status Indicators

**WBS Item Status:**
- ⚪ Pending: Light gray circle
- 🟢 Completed: Green circle with checkmark

**Budget Progress Bar:**
- Background: Light gray (#E5E7EB)
- Fill color:
  - Green (#10B981): 0-680 MNOK
  - Yellow (#F59E0B): 680-700 MNOK
  - Red (#EF4444): >700 MNOK
- Height: 20px
- Border radius: 10px (rounded)

---

#### 10.3.4 Modals

**Structure:**
- Overlay: Semi-transparent black (#000000 40% opacity)
- Modal box: White, centered, max-width 600px
- Close button: X icon in top-right
- Buttons: Primary + Secondary at bottom-right

**Examples:**
- Confirmation Modal (Commit): "Confirm commitment: 105 MNOK, 2.5 months?"
- Error Modal (Validation Failure): Red error icon, error list, "Back to Planning" button
- Success Modal (Plan Approved): Green success icon, stats table, "Export" and "New Game" buttons

---

### 10.4 Responsive Breakpoints

**Tailwind CSS Breakpoints:**
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (desktops)
- `xl`: 1280px (large desktops)

**Design Priorities:**
- Desktop-first design (primary use case)
- Tablet support (iPad horizontal)
- Mobile support (nice-to-have, not critical for MVP)

---

### 10.5 Accessibility

**Keyboard Navigation:**
- Tab order: Header → Main content → Footer
- Enter key submits forms, Escape closes modals
- Focus indicators visible (blue outline)

**Screen Reader Support:**
- All buttons have aria-label
- Form inputs have associated <label>
- Status indicators have aria-live regions (announce updates)

**Color Contrast:**
- Text on white background: ≥4.5:1 contrast ratio
- Important buttons: ≥7:1 contrast (AAA level)

---

## 11. Success Metrics

*(Detailed metrics already defined in Section 2.2 and Brainstorming Summary. Reference those for complete list.)*

**Key Metrics Summary:**

**User Engagement:**
- Completion Rate: ≥60%
- Time to Completion: 45-60 minutes
- Renegotiation Rate: ≥40%

**Learning Outcomes:**
- Document Utilization: ≥50%
- Constraint Awareness: ≥70%
- Negotiation Strategy Diversity: ≥3 tactics per user

**User Satisfaction:**
- Post-Simulation Survey: ≥4.0/5.0
- NPS: ≥50% Promoters

**Technical Performance:**
- AI Response Time: <3 seconds (95th percentile)
- System Uptime: ≥99%

---

## 12. Scope Definition

### 12.1 In Scope (MVP)

✅ **Must Have Features (15 total):**
1. User authentication (Supabase)
2. Session initialization and persistence (localStorage)
3. Project dashboard with constraints
4. WBS view
5. Supplier directory
6. AI chat interface
7. AI supplier logic (Gemini integration)
8. Quote acceptance and commitment
9. Real-time plan validation
10. Plan submission and win/loss state
11. Session export (JSON)
12. Renegotiation capability
13. Document access (PDFs)
14. Error handling and loading states
15. Help documentation

✅ **Technical Components:**
- React + Next.js frontend
- FastAPI backend (2-3 endpoints)
- Supabase Auth
- localStorage for session data
- Static JSON files (WBS, suppliers)

✅ **Single Scenario:**
- Nye Hædda Barneskole only

---

### 12.2 Out of Scope (MVP)

❌ **Post-MVP (Should Have):**
- Cloud backup (Supabase Storage)
- Visual Gantt chart
- PDF export
- Negotiation hints
- Auto-save to cloud
- Session import

❌ **Future (Could Have):**
- Difficulty settings
- Random risk events
- Multiplayer mode
- Instructor dashboard
- Alternative scenarios
- Achievements/badges
- AI voice chat
- Mobile native app

❌ **Explicitly Not Building:**
- Execution phase simulation
- Financial management (beyond budget totals)
- 3D visualization
- MS Project integration
- Social features
- VR/AR experience

---

## 13. Dependencies and Assumptions

### 13.1 External Dependencies

**DEP-1: Supabase Service**
- **Dependency:** Supabase Auth must be available and operational
- **Risk:** Supabase downtime prevents user login
- **Mitigation:** Use Supabase's 99.9% uptime SLA; have status page for known issues
- **Contingency:** If Supabase has prolonged outage, users can still access simulation if already logged in (JWT cached)

**DEP-2: Gemini API**
- **Dependency:** Google Gemini 2.5 API must be available
- **Risk:** API downtime or rate limiting prevents AI responses
- **Mitigation:** Implement retry logic with exponential backoff; show user-friendly error: "AI service temporarily unavailable"
- **Contingency:** Queue requests during rate limits; consider fallback to Gemini Flash (lower quality but higher availability)

**DEP-3: Vercel Platform**
- **Dependency:** Vercel for hosting and deployment
- **Risk:** Vercel downtime affects application availability
- **Mitigation:** Vercel has 99.99% uptime SLA; global CDN reduces regional failures
- **Contingency:** Static assets can be mirrored to alternative CDN if needed

---

### 13.2 Data Dependencies

**DEP-4: Static WBS Data**
- **Dependency:** Accurate extraction of WBS from wbs.pdf into wbs.json
- **Risk:** Manual data entry errors (wrong costs, missing dependencies)
- **Mitigation:** Manual review and validation against original PDF; cross-reference with LOG565 course materials
- **Verification:** Test simulation with known valid plan to ensure constraints are achievable

**DEP-5: Requirements Specification**
- **Dependency:** Requirements from krav-spec.pdf must be accurately represented in AI prompts
- **Risk:** AI references incorrect or outdated requirements
- **Mitigation:** Extract key requirements during prompt engineering; manual review of AI responses during testing

---

### 13.3 Assumptions

**ASM-1: User Device Capabilities**
- **Assumption:** Users have devices with:
  - Modern browsers (Chrome 120+, Firefox 120+, Safari 17+)
  - ≥5 MB available localStorage
  - Stable internet connection (for AI API calls)
- **Validation:** Test on common student devices (laptops, iPads)

**ASM-2: Session Completion in Single Sitting**
- **Assumption:** Most users will complete simulation in one 45-60 minute session without needing to resume on different device
- **Rationale:** This assumption justifies localStorage-only approach (no database)
- **Validation:** Track session duration and abandonment rate during pilot testing
- **Fallback:** If assumption proves false, add cloud backup feature (Should-Have)

**ASM-3: Instructor Manual Review**
- **Assumption:** Instructors are willing to manually review exported JSON files (no automated dashboard for MVP)
- **Rationale:** Keeps MVP scope minimal
- **Validation:** Confirm with 2-3 instructors during pilot
- **Fallback:** Build instructor dashboard post-MVP if demand is high

**ASM-4: Norwegian Language Sufficiency**
- **Assumption:** Norwegian-only UI and AI is acceptable for target market (LOG565 students in Norway)
- **Validation:** Confirm with instructors and students
- **Fallback:** Add English version post-MVP for international expansion

**ASM-5: Free Tier Sustainability**
- **Assumption:** Gemini API costs remain <2 NOK per session, making free access sustainable
- **Validation:** Monitor costs during pilot testing
- **Fallback:** If costs exceed projections, implement rate limiting (e.g., max 100 messages per session) or explore freemium model

---

### 13.4 Constraints

**CON-1: Development Timeline**
- **Constraint:** MVP must be completed in 3-4 weeks
- **Impact:** Limits feature scope; prioritize Must-Haves only
- **Mitigation:** Use pre-built libraries (Supabase, Shadcn, PydanticAI) to accelerate development

**CON-2: Budget**
- **Constraint:** Minimal budget for MVP (assumes free tiers: Vercel, Supabase, Gemini)
- **Impact:** Cannot use premium features or paid support
- **Mitigation:** Design architecture to stay within free tier limits

**CON-3: Team Size**
- **Constraint:** Small team (1-2 developers for MVP)
- **Impact:** Limited parallel workstreams
- **Mitigation:** Clear separation of concerns (frontend/backend can be developed in parallel if 2 developers)

---

## 14. Glossary

**AI Agent / AI Supplier:** A persona-driven AI chatbot representing a specific supplier (e.g., Bjørn Eriksen - Totalentreprenør). Powered by Gemini 2.5, configured with system prompts to behave consistently with the persona.

**Baseline Estimate:** The initial cost and duration estimate for a WBS item, provided in the WBS document. Used as a reference point for negotiations but not binding.

**Commitment:** The act of accepting a negotiated quote and adding it to the project plan. Creates a plan entry with cost, duration, start date, and end date.

**Critical Path:** The longest sequence of dependent tasks in the project plan. Determines the projected end date.

**Current Plan:** The set of all currently committed WBS items. Stored in `session.current_plan` in localStorage.

**Gemini:** Google's large language model (LLM) used to power AI supplier responses. Accessed via API.

**Hædda Barneskole:** The construction project case study from LOG565 course. A new elementary school in Hædda municipality, Norway.

**Hidden Parameters:** Minimum acceptable cost and duration values for each AI supplier, enforced in the system prompt. Not visible to users. Prevents AI from accepting unrealistically low offers.

**localStorage:** Browser-based storage (5-10 MB per domain) where the entire game session is persisted. Data survives page refreshes but is cleared if user clears browser cache.

**LOG565:** Project Management 2 course at Norwegian business schools (e.g., BI, NHH, NTNU).

**MNOK:** Millioner Norske Kroner (Millions of Norwegian Kroner). Currency unit used in the simulation (e.g., 700 MNOK budget).

**MVP (Minimum Viable Product):** The initial version of the simulation with only essential features (15 Must-Haves). Designed to validate product-market fit.

**Persona:** The personality, motivations, and negotiation style of an AI supplier. Defined in the system prompt.

**Plan History:** A chronological log of all commit and uncommit actions. Stored in `session.plan_history`. Used for export and tracking changes.

**PydanticAI:** Python library for building AI agents with structured inputs/outputs. Simplifies Gemini API integration.

**Renegotiation:** The act of uncommitting a previously committed WBS item and reopening negotiations. Allows iterative planning.

**Session:** A single playthrough of the simulation. Starts when user clicks "Start New Game", ends when plan is successfully submitted or abandoned.

**Supabase:** Backend-as-a-Service platform. Used for authentication (JWT tokens) in this project.

**System Prompt:** The initial instructions given to the AI that define its persona, knowledge, and behavior. Includes supplier personality, negotiation rules, and references to project documents.

**Uncommit:** Remove a previously committed WBS item from the current plan. Budget and timeline recalculate. Logged in plan_history.

**WBS (Work Breakdown Structure):** Hierarchical decomposition of project work into manageable tasks. 15 items total for Hædda project.

**WBS Item:** A single task in the WBS (e.g., "1.3.1 - Grunnarbeid"). Has baseline cost, duration, dependencies, and suggested suppliers.

---

## Appendices

### Appendix A: Static Data File Samples

**Sample: wbs.json (excerpt)**
```json
[
  {
    "id": "1.1",
    "name": "Prosjektering",
    "description": "Design and engineering phase",
    "baseline_cost": 30,
    "baseline_duration": 0.5,
    "dependencies": [],
    "suggested_suppliers": ["siri-hansen"]
  },
  {
    "id": "1.3.1",
    "name": "Grunnarbeid",
    "description": "Site preparation, earthwork, foundation groundwork",
    "baseline_cost": 100,
    "baseline_duration": 2,
    "dependencies": ["1.2"],
    "suggested_suppliers": ["bjorn-eriksen", "kari-jensen"]
  },
  {
    "id": "2.1",
    "name": "Råbygg - Fundament",
    "description": "Foundation construction",
    "baseline_cost": 150,
    "baseline_duration": 3,
    "dependencies": ["1.3.1"],
    "suggested_suppliers": ["bjorn-eriksen"]
  }
]
```

---

**Sample: suppliers.json (excerpt)**
```json
[
  {
    "id": "bjorn-eriksen",
    "name": "Bjørn Eriksen",
    "role": "Totalentreprenør",
    "specialty": ["1.3.1", "2.1", "2.2", "2.3"],
    "persona_summary": "Profit-driven general contractor. Experienced negotiator who starts with inflated quotes but is flexible with strong evidence-based arguments.",
    "system_prompt": "You are Bjørn Eriksen, a general contractor (Totalentreprenør) with 20 years of experience in Norwegian construction. Your main goal is to maximize profit while maintaining a good industry reputation. You start negotiations with quotes 15-20% above your minimum acceptable cost, but you can be negotiated down with strong arguments. You respect project managers who reference requirements specifications (krav-spec) and industry standards. You become more flexible when users propose creative solutions like phased delivery or alternative materials. You speak Norwegian. Never accept offers below {{baseline_cost * 0.88}} MNOK or {{baseline_duration * 0.92}} months for this WBS item.",
    "hidden_params": {
      "min_cost_multiplier": 0.88,
      "min_duration_multiplier": 0.92
    }
  }
]
```

---

### Appendix B: User Journey Example (Detailed)

*(This is a condensed reference to the detailed user journey in Brainstorming Executive Summary, Section 7)*

**Sara's Complete Journey (34 Steps):**
1. Discovery → 2. Registration → 3. Login → ... → 34. Exam Success

**Key Phases:**
- Onboarding (5 min)
- First Negotiation (10-15 min)
- Iteration & Crisis (20-25 min)
- Completion & Success (5-10 min)
- Transfer to Real World (1 week later)

---

### Appendix C: Validation Algorithm (Pseudocode)

```typescript
function validatePlan(session: GameSession): ValidationResult {
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];

  // 1. Completeness Check
  const committedCount = Object.keys(session.current_plan).length;
  const totalWBSItems = session.wbs_items.length;
  if (committedCount < totalWBSItems) {
    errors.push({
      type: 'completeness',
      message: `Only ${committedCount}/${totalWBSItems} WBS items committed`,
      missing: session.wbs_items
        .filter(w => !session.current_plan[w.id])
        .map(w => w.id)
    });
  }

  // 2. Budget Check
  const totalCost = Object.values(session.current_plan)
    .reduce((sum, entry) => sum + entry.cost, 0);

  if (totalCost > 700) {
    errors.push({
      type: 'budget',
      message: `Budget exceeded by ${totalCost - 700} MNOK`,
      current: totalCost,
      limit: 700,
      suggestions: getHighCostItems(session.current_plan, 3) // Top 3 expensive items
    });
  } else if (totalCost > 680) {
    warnings.push({
      type: 'budget',
      message: `Budget at ${(totalCost/700*100).toFixed(1)}% - limited flexibility`
    });
  }

  // 3. Timeline Check (Critical Path Calculation)
  const endDate = calculateCriticalPath(session.current_plan, session.wbs_items);
  const deadline = new Date('2026-05-15');

  if (endDate > deadline) {
    const daysLate = Math.ceil((endDate.getTime() - deadline.getTime()) / (1000*60*60*24));
    errors.push({
      type: 'timeline',
      message: `Project delayed by ${daysLate} days`,
      current: endDate.toISOString().split('T')[0],
      limit: '2026-05-15'
    });
  }

  // 4. Dependency Check
  for (const [wbsId, entry] of Object.entries(session.current_plan)) {
    const wbsItem = session.wbs_items.find(w => w.id === wbsId);

    for (const depId of wbsItem.dependencies) {
      const depEntry = session.current_plan[depId];

      if (!depEntry) {
        errors.push({
          type: 'dependency',
          message: `${wbsId} requires ${depId} to be completed first`,
          wbs_item: wbsId,
          missing_dependency: depId
        });
      } else if (new Date(entry.start_date) < new Date(depEntry.end_date)) {
        errors.push({
          type: 'dependency',
          message: `${wbsId} starts (${entry.start_date}) before ${depId} finishes (${depEntry.end_date})`,
          wbs_item: wbsId,
          blocking_dependency: depId
        });
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors: errors,
    warnings: warnings
  };
}

function calculateCriticalPath(
  currentPlan: Record<string, PlanEntry>,
  wbsItems: WBSItem[]
): Date {
  // Topological sort + longest path algorithm
  // (Implementation details omitted for brevity)
  // Returns the latest end_date in the critical path
}
```

---

### Appendix D: Critical Path Calculation Notes

**Algorithm:** Topological Sort + Longest Path

**Steps:**
1. Build dependency graph from WBS items
2. Topological sort (ensures dependencies processed before dependents)
3. For each node in topological order:
   - Calculate earliest start: MAX(dependency end dates)
   - Calculate end: start + duration
4. Return maximum end date across all nodes

**Edge Cases:**
- Circular dependencies: Should not exist in WBS data (validation during data entry)
- Missing dependencies: Validation catches this before calculation
- Multiple paths: Algorithm finds the longest (critical) path

**Performance:**
- Time complexity: O(V + E) where V=WBS items, E=dependencies
- For 15 WBS items: <1ms calculation time

---

### Appendix E: Sample localStorage Sessions

This appendix provides examples of localStorage data structure at different stages of gameplay to aid frontend development and testing.

#### E.1 Empty Session (New Game)

```json
{
  "gameId": "game_1733645231000",
  "userId": "user_abc123",
  "createdAt": "2025-12-08T10:00:31Z",
  "status": "in_progress",
  "budgetUsed": 0,
  "projectedEndDate": null,
  "planEntries": [],
  "chatLogs": [],
  "metadata": {
    "lastModified": "2025-12-08T10:00:31Z",
    "version": "1.0"
  }
}
```

**Size:** ~250 bytes

#### E.2 Partially Complete Session (3/15 WBS Items)

```json
{
  "gameId": "game_1733645231000",
  "userId": "user_abc123",
  "createdAt": "2025-12-08T10:00:31Z",
  "status": "in_progress",
  "budgetUsed": 215000000,
  "projectedEndDate": "2026-03-15",
  "planEntries": [
    {
      "wbsId": "1.3.1",
      "wbsName": "Grunnarbeid",
      "supplierId": "supplier_groundwork",
      "duration": 60,
      "cost": 105000000,
      "startDate": "2025-01-01",
      "dependencies": [],
      "negotiatedAt": "2025-12-08T10:15:00Z"
    },
    {
      "wbsId": "1.3.2",
      "wbsName": "Fundamentering",
      "supplierId": "supplier_foundation",
      "duration": 45,
      "cost": 60000000,
      "startDate": "2025-03-01",
      "dependencies": ["1.3.1"],
      "negotiatedAt": "2025-12-08T10:32:00Z"
    },
    {
      "wbsId": "1.4.1",
      "wbsName": "Råbygg",
      "supplierId": "supplier_construction",
      "duration": 90,
      "cost": 50000000,
      "startDate": "2025-04-15",
      "dependencies": ["1.3.2"],
      "negotiatedAt": "2025-12-08T10:48:00Z"
    }
  ],
  "chatLogs": [
    {
      "supplierId": "supplier_groundwork",
      "messages": [
        {
          "role": "user",
          "content": "Jeg trenger et pristilbud for grunnarbeid (WBS 1.3.1). Varighet og kostnad?",
          "timestamp": "2025-12-08T10:12:00Z"
        },
        {
          "role": "assistant",
          "content": "Basert på grunnforholdene i Hædda kan vi levere grunnarbeid på 3 måneder for 120 MNOK.",
          "timestamp": "2025-12-08T10:12:15Z"
        },
        {
          "role": "user",
          "content": "Budsjettet er stramt. Kan vi optimalisere ned til 2 måneder og 105 MNOK?",
          "timestamp": "2025-12-08T10:13:00Z"
        },
        {
          "role": "assistant",
          "content": "Med dobbelskift og effektiv ressursbruk kan vi redusere til 2 måneder for 105 MNOK. Akseptert.",
          "timestamp": "2025-12-08T10:13:30Z"
        }
      ]
    }
  ],
  "metadata": {
    "lastModified": "2025-12-08T10:48:00Z",
    "negotiationCount": 8,
    "version": "1.0"
  }
}
```

**Size:** ~2.1 KB (estimated ~20 KB for full 15 WBS items with chat logs)

#### E.3 Complete Session (All 15 WBS Items, Within Budget)

```json
{
  "gameId": "game_1733645231000",
  "userId": "user_abc123",
  "createdAt": "2025-12-08T10:00:31Z",
  "status": "completed",
  "budgetUsed": 695000000,
  "projectedEndDate": "2026-05-10",
  "completedAt": "2025-12-08T11:45:00Z",
  "planEntries": [
    {
      "wbsId": "1.3.1",
      "wbsName": "Grunnarbeid",
      "supplierId": "supplier_groundwork",
      "duration": 60,
      "cost": 105000000,
      "startDate": "2025-01-01",
      "dependencies": [],
      "negotiatedAt": "2025-12-08T10:15:00Z"
    },
    {
      "wbsId": "1.3.2",
      "wbsName": "Fundamentering",
      "supplierId": "supplier_foundation",
      "duration": 45,
      "cost": 60000000,
      "startDate": "2025-03-01",
      "dependencies": ["1.3.1"],
      "negotiatedAt": "2025-12-08T10:32:00Z"
    },
    ...
    // (13 more WBS items omitted for brevity)
  ],
  "chatLogs": [
    ...
    // (Full negotiation history for 3 negotiable WBS items with 4 agents, ~10-20 messages total)
  ],
  "validationResult": {
    "budgetValid": true,
    "deadlineValid": true,
    "allItemsComplete": true,
    "criticalPath": ["1.3.1", "1.3.2", "1.4.1", "1.4.2", "1.5.1"],
    "validatedAt": "2025-12-08T11:45:00Z"
  },
  "metadata": {
    "lastModified": "2025-12-08T11:45:00Z",
    "negotiationCount": 42,
    "sessionDuration": 6300,
    "version": "1.0"
  }
}
```

**Size:** ~62 KB (validated to fit within localStorage 5 MB limit; allows 80+ sessions)

#### E.4 Storage Monitoring Example

Frontend should implement storage checks:

```typescript
function checkStorageUsage() {
  const used = JSON.stringify(localStorage).length;
  const usedKB = (used / 1024).toFixed(2);
  const usedPercent = ((used / (5 * 1024 * 1024)) * 100).toFixed(1);

  console.log(`localStorage: ${usedKB} KB used (${usedPercent}%)`);

  if (usedPercent > 80) {
    // Warn user: "Lagringsplass lav. Vurder å eksportere gamle økter."
  }
}
```

**Reference:** See `research-report-2025-12-07.md` Section 2 for full localStorage capacity analysis.

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | [TBD] | | |
| Technical Lead | [TBD] | | |
| UX Designer | [TBD] | | |
| QA Lead | [TBD] | | |

---

**End of Product Requirements Document (PRD)**

*This document defines the complete functional and technical requirements for the Nye Hædda Barneskole Project Management Simulation MVP. All implementation work should reference this PRD as the single source of truth.*

**Next Steps:**
1. PRD Validation (stakeholder review)
2. UX Design (wireframes, user flows)
3. Implementation (Week 1-4)
4. Testing & Launch (Week 4)
