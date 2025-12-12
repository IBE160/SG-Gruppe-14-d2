# Scope Change Implementation Tasks
## Nye Hædda Barneskole - Nedskalert Scope

**Document Version:** 1.1
**Date:** 2025-12-11
**Status:** Implementation Guide
**Source:** "Nytt scope og nødvendige endringer.pdf" + Supabase Database Integration

---

## Executive Summary

This document tracks the major scope changes from the original plan (15 suppliers, 15 WBS packages) to the scaled-down POC (3 suppliers, 3 WBS packages, 4 AI agent roles). The focus is on AI agent negotiation with realistic constraints.

### Key Changes at a Glance:
- **Suppliers:** 15 → 3 negotiable suppliers
- **WBS Packages:** 15 → 3 negotiable packages (3 of 5 on critical path)
- **AI Agent Roles:** 5 supplier personas → 4 distinct roles (Owner + 3 suppliers)
- **Budget Model:** 700 MNOK total → 310 MNOK available for 3 negotiable packages (650 MNOK locked)
- **Negotiation Types:** 3 main strategies (quality, scope, time/cost trade-offs)
- **Time Constraint:** 15 months INFLEXIBLE (enforced via system prompts)
- **Owner Role:** New AI agent representing municipality (budget negotiation only)
- **Data Storage:** localStorage → **Supabase Database** (authentication + game sessions)

---

## Table of Contents

