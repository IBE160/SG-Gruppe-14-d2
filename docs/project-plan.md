# Project Plan

## Instructions

1.  Where you see {prompt / user-input-file}, you can add your own prompt or filename to provide extra instructions. If you don't wish to add anything, you can remove this part.
2.  If a prompt is already written, e.g., "Root Cause Analysis...", feel free to replace it with your own.

---

## 📊 Executive Summary (Updated: December 16, 2025)

### Project Status: **POC FUNCTIONAL - 75% COMPLETE** ✅

The PM Simulator project has successfully implemented core functionality and is ready for **classroom demonstrations** and **proof-of-concept testing**. The application features a working AI-powered negotiation system, full authentication, budget tracking, and data persistence.

### What's Working ✅

**Complete & Operational:**
1. ✅ **User Authentication** - Full Supabase auth with email/password, registration, login, password reset
2. ✅ **Dashboard** - 3-tier budget visualization (310/390/700 MNOK), WBS package listing, agent panels
3. ✅ **AI Negotiation** - Real-time chat with 4 AI agents using Gemini 2.5 Flash, context-aware responses
4. ✅ **Offer Management** - Automatic offer detection, accept/reject buttons, budget impact preview
5. ✅ **Budget Tracking** - Real-time updates, validation (≤700 MNOK), duplicate prevention
6. ✅ **Data Persistence** - Sessions, commitments, and negotiation history saved to database
7. ✅ **Backend API** - 10 RESTful endpoints, JWT auth, RLS-compliant database access
8. ✅ **Design System** - Professional UI with Tailwind CSS, Shadcn components, color-coded budget tiers
9. ✅ **Static Data** - Complete WBS (15 items) and agent configs (4 agents) in JSON format
10. ✅ **Documentation** - 40+ comprehensive docs (PRD, architecture, test plans, troubleshooting)

### What's Missing ❌

**Critical for MVP:**
1. ⚠️ **Session Completion Flow** - No results page or completion summary (est: 4-6 hours)
2. ⚠️ **Chat History Loading** - Messages reset on page refresh (est: 2 hours)
3. ⚠️ **Database Import Verification** - Need to confirm schema imported to Supabase production

**Important but Not Blocking:**
4. ❌ **Renegotiation** - Cannot uncommit accepted offers (est: 3-4 hours)
5. ❌ **Timeline/Dependency Validation** - No deadline or critical path checks (est: 4-6 hours)
6. ❌ **Agent Timeout UI** - No visual countdown for 6-disagreement limit (est: 3 hours)
7. ❌ **Visualizations** - Gantt chart and precedence diagram designs exist but not coded (est: 6-8 hours using gantt-task-react + ReactFlow libraries)
8. ❌ **Export** - No session export to JSON/PDF (est: 4-6 hours)
9. ⚠️ **Mobile Responsive** - Desktop-optimized, limited mobile support (est: 8-12 hours)
10. ❌ **Automated Tests** - No unit/integration/E2E test suite (est: 40+ hours)

### File Statistics
- **Frontend:** ~150 source files, ~8,000+ lines of TypeScript/TSX
- **Backend:** ~10 Python files, ~1,200+ lines of code
- **Database:** 5 tables, 627-line migration script with RLS policies
- **Documentation:** 40+ markdown files, 18 SVG diagrams
- **Data Files:** 2 JSON files (15 WBS items, 4 agent configs)

### Recommended Next Steps
1. **Week 1:** Verify database import, implement session completion flow, add chat history loading
2. **Week 2:** Add renegotiation, timeline validation, agent timeout UI
3. **Week 3:** Build visualizations using gantt-task-react (Gantt chart) and ReactFlow (precedence diagram)
4. **Week 4:** Add export, improve mobile responsiveness, write automated tests
5. **Week 5:** Production deployment, pilot testing with LOG565 class

### Timeline to MVP: 20-30 hours
### Timeline to Full POC: 40-55 hours

---

## Phase 0: Discovery & Analysis

- [x] **/run-agent-task analyst *workflow-init**
    - *File: `bmm-workflow-status.yaml`*
    - *Status: Done. Initialized the project workflow tracking.*

- **Brainstorming (Completed)**
    - [x] **/run-agent-task analyst *brainstorm "Initial project ideas and scope"**
        - *File: `brainstorming-session-results-2025-12-02.md`*
        - *Defines: General ideas for the project.*
    - [x] **/run-agent-task analyst *brainstorm "User interaction models"**
        - *File: `brainstorming-session-results-user-interactions-2025-12-02.md`*
        - *Defines: Initial concepts for how users will interact with the simulation.*
    - [x] **/run-agent-task analyst *brainstorm "Risk and monitoring strategies"**
        - *File: `brainstorming-session-results-risk-and-monitoring-2025-12-02.md`*
        - *Defines: Potential risks and how to monitor them.*
    - [x] **/run-agent-task architect *brainstorm "Technical Architecture"**
        - *File: `brainstorming-technical-architecture-report.md`*
        - *Defines: The core technology stack (React, FastAPI, SQLite).*

- **Brainstorming (Completed)**
    - [x] **/run-agent-task analyst *brainstorm "Audience and Core Value"**
        - *File: `brainstorming-session-audience-and-core-value-2025-12-07.md`*
        - *Defines: User Personas (Sara, Magnus, Prof. Eriksen, Ingrid), Value Proposition, Success Metrics, Jobs-to-be-Done.*
    - [x] **/run-agent-task analyst *brainstorm "Core Functionality and Scope"**
        - *File: `brainstorming-session-core-functionality-and-scope-2025-12-07.md`*
        - *Defines: MVP features (15 Must-Haves), Simplified Architecture (localStorage + Supabase Auth), Data Flow, localStorage Schema, 3-4 week timeline.*

- [x] **Research**
    - [x] /run-agent-task analyst *research*
        - *File: `research-report-2025-12-07.md`*
        - *Description: Comprehensive research on 3 topics: (1) AI prompt engineering for negotiation agents (2025 best practices, context engineering, tight personas), (2) localStorage limits and offline-first patterns (5-10 MB validated, storage monitoring recommended), (3) Competitive analysis of PM simulation tools (MIT Sloan, Cesim, SimProject, GoVenture—all focus on execution, not planning). Key finding: Our AI negotiation + planning focus + Norwegian context creates unique market position.*

- [x] **Product Brief**
    - [x] /run-agent-task analyst *product-brief*
        - *File: `product-brief.md`*
        - *Description: Concise 2-3 page stakeholder-facing brief synthesizing proposal, brainstorming, PRD, and research. Sections: Vision & Problem, Solution, Target Users (Sara, Magnus, Prof. Eriksen), MVP Scope (15 Must-Haves), Timeline (3-4 weeks), Success Metrics, Unique Value Proposition (vs competitors), Risk Mitigation. Ready for stakeholder approval.*

---

## Phase 1: Planning

- [x] **/run-agent-task pm *prd**
    - *File: `PRD.md`*
    - *Description: Complete Product Requirements Document with 14 sections, 35+ functional requirements, 30+ user stories, technical specs. Updated to v2.0 for POC scope (3 negotiable WBS + 4 AI agents, 310/390/700 MNOK budget model, inflexible time constraint).*
- [x] **/run-agent-task pm *validate-prd**
    - *File: `validation-report-PRD-2025-12-07.md`*
    - *Description: Comprehensive validation checklist with 111 review items across completeness, clarity, consistency, feasibility, alignment, user-centricity, and actionability. Result: 97% pass rate (34/35 items passed).*
- [x] **/run-agent-task ux-designer *create-ux-design**
    - *File: `ux-design-specification.md`*
    - *Description: Complete UX Design Specification with 9 sections: Design Principles, Visual Design System (colors, typography, spacing), Wireframes (Login, Dashboard, Chat, Modals), User Flows (3 detailed flows), Component Specifications (5 components with TSX code), Interaction Patterns, Responsive Design (desktop + tablet), Accessibility (WCAG 2.1 Level A), Implementation Notes (Tailwind, Shadcn, Norwegian strings). Updated to v2.0 for POC scope.*
- [x] **/run-agent-task ux-designer *validate-ux-design**
    - *File: `validation-report-UX-Design-2025-12-07.md`*
    - *Description: UX Design validation with 90+ review items across Visual Design System, Wireframes, User Flows, Components, Interactions, Responsive Design, Accessibility, Implementation Readiness, PRD Alignment. Result: 96% pass rate (119.5/124 items), APPROVED for implementation.*

---

## Phase 2: Solutioning

- [x] **/run-agent-task architect *create-architecture**
    - *File: `architecture.md` (Note: Key decisions captured in `brainstorming-technical-architecture-report.md`)*
    - *Description: Technical architecture validated through research. Stack: React + TypeScript + Tailwind CSS + Shadcn UI (frontend), FastAPI (backend), Supabase PostgreSQL (storage + auth), Gemini 2.5 Flash (AI), Vercel (hosting). Architecture updated to support database-backed sessions for multi-device capability.*
- [x] **/run-agent-task pm *create-epics-and-stories**
    - *File: `epics.md`*
    - *Description: 10 epics broken into 42 user stories totaling 125 story points. Updated to v2.0 for POC scope: 3 negotiable + 12 locked WBS, 4 AI agents (Owner + 3 suppliers), explicit accept/reject flow, budget display (310/390/700). Sprint plan defined for 4-5 weeks. Includes acceptance criteria, technical notes, and traceability to PRD.*
- [x] **/run-agent-task tea *test-design**
    - *File: `test-design.md`*
    - *Description: Comprehensive test strategy with 60%+ coverage target. Includes unit tests (Vitest), integration tests (React Testing Library), E2E tests (Playwright), AI quality testing (50 scenarios), UAT plan (5-10 students), performance testing (Lighthouse), accessibility testing (WCAG 2.1 Level A), security testing. 90+ test cases defined across 8 epics.*
- [x] **/run-agent-task architect *solutioning-gate-check**
    - *File: `solutioning-gate-check.md`*
    - *Description: Final readiness assessment before Phase 3. Result: ✅ GO (Approved to proceed). Documentation 100% complete (Phase 0, 1, 2), architecture validated, 7/7 decision criteria met, medium risk level with mitigation strategies, 90% confidence in 3-4 week delivery. 4 non-critical blockers identified, all resolvable Week 1-2.*
- [x] **API & Database Integration Guide**
    - *File: `API_DATABASE_INTEGRATION_GUIDE.md`*
    - *Description: Comprehensive 2000+ line guide for Gemini API and Supabase PostgreSQL integration. Covers database schema (4 tables), backend API endpoints (11 endpoints), frontend integration patterns, security best practices, complete SQL migrations and code examples.*
- [x] **UX Functional Flows & Visualizations**
    - *Files: `docs/ux/functional_flows/` (7 flow diagrams + 2 visualizations)*
    - *Description: Complete functional flow diagrams (validation rules, budget calculation, AI negotiation, commitment flow, state management, error handling, critical path/timeline) and visualization designs (Gantt chart, precedence diagram). 10 SVG files total.*
    - *Implementation Note: Visualizations will be built using gantt-task-react (Gantt) and ReactFlow (Precedence) libraries, configured to match the designs. See `docs/Precedence-And-Gantt.md` for implementation guide.*
- [x] **WBS Source Data**
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

- [x] **Supabase Authentication Setup**
    - *Files: `backend/config.py`, `backend/main.py`, `frontend/lib/supabase/`*
    - *Description: Supabase project configured (cmntglldaqrekloixxoc.supabase.co). Email auth enabled. JWT validation with JWKS implemented. Frontend SSR auth library integrated. Environment variables configured.*

- [x] **User Registration & Login**
    - *Files: `frontend/app/auth/`, `frontend/components/sign-up-form.tsx`, `frontend/components/login-form.tsx`*
    - *Description: Complete auth flows with email/password. Registration, login, forgot password, update password pages. Error handling, loading states, redirects to protected pages implemented.*

- [x] **Chat Interface UI (Basic)**
    - *Files: `frontend/components/chat-interface.tsx`, `frontend/app/chat/chat-page-client.tsx`, `frontend/app/chat/page.tsx`*
    - *Description: Chat UI with message display (user/agent bubbles), textarea input, send button, agent selection screen. Scrollable chat window with auto-scroll. Loading states with typing indicator. Simulated responses (not yet connected to backend AI).*

- [x] **AI Agent System Prompts (All 4 Agents)**
    - *File: `docs/AI_AGENT_SYSTEM_PROMPTS.md` (682 lines)*
    - *Description: Complete system prompts for all 4 AI agents with detailed personas, negotiation parameters, and behavioral rules. Owner: Anne-Lise Berg (Municipality - budget approval, NO time extensions). Supplier 1: Bjørn Eriksen (Price/quality negotiation). Supplier 2: Kari Andersen (Time/cost tradeoffs). Supplier 3: Per Johansen (Scope reduction). Includes testing guidelines and 10+ test scenarios per agent.*

- [x] **Prompts Viewer Page**
    - *File: `frontend/app/prompts/page.tsx`*
    - *Description: Server-side page that reads and displays AI_AGENT_SYSTEM_PROMPTS.md as formatted markdown. Uses ReactMarkdown with GitHub-flavored markdown support. Accessible at /prompts with navigation link from homepage.*

- [x] **Backend Dependencies Installation**
    - *File: `backend/requirements.txt`*
    - *Description: All required packages installed including FastAPI, Supabase, python-jose, pydantic-settings, google-generativeai (Gemini API), uvicorn. Ready for implementation.*

- [x] **Static Data Files (JSON conversion)**
    - *Status: COMPLETE. Both wbs.json and agents.json created and deployed.*
    - *Files: `frontend/public/data/wbs.json` (15 WBS items: 3 negotiable + 12 locked, 310/390/700 MNOK structure) and `frontend/public/data/agents.json` (4 AI agents with full configurations).*
    - *Description: WBS data extracted from wbs.pdf with complete metadata (budget, dependencies, critical path, suppliers). Agent configs extracted from AI_AGENT_SYSTEM_PROMPTS.md with capabilities, negotiation styles, and cost multipliers.*

- [x] **Database Schema Creation**
    - *Status: COMPLETE. All SQL migrations written and ready for import.*
    - *Files: `database/migrations/001_complete_schema.sql` (627 lines), `IMPORT_TO_SUPABASE.md` (import guide).*
    - *Description: 5 tables created (game_sessions, wbs_commitments, negotiation_history, agent_timeouts, user_analytics). Includes RLS policies, indexes, triggers, computed columns. Import guide provided.*
    - *⚠️ Verification Needed: Confirm schema has been imported to Supabase production instance.*

- [x] **Backend API Endpoints**
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

- [x] **Dashboard & Budget Tracking** (Week 2) - ✅ COMPLETE
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

- [x] **AI Negotiation System** (Week 3) - ✅ COMPLETE
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

- [x] **Plan Management & Validation** (Week 3-4) - ⚠️ PARTIALLY COMPLETE
    - *Status: Core commitment flow implemented, some advanced features missing.*
    - *Files: `backend/main.py` (commitments endpoints), `frontend/components/chat-interface.tsx` (offer acceptance)*
    - *Features Implemented:*
        - ✅ Commitment flow with offer acceptance
        - ✅ Budget validation (≤700 MNOK total, ≤310 MNOK available)
        - ✅ Duplicate commitment prevention
        - ✅ Database persistence via POST /api/sessions/{id}/commitments
        - ✅ Session budget updates
        - ✅ Error handling with user feedback
    - *Missing Features:*
        - ❌ Renegotiation (uncommit) functionality
        - ❌ Dependency validation against WBS structure
        - ❌ Timeline validation (deadline ≤May 15 2026)
        - ❌ Modal confirmations for commitments
        - ❌ Session completion flow

- [ ] **Visualization Features** (Week 4-5) - ❌ NOT IMPLEMENTED
    - *Status: Design files exist, library-based implementation planned.*
    - *Available Designs: `docs/ux/functional_flows/visualization-01-gantt-chart.svg`, `visualization-02-precedence-diagram.svg`*
    - *Implementation Approach:*
        - **Gantt Chart:** Using `gantt-task-react` library (30K+ weekly downloads)
          - Pre-built timeline rendering with Month/Week/Day view modes
          - Configured for Feb 2025 - May 2026 timeline
          - Color scheme: Red (critical path), Green (negotiable), Gray (locked)
        - **Precedence Diagram:** Using `ReactFlow` library (500K+ weekly downloads)
          - Purpose-built for Activity-on-Node (AON) network diagrams
          - Auto-layout, zoom, pan, drag interactions built-in
          - Node display: WBS ID, name, duration, ES/EF/LS/LF, slack time
        - See `docs/Precedence-And-Gantt.md` for complete implementation guide
    - *Missing Features:*
        - ❌ Gantt chart React component with gantt-task-react integration
        - ❌ Precedence diagram AON network with ReactFlow integration
        - ❌ History/timeline view
        - ❌ Tabbed navigation between views
    - *Estimated Effort: 6-8 hours (reduced from 16-24 hours with library approach)*

- [x] **Export & Polish** (Week 5) - ⚠️ PARTIALLY COMPLETE
    - *Status: Some polish complete, export missing.*
    - *Features Implemented:*
        - ✅ Session management (create/retrieve/update)
        - ✅ Design system with comprehensive color palette
        - ✅ Error handling and loading states
        - ✅ Responsive UI components (Tailwind + Shadcn)
        - ✅ Testing scripts (backend/test_chat.py, test_setup.py, etc.)
        - ✅ Troubleshooting documentation (TROUBLESHOOTING_REPORT_DEC_16.md)
    - *Missing Features:*
        - ❌ Session export as JSON/PDF
        - ❌ Help documentation modal in UI
        - ❌ Integration testing with Playwright
        - ❌ Agent timeout UI countdown
        - ❌ Session completion page

**Current Progress:** Sprint 2-3 features ~85% complete. Sprint 4-5 features ~40% complete. Core negotiation loop fully functional.

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
- **Phase 3 (Implementation):** ✅ ~75% Complete (10/10 Sprint 1 tasks, 3.5/5 Sprint 2-5 themes)
- **Phase 4 (Testing):** ⏸️ Not Started (0/6 test categories)
- **Phase 5 (Deployment):** ⏸️ Not Started (0/4 deployment tasks)

**Key Achievements:**
- ✅ Sprint 1 foundation 100% complete
- ✅ All 4 AI agent prompts fully documented (682 lines) and integrated with Gemini API
- ✅ Complete WBS and agent data files (wbs.json, agents.json)
- ✅ Database schema created (5 tables, RLS policies, triggers) - awaiting import verification
- ✅ Backend API fully operational (10 endpoints, Gemini service, auth)
- ✅ Dashboard with 3-tier budget visualization
- ✅ Full AI negotiation loop (chat, offer detection, accept/reject, persistence)
- ✅ Auth system fully functional
- ✅ Design system with comprehensive color palette
- ✅ 40+ documentation files

**Remaining Gaps (MVP Completion):**
1. ⚠️ **Session Completion Flow** - No completion page or results summary (4-6 hours)
2. ⚠️ **Chat History Loading** - Messages not loaded from DB on page refresh (2 hours)
3. ⚠️ **Database Import Verification** - Confirm schema imported to Supabase production (30 minutes)
4. ❌ **Renegotiation (Uncommit)** - Cannot undo commitments (3-4 hours)
5. ❌ **Timeline/Dependency Validation** - No deadline or critical path checks (4-6 hours)
6. ❌ **Visualizations** - Gantt chart and precedence diagram not built (6-8 hours using gantt-task-react + ReactFlow)
7. ❌ **Export Functionality** - No session export to JSON/PDF (3-4 hours)
8. ❌ **Automated Testing** - No unit/integration/E2E test suite (8-10 hours)

**Nice to Have (If Time Permits):**
9. ⏸️ **Agent Timeout UI** - Visual countdown for 6-disagreement timeout (3 hours)
10. ⏸️ **Mobile Responsiveness** - Desktop-first, limited mobile support (8-12 hours)
11. ⏸️ **Help Documentation Modal** - In-app help system (1-2 hours)

**Next Priority Actions (MVP Completion):**
1. Verify database schema import in Supabase production instance
2. Implement session completion flow (`/app/complete/page.tsx` + API endpoint)
3. Add chat history loading from `negotiation_history` table
4. Implement uncommit functionality for renegotiation
5. Add timeline/dependency validation (critical path algorithm)
6. Build Gantt chart (gantt-task-react) and precedence diagram (ReactFlow) visualizations
7. Implement session export functionality
8. Write automated test suite (backend + frontend)

**Estimated time to MVP (required features only):** 29-38 hours of focused development work.
**Estimated time with nice-to-have features:** 40-53 hours.

**Recommended approach:** Team of 2-3 developers working in parallel (see `MVP_COMPLETION_ROADMAP_REVISED.md`)

---

## BMAD Workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">
