# Project Plan

## Instructions

1.  Where you see {prompt / user-input-file}, you can add your own prompt or filename to provide extra instructions. If you don't wish to add anything, you can remove this part.
2.  If a prompt is already written, e.g., "Root Cause Analysis...", feel free to replace it with your own.

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
- [x] **WBS Source Data**
    - *File: `docs/data/wbs.pdf`*
    - *Description: Complete Work Breakdown Structure with all 70+ work packages including IDs, names, responsibilities, durations, start/end dates, dependencies, deliverables, and cost estimates (totaling 700 MNOK). Source data ready for conversion to JSON.*

---

## Phase 3: Implementation

### Sprint 1 - Foundation & Infrastructure (Week 1)

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

- [ ] **Static Data Files (JSON conversion)**
    - *Status: WBS PDF exists, but wbs.json and agents.json NOT YET CREATED.*
    - *Description: Need to extract data from wbs.pdf (70+ WBS items) and AI_AGENT_SYSTEM_PROMPTS.md (4 agents) into structured JSON files. Target: frontend/public/data/wbs.json (15 items: 3 negotiable + 12 locked with 310/390 MNOK split) and agents.json (4 agent configs).*

- [ ] **Database Schema Creation**
    - *Status: SQL migration written in API_DATABASE_INTEGRATION_GUIDE.md but NOT YET RUN.*
    - *Description: Need to execute SQL migration to create 4 tables: game_sessions, wbs_commitments, negotiation_history, user_analytics. Includes RLS policies, indexes, triggers.*

- [ ] **Backend API Endpoints**
    - *Status: Only `/` and `/me` endpoints exist. Gemini service NOT CREATED.*
    - *Description: Need to implement: backend/services/gemini_service.py, POST /api/chat, GET/POST/PUT /api/sessions, POST /api/sessions/{id}/commitments, GET /api/sessions/{id}/history.*

**Sprint 1 Progress:** 7/10 tasks complete (70%). Blocked on JSON conversion and database setup.

---

### Sprint 2-5 - Core Features (Weeks 2-5) - **NOT STARTED**

- [ ] **Dashboard & Budget Tracking** (Week 2)
    - *Description: Dashboard UI with constraint panel (310/390/700 MNOK budget display), WBS list component (3 negotiable highlighted + 12 locked grayed), real-time budget/timeline updates, status indicators (pending/completed).*

- [ ] **AI Negotiation System** (Week 3)
    - *Description: Gemini service integration using prompts from AI_AGENT_SYSTEM_PROMPTS.md, POST /api/chat endpoint with context injection, offer detection/parsing, negotiation history persistence to database, explicit accept/reject buttons on offers.*

- [ ] **Plan Management & Validation** (Week 3-4)
    - *Description: Commitment flow with modal confirmations, renegotiation (uncommit) functionality, dependency validation against WBS structure, plan validation (budget ≤700 MNOK, timeline ≤May 15 2026), success/error modals with actionable feedback.*

- [ ] **Visualization Features** (Week 4-5)
    - *Description: Gantt chart React component (based on docs/ux/functional_flows/visualization-01-gantt-chart.svg design), precedence diagram AON network (based on visualization-02-precedence-diagram.svg), history/timeline view, tabbed navigation between views.*

- [ ] **Export & Polish** (Week 5)
    - *Description: Session export as JSON via GET /api/sessions/{id}/export, session management dashboard, help documentation modal, integration testing with Playwright, bug fixes and UI polish.*

**Current Progress:** Sprint 1 foundation 70% complete. Core features blocked on database and backend API implementation.

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
- **Phase 3 (Implementation):** 🔄 ~25% Complete (7/10 Sprint 1 tasks, 0/5 Sprint 2-5 themes)
- **Phase 4 (Testing):** ⏸️ Not Started (0/6 test categories)
- **Phase 5 (Deployment):** ⏸️ Not Started (0/4 deployment tasks)

**Key Achievements:**
- ✅ All 4 AI agent prompts fully documented (682 lines with test scenarios)
- ✅ Complete WBS source data (70+ packages, 700 MNOK total)
- ✅ All UX flows designed (7 functional flows + 2 visualizations)
- ✅ Auth system fully functional
- ✅ Chat UI implemented (awaiting backend integration)
- ✅ Prompts viewer page live

**Critical Blockers:**
1. 🚨 **JSON data extraction** - Convert wbs.pdf + AI_AGENT_SYSTEM_PROMPTS.md → wbs.json + agents.json (2-3 hours manual work)
2. 🚨 **Database schema** - Run SQL migration from API_DATABASE_INTEGRATION_GUIDE.md (30 minutes)
3. 🚨 **Backend API** - Implement Gemini service + 5 core endpoints (12-16 hours development)

**Next Actions:**
1. Extract WBS data from PDF → create wbs.json (15 items: 3 negotiable + 12 locked)
2. Extract agent configs from prompts doc → create agents.json (4 agents)
3. Run database migration in Supabase
4. Implement backend/services/gemini_service.py
5. Implement POST /api/chat endpoint
6. Build Dashboard UI (constraint panel + WBS list)

**Estimated time to unblock Sprint 2:** 15-20 hours of focused development work.

---

## BMAD Workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">