1. [Scaled-Down Scope Details](#1-scaled-down-scope-details)
2. [Roles and Negotiation Possibilities](#2-roles-and-negotiation-possibilities)
3. [Critical Path, Budget, and Time](#3-critical-path-budget-and-time)
4. [System Prompts (AI Agents)](#4-system-prompts-ai-agents)
5. [Supabase Database Integration](#5-supabase-database-integration)
6. [Consequences for Mockups and Repository](#6-consequences-for-mockups-and-repository)
7. [Implementation Checklist](#7-implementation-checklist)
8. [File-by-File Update Plan](#8-file-by-file-update-plan)

---

## 1. Scaled-Down Scope Details

### Original Scope:
- 15 suppliers
- 15 WBS work packages
- User negotiates all 15
- Total budget: 700 MNOK, 15 months

### New Scope:
- **3 negotiable suppliers** and **3 negotiable WBS packages**
- The remaining 12 suppliers/packages are already contracted ("locked/gray")
- User can ONLY work with these 3 packages and 3 suppliers
- Rest of budget and time considered already committed

### Rationale:
> "Jobben ligger i AI-agentene/de nå 4 rollene og vi trenger POC asap."

The focus is on proving the AI agent negotiation concept, not on building a complete simulation with 15 items.

---

## 2. Roles and Negotiation Possibilities

### 2.1 Owner (Municipality - "Eier/Kommunen")

**Role:** The only party that can adjust budget or time.

**CRITICAL RULE:**
> "Tiden kan ikke forlenges, selv om dette bare skal komme frem gjennom dialog med AI-agenten (system prompt må gjøre dette ufravikelig)."

**Negotiation Powers:**
- ✅ Can increase budget (with strong user argumentation)
- ❌ **CANNOT extend time** (inflexible - must be enforced via system prompt)

**System Prompt Requirement:**
- Must reject all time extension requests with explanation: "Skolen må stå klar til skolestart i august; samfunnskostnaden ved forsinkelse er høyere enn økt budsjett."

---

### 2.2 Suppliers (3 Total)

**Supplier Negotiation Powers:**

1. **Deliver faster for higher cost**
   - Overtime/increased capacity → higher price
   - If cost exceeds budget → requires budget negotiation with Owner
   - User must argue well to Owner AI for budget increase

2. **Deliver cheaper for lower quality**
   - Reduced quality trade-off
   - Supplier can offer lower price if user accepts quality reduction

---

### 2.3 Three Main Negotiation Strategies

| Strategy | Description | Who to Negotiate With |
|----------|-------------|----------------------|
| **Reduced Quality** | Accept lower quality for lower cost | **Supplier** |
| **Reduced Scope** | Remove features from the building (e.g., fewer classrooms) | **Owner** |
| **Shorter Time for Higher Cost** | Faster delivery via overtime/more workers | **Supplier → Owner** (if budget exceeded) |

---

## 3. Critical Path, Budget, and Time

### 3.1 Critical Path Structure

**Original mockup:** 15 WBS items total, 5 on critical path

**New structure:**
- **3 negotiable packages** must be **3 of the 5 on critical path**
- The remaining 2 critical path items are locked/contracted
- 12 other WBS items are "gray" (already contracted)

### Reference from PDF:
> "De 3 forhandlingsbare leverandørene/WBS-pakkene skal være 3 av 5 WBS'er på kritisk sti (ref. utdatert mockup)."

---

### 3.2 Budget Model

**Total Project Budget:** 700 MNOK, 15 months

**Budget Breakdown:**

| Category | Amount | Status |
|----------|--------|--------|
| 12 "Gray" Suppliers (locked) | ~650 MNOK | Already contracted, 13 months |
| **3 Negotiable Packages** | **310 MNOK available** | User must negotiate within this |
| **Total** | **700 MNOK** | **15 months deadline** |

**Baseline Estimate for 3 Packages (from old mockup):**
- WBS 1.3.1 Grunnarbeid: 105 MNOK
- WBS 1.3.2 Fundamentering: 60 MNOK
- WBS 1.4.1 Råbygg: 180 MNOK
- **Total:** 345 MNOK

**THE CHALLENGE:**
> "For å gjøre det mer utfordrende kan vi for eksempel legge opp til at de tre kritiske pakkene i simuleringen bare har 310 MNOK tilgjengelig (dvs. 45 MNOK under anslaget fra mockup), slik at brukeren må forhandle for å få disse på plass."

**User starts with deficit:** 345 MNOK baseline - 310 MNOK available = **35-45 MNOK shortfall**

User MUST negotiate to reduce costs or get Owner to approve budget increase.

---

### 3.3 Budget Flexibility

**From Bård (stakeholder):**
> "Dersom de tre kritiske WBS-pakkene samlet blir større enn det vi klarer å «hente inn» innenfor 50 MNOK, kan vi justere rammene slik: vi senker de 650 MNOK som ligger på de grå/kontraktfestede leverandørene tilsvarende."

**Acceptable Total Budget:**
- Slightly over 700 MNOK is acceptable
- **Priority: TIME > BUDGET**
- "Riktig tid er viktigst" - meeting the deadline is more important than staying under budget

---

### 3.4 Time Constraint

**Deadline:** May 15, 2026 (15 months from project start)

**INFLEXIBLE:**
> "Tiden kan ikke forlenges."

**Reason (from Bård):**
> "Skolen må stå klar til skolestart i august; samfunnskostnaden ved forsinkelse er høyere enn økt budsjett."

**System Prompt Enforcement:**
- Owner AI agent must **ALWAYS refuse** time extension requests
- Even if user begs, Owner must explain: societal cost of delay > increased budget
- Supplier AI agents should not offer time extensions directly (only faster delivery for more cost)

---

## 4. System Prompts (AI Agents)

### 4.1 New AI Agent Structure

**Old:** 5 supplier personas (Bjørn, Kari, Per, Silje, Tor)
**New:** **4 AI agent roles**

1. **Owner Agent** (Municipality - "Kommunen")
2. **Supplier Agent 1** (e.g., Totalentreprenør for Grunnarbeid)
3. **Supplier Agent 2** (e.g., Entreprenør for Fundamentering)
4. **Supplier Agent 3** (e.g., Entreprenør for Råbygg)

---

### 4.2 Owner Agent System Prompt Requirements

**Identity:**
- Name: e.g., "Kommunaldirektør Anne-Lise Berg"
- Role: Municipal project owner, budget approver
- Context: Responsible for ensuring school opens on time for August school start

**Negotiation Parameters:**
- **Budget:** Can approve increases IF user provides strong justification
  - Initial resistance: "Vi har allerede stramme rammer..."
  - Concession rate: Low (~3-5% increases max per round)
  - Requires good arguments: cost-benefit, risk mitigation, quality assurance
- **Time:** **ABSOLUTELY INFLEXIBLE**
  - Always responds: "Tidsfristen er ufravikelig. Skolen må stå klar til skolestart i august."
  - Even with perfect arguments, time cannot be extended

**Personality:**
- Professional, cautious, budget-conscious
- Balances municipal responsibility vs project success
- Sympathetic but firm on constraints

**Prompt Structure:**
```
You are Kommunaldirektør Anne-Lise Berg, representing the municipality...

CRITICAL RULES:
1. Time cannot be extended under ANY circumstances
2. Budget can be increased ONLY with exceptional justification
3. You must explain: "Samfunnskostnaden ved forsinkelse er høyere enn økt budsjett"

When user requests time extension:
- ALWAYS refuse politely but firmly
- Explain: School must open for August start
- Suggest: Find ways to reduce scope or accept higher cost for faster delivery

When user requests budget increase:
- Initially resistant
- Ask for detailed justification
- If argument strong → concede small increase (3-5%)
- If argument weak → suggest renegotiating with suppliers for lower cost
```

---

### 4.3 Supplier Agent System Prompt Requirements

**Agent Type 1: Can negotiate PRICE only**
- Can offer cheaper (lower quality)
- Can offer more expensive (higher capacity/overtime for faster delivery)
- **Cannot negotiate time independently**

**Agent Type 2: Can negotiate TIME (faster) for higher cost**
- Offers: "I can deliver faster, but it will require overtime → +X% cost"
- User must then negotiate with Owner if cost exceeds budget

**Agent Type 3: Can reduce SCOPE**
- Offers: "I can remove [feature] to reduce cost"
- Links to Owner perspective: scope changes require Owner approval

**Hidden Parameters (examples):**
- `initial_margin`: 1.15-1.30 (15-30% markup over baseline)
- `concession_rate`: 0.03-0.07 (3-7% price reduction per round)
- `patience`: 2-4 rounds before walking away
- `quality_flexibility`: boolean (can reduce quality for cost savings)

---

### 4.4 Supplier Persona Examples

**Supplier 1: Bjørn Eriksen (Totalentreprenør - Grunnarbeid)**
- Baseline: 105 MNOK, 60 days
- Personality: Skeptical, quality-focused
- Negotiation style: "Jeg kan ikke gå under 100 MNOK uten å redusere kvaliteten..."
- Can offer: Cheaper (90 MNOK, reduced quality) OR faster (95 MNOK, 45 days)

**Supplier 2: Kari Andersen (Fundamentering)**
- Baseline: 60 MNOK, 45 days
- Personality: Pragmatic, flexible
- Can offer: Scope reduction ("Vi kan bruke enklere fundamentering → 50 MNOK")

**Supplier 3: Per Johansen (Råbygg)**
- Baseline: 180 MNOK, 90 days
- Personality: Aggressive, profit-driven
- High margin: Starts at 200 MNOK
- Concession: Will reduce to 175 MNOK after strong negotiation

---

## 5. Supabase Database Integration

### 5.1 Overview

**Critical Architectural Change:**
The application now uses **Supabase** as the primary database and authentication provider, replacing the original localStorage-based approach.

**What Changed:**
- **OLD:** All data stored in browser localStorage (user credentials, game sessions, negotiation history)
- **NEW:** Supabase PostgreSQL database + Supabase Auth (JWT-based authentication)

**Why This Matters:**
- ✅ **Persistent storage** across devices and browser sessions
- ✅ **Secure authentication** with JWT tokens
- ✅ **Multi-user support** with proper user isolation
- ✅ **Data integrity** with relational database constraints
- ✅ **Scalability** for future features (leaderboards, multiplayer, etc.)

---

### 5.2 Backend Configuration (Already Implemented)

The backend folder already has Supabase fully configured:

**Files:**
1. **`backend/config.py`**
   - Loads Supabase credentials from `.env.local`
   - Environment variables: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`

2. **`backend/main.py`**
   - Supabase client initialized (line 14)
   - JWT authentication with JWKS validation (lines 26-98)
   - Protected endpoint `/me` returns current user (lines 127-133)
   - CORS configured for `localhost:3000`

3. **`backend/requirements.txt`**
   - Dependencies: `supabase`, `python-jose[cryptography]`, `fastapi`, `uvicorn`

4. **`backend/.env.example`**
   - Template for Supabase credentials

**Authentication Flow:**
1. User logs in via frontend → Supabase Auth
2. Supabase returns JWT token
3. Frontend stores JWT in memory (NOT localStorage for security)
4. Frontend sends JWT in Authorization header to backend
5. Backend validates JWT using JWKS from Supabase
6. Backend returns user data or protected resources

---

### 5.3 Frontend Configuration (Already Implemented)

The frontend folder already has Supabase libraries installed:

**Files:**
1. **`frontend/package.json`**
   - Dependencies: `@supabase/supabase-js`, `@supabase/ssr`

2. **`frontend/.env.local`** (configured)
   - Contains Supabase URL and Anon Key

**Required Frontend Implementation:**
- Supabase client initialization
- Auth state management (login, logout, session persistence)
- API calls with JWT token in headers
- Protected routes (redirect to login if not authenticated)

---

### 5.4 Database Schema Requirements

**Tables Needed:**

#### 1. `users` (Managed by Supabase Auth)
Automatically created by Supabase. Contains:
- `id` (UUID, primary key)
- `email` (unique)
- `encrypted_password`
- `created_at`, `updated_at`

#### 2. `game_sessions`
```sql
CREATE TABLE game_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_name VARCHAR(255),
  status VARCHAR(50) DEFAULT 'in_progress', -- 'in_progress', 'completed', 'failed'

  -- Budget tracking
  total_budget DECIMAL(10, 2) DEFAULT 700.00, -- MNOK
  locked_budget DECIMAL(10, 2) DEFAULT 650.00,
  available_budget DECIMAL(10, 2) DEFAULT 310.00,
  current_budget_used DECIMAL(10, 2) DEFAULT 0.00,

  -- Time tracking
  deadline_date DATE DEFAULT '2026-05-15',
  projected_completion_date DATE,

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);
```

#### 3. `wbs_commitments`
```sql
CREATE TABLE wbs_commitments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES game_sessions(id) ON DELETE CASCADE,
  wbs_id VARCHAR(50) NOT NULL, -- e.g., "1.3.1", "2.1"
  wbs_name VARCHAR(255),

  -- Commitment details
  supplier_agent_id VARCHAR(100), -- e.g., "bjorn_eriksen", "owner_anne_lise"
  committed_cost DECIMAL(10, 2),
  committed_duration_days INTEGER,
  committed_at TIMESTAMP DEFAULT NOW(),

  -- Negotiation metadata
  negotiation_rounds INTEGER DEFAULT 0,
  quality_reduced BOOLEAN DEFAULT false,
  scope_reduced BOOLEAN DEFAULT false,

  UNIQUE(session_id, wbs_id)
);
```

#### 4. `negotiation_history`
```sql
CREATE TABLE negotiation_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id UUID REFERENCES game_sessions(id) ON DELETE CASCADE,
  wbs_id VARCHAR(50),
  agent_id VARCHAR(100), -- e.g., "kari_andersen", "owner_anne_lise"
  agent_type VARCHAR(50), -- 'supplier' or 'owner'

  -- Message content
  user_message TEXT,
  agent_response TEXT,

  -- Offer details (if applicable)
  offer_cost DECIMAL(10, 2),
  offer_duration_days INTEGER,
  offer_accepted BOOLEAN DEFAULT false,

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

### 5.5 API Endpoints Required

**Authentication:**
- `POST /auth/signup` - Register new user (Supabase)
- `POST /auth/login` - Login (Supabase)
- `POST /auth/logout` - Logout (Supabase)
- `GET /auth/me` - Get current user (already implemented)

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

### 5.6 Security Considerations

**Row Level Security (RLS) Policies:**

Enable RLS on all tables to ensure users can only access their own data:

```sql
-- Game Sessions: Users can only see their own sessions
ALTER TABLE game_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own sessions"
  ON game_sessions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own sessions"
  ON game_sessions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own sessions"
  ON game_sessions FOR UPDATE
  USING (auth.uid() = user_id);

-- Similar policies for wbs_commitments and negotiation_history
```

**JWT Token Storage:**
- Store JWT in memory (React state or context)
- Optionally use httpOnly cookies for added security
- **Never** store JWT in localStorage (XSS vulnerability)

---

### 5.7 Migration from localStorage

**Impact on Existing Code:**
- Remove all `localStorage.getItem()` and `localStorage.setItem()` calls
- Replace with API calls to backend
- Update frontend state management to fetch from Supabase
- Update validation logic to check Supabase session data

**Data to Migrate:**
- Current plan state → `game_sessions` table
- WBS commitments → `wbs_commitments` table
- Negotiation chat logs → `negotiation_history` table
- User credentials → Supabase Auth (re-register users)

---

### 5.8 Implementation Priority

**Phase 1: Authentication (CRITICAL)**
1. Set up Supabase client in frontend
2. Create login/signup pages
3. Implement JWT token management
4. Protect routes with auth guards

**Phase 2: Game Sessions (HIGH)**
1. Create database tables (migrations)
2. Implement session CRUD endpoints
3. Update frontend to save/load from database
4. Test session persistence

**Phase 3: Negotiation History (MEDIUM)**
1. Create negotiation_history table
2. Store all AI chat messages in database
3. Implement chat history retrieval
4. Display past negotiations in UI

**Phase 4: Data Migration (LOW)**
1. Export existing localStorage data
2. Import into Supabase tables
3. Verify data integrity
4. Remove localStorage code

---

## 6. Consequences for Mockups and Repository

### 6.1 UI/UX Changes Required

**Dashboard:**
- Show **Owner perspective** prominently
- Budget display: "310 MNOK available for 3 packages | 650 MNOK locked"
- WBS list: Highlight 3 negotiable items, show 12 as "gray/contracted"

**Chat Interface:**
- Add ability to select negotiation partner: Supplier OR Owner
- Clear indication of who user is chatting with
- Offer acceptance: **MUST be active user choice (Yes/No buttons)**

**Critical Requirement:**
> "Det er viktig at brukergrensesnittet og dialogen med AI'en ikke automatisk aksepterer en avtale, det må være et aktivt valg som brukeren må få hver gang de får et tilbud – som da kan forhandles videre om eller aksepteres ved valg (ja/nei)."

**No Contract Signing:**
> "Ingen kontrakt skal inngås, så det elementet er out of scope."

---

### 5.2 Gantt Chart / Precedence Diagram Updates

**Gantt Chart:**
- Show all 15 WBS items
- Highlight 3 negotiable items in blue/interactive
- Show 12 locked items in gray (non-interactive)
- Display critical path (5 items total, 3 negotiable)

**Precedence Diagram:**
- Same logic: 3 nodes interactive, 12 grayed out
- Critical path highlighted in red
- Show dependencies clearly

---

### 5.3 New Mockup Files Needed

| Mockup File | Description | Key Changes |
|-------------|-------------|-------------|
| `nhb-08-screen-dashboard.svg` | Dashboard | Owner budget panel, 3 negotiable WBS highlighted |
| `nhb-09-screen-chat.svg` | Chat negotiation | Supplier/Owner toggle, Accept/Reject offer buttons |
| `nhb-10-screen-gantt-chart.svg` | Gantt chart | 3 of 5 critical path items interactive, 12 gray |
| `nhb-11-screen-precedence-diagram.svg` | Network diagram | Same as Gantt - 3 interactive, 12 locked |
| `nhb-16-modal-supplier-selection.svg` | Supplier selection | Show only 3 suppliers |
| `nhb-17-modal-commitment-confirm.svg` | Commitment confirmation | Add Accept/Reject buttons explicitly |
| `nhb-21-modal-owner-negotiation.svg` | **NEW:** Owner chat modal | Budget negotiation interface |

---

## 6. Implementation Checklist

### Phase 1: Documentation Updates

- [ ] Update `PRD.md`:
  - [ ] FR-3: WBS Management → 3 negotiable items only
  - [ ] FR-4: AI Supplier Negotiation → 4 agents (Owner + 3 suppliers)
  - [ ] FR-5: Budget model → 310 MNOK available, 650 locked
  - [ ] FR-6: Time constraint → Inflexible 15 months
  - [ ] FR-7: Negotiation types → 3 strategies documented

- [ ] Update `product-brief.md`:
  - [ ] Section 2: Solution Overview → 3 suppliers, 3 WBS
  - [ ] Section 4: MVP Scope → Scaled-down feature set
  - [ ] Section 6: Success Metrics → Updated for POC focus

- [ ] Update `ux-design-specification.md`:
  - [ ] Section 3.2: Dashboard → Owner budget panel
  - [ ] Section 3.3: Chat Page → Supplier/Owner selection
  - [ ] Section 3.4: Commitment Modal → Accept/Reject explicit buttons
  - [ ] Section 3.7: Gantt Chart → 3 interactive, 12 gray
  - [ ] Section 3.8: Precedence Diagram → Critical path highlighting

- [ ] Update `epics.md`:
  - [ ] Epic 3: WBS Management → 3 items only
  - [ ] Epic 4: AI Supplier Negotiation → 4 agent roles
  - [ ] Epic 5: Plan Management → Owner negotiation stories
  - [ ] New stories: E4.7 Owner AI Agent, E5.6 Budget Negotiation Flow

- [ ] Create `AI_AGENT_SYSTEM_PROMPTS.md`:
  - [ ] Owner agent prompt (full specification)
  - [ ] Supplier 1 prompt (price negotiation)
  - [ ] Supplier 2 prompt (time/cost trade-off)
  - [ ] Supplier 3 prompt (scope reduction)

---

### Phase 2: Static Data Updates

- [ ] Update `/public/data/wbs.json`:
  - [ ] Mark 3 items as `negotiable: true`
  - [ ] Mark 12 items as `negotiable: false, status: "contracted"`
  - [ ] Update baseline costs: 105, 60, 180 MNOK for negotiable items

- [ ] Update `/public/data/suppliers.json`:
  - [ ] Remove 2 suppliers (keep 3 only)
  - [ ] Add `owner` entry for Owner AI agent
  - [ ] Update negotiation parameters (margin, concession_rate, patience)

- [ ] Create `/public/data/budget_model.json`:
  - [ ] Total: 700 MNOK
  - [ ] Locked: 650 MNOK
  - [ ] Available: 310 MNOK
  - [ ] Baseline_needed: 345 MNOK
  - [ ] Deficit: 35 MNOK

---

### Phase 3: Mockup Creation

- [ ] `nhb-01-flow-complete-user-journey.svg` - Updated user flow with Owner negotiation
- [ ] `nhb-02-flow-authentication.svg` - No changes
- [ ] `nhb-03-flow-negotiation-strategy.svg` - **NEW:** 3 negotiation types diagram
- [ ] `nhb-07-screen-login.svg` - No changes
- [ ] `nhb-08-screen-dashboard.svg` - **UPDATED:** Owner panel, 3 WBS highlighted
- [ ] `nhb-09-screen-chat.svg` - **UPDATED:** Supplier/Owner toggle, Accept/Reject
- [ ] `nhb-10-screen-gantt-chart.svg` - **UPDATED:** 3 interactive, 12 gray
- [ ] `nhb-11-screen-precedence-diagram.svg` - **UPDATED:** Critical path (3 of 5)
- [ ] `nhb-12-screen-history-timeline.svg` - Minor updates
- [ ] `nhb-13-component-wbs-card.svg` - Show negotiable vs locked status
- [ ] `nhb-14-component-navigation.svg` - No changes
- [ ] `nhb-15-screen-registration.svg` - No changes
- [ ] `nhb-16-modal-supplier-selection.svg` - **UPDATED:** 3 suppliers only
- [ ] `nhb-17-modal-commitment-confirm.svg` - **UPDATED:** Accept/Reject buttons
- [ ] `nhb-18-modal-help-onboarding.svg` - Update help text
- [ ] `nhb-19-modal-success.svg` - No changes
- [ ] `nhb-20-modal-error-validation.svg` - No changes
- [ ] `nhb-21-modal-owner-negotiation.svg` - **NEW:** Owner chat interface

---

### Phase 4: Verification & Testing

- [ ] **Documentation consistency check:**
  - [ ] All docs reference 3 suppliers, 3 WBS
  - [ ] Budget model consistent across all files (310/650/700)
  - [ ] Time constraint documented as inflexible
  - [ ] Owner role clearly defined

- [ ] **Mockup design review:**
  - [ ] Fonts compatible across systems (use web-safe fonts)
  - [ ] Colors consistent with design system
  - [ ] SVG files optimized (<500 KB each)
  - [ ] Norwegian language throughout

- [ ] **AI prompt validation:**
  - [ ] Owner prompt rejects time extensions 100%
  - [ ] Supplier prompts follow negotiation types
  - [ ] Hidden parameters tested (margin, concession rates)

---

## 7. File-by-File Update Plan

### Documentation Files (Markdown)

| File Path | Priority | Changes Required | Estimated Time |
|-----------|----------|------------------|----------------|
| `docs/PRD.md` | **HIGH** | Rewrite FR-3, FR-4, FR-5, FR-6, FR-7 | 2-3 hours |
| `docs/product-brief.md` | **HIGH** | Update Sections 2, 4, 6 | 1-2 hours |
| `docs/ux-design-specification.md` | **HIGH** | Update Sections 3.2-3.8 | 2-3 hours |
| `docs/epics.md` | **HIGH** | Rewrite Epic 3, 4, 5; add stories | 2-3 hours |
| `docs/brainstorming-*.md` | **MEDIUM** | Update for 3 WBS scope | 1 hour |
| `docs/validation-report-*.md` | **LOW** | Re-run validation if needed | 30 min |

**Total Documentation Time:** ~10-15 hours

---

### Static Data Files (JSON)

| File Path | Priority | Changes Required | Estimated Time |
|-----------|----------|------------------|----------------|
| `/public/data/wbs.json` | **HIGH** | Add `negotiable` flag, update costs | 30 min |
| `/public/data/suppliers.json` | **HIGH** | Remove 2, add Owner entry | 30 min |
| `/public/data/budget_model.json` | **HIGH** | Create new file | 15 min |
| `/backend/prompts/owner.md` | **CRITICAL** | Write Owner system prompt | 2 hours |
| `/backend/prompts/supplier_1.md` | **CRITICAL** | Update for price negotiation | 1 hour |
| `/backend/prompts/supplier_2.md` | **CRITICAL** | Update for time/cost trade-off | 1 hour |
| `/backend/prompts/supplier_3.md` | **CRITICAL** | Update for scope reduction | 1 hour |

**Total Data/Prompt Time:** ~6-7 hours

---

### Mockup Files (SVG)

| File Path | Priority | Changes Required | Estimated Time |
|-----------|----------|------------------|----------------|
| `docs/ux/nhb-01-flow-complete-user-journey.svg` | **HIGH** | Add Owner negotiation flow | 1-2 hours |
| `docs/ux/nhb-03-flow-negotiation-strategy.svg` | **HIGH** | Create new diagram | 1-2 hours |
| `docs/ux/nhb-08-screen-dashboard.svg` | **CRITICAL** | Owner panel, 3 WBS highlight | 2-3 hours |
| `docs/ux/nhb-09-screen-chat.svg` | **CRITICAL** | Supplier/Owner toggle | 2-3 hours |
| `docs/ux/nhb-10-screen-gantt-chart.svg` | **HIGH** | 3 interactive, 12 gray | 2-3 hours |
| `docs/ux/nhb-11-screen-precedence-diagram.svg` | **HIGH** | Critical path (3 of 5) | 2-3 hours |
| `docs/ux/nhb-13-component-wbs-card.svg` | **MEDIUM** | Negotiable status badge | 1 hour |
| `docs/ux/nhb-16-modal-supplier-selection.svg` | **HIGH** | 3 suppliers only | 1-2 hours |
| `docs/ux/nhb-17-modal-commitment-confirm.svg` | **HIGH** | Accept/Reject buttons | 1-2 hours |
| `docs/ux/nhb-21-modal-owner-negotiation.svg` | **CRITICAL** | Create new mockup | 2-3 hours |

**Total Mockup Time:** ~16-24 hours

---

### **GRAND TOTAL ESTIMATED TIME:** ~32-46 hours (4-6 days of focused work)

---

## 8. Critical Questions for Clarification

Before starting implementation, confirm these details:

1. **Which 3 WBS items are negotiable?**
   - Suggested: 1.3.1 Grunnarbeid, 1.3.2 Fundamentering, 1.4.1 Råbygg
   - Confirm these are 3 of the 5 on critical path

2. **Exact budget breakdown:**
   - Locked: 650 MNOK or 655 MNOK? (depends on whether 50 MNOK or 45 MNOK available)
   - Available: 310 MNOK confirmed?

3. **Supplier personas:**
   - Can we reuse Bjørn, Kari, Per from original? Or create new ones?
   - Suggested names for Owner: "Kommunaldirektør Anne-Lise Berg" or similar?

4. **Mockup design style:**
   - Follow existing nhb-* mockup visual style exactly?
   - Color scheme for "negotiable" vs "locked" items?

5. **System prompt testing:**
   - How many test negotiations required per agent before approval?
   - Suggested: 10 samples per agent (40 total tests)

---

## 9. References

**Source Document:**
- PDF: "Nytt scope og nødvendige endringer.pdf" (4 pages)
- Date: 2025-12-11
- Author: [Stakeholder: Bård]

**Key Quotes:**
1. "Vi går fra 15 → 3 leverandører og 3 WBS-arbeidspakker det kan forhandles om."
2. "Tiden kan ikke forlenges, selv om dette bare skal komme frem gjennom dialog med AI-agenten."
3. "Det er viktig at brukergrensesnittet og dialogen med AI'en ikke automatisk aksepterer en avtale."
4. "Ingen kontrakt skal inngås, så det elementet er out of scope."
5. "De tre kritiske pakkene i simuleringen bare har 310 MNOK tilgjengelig (dvs. 45 MNOK under anslaget)."

---

**End of Task Reference Document**

**Next Steps:**
1. Review this document with stakeholders
2. Confirm 3 WBS items and supplier personas
3. Begin Phase 1: Documentation updates
4. Proceed to Phase 2-4 based on priority

**Status:** Ready for implementation - all tasks documented and prioritized.