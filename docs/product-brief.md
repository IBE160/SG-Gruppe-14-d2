# Product Brief
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 1.0
**Date:** 2025-12-07
**Status:** Final
**Project Phase:** Phase 0 Complete, Ready for Solutioning

---

## Executive Overview

**Nye Hædda Barneskole** is an AI-powered project management simulation that teaches university students the critical planning phase of construction projects through realistic negotiation with AI supplier personas. The MVP will be delivered in **4-5 weeks** with a focus on Norwegian university students learning procurement, constraint balancing, and negotiation skills.

**Key Differentiators:**
- ✅ **Only PM simulation focused on PLANNING** (vs execution)
- ✅ **AI-powered negotiation** with 5 realistic supplier personas
- ✅ **Norwegian language** and construction context
- ✅ **45-60 minute experience** (fits within single lecture)

**Market Opportunity:** Norwegian universities (NTNU, UiO, UiB, HiOA) teaching PM courses to ~500-1,000 students annually. Potential expansion to Nordic region and other industries.

---

## 1. Vision & Problem Statement

### Vision
Create an immersive learning environment where students experience the complexities of project planning—navigating budget constraints, tight deadlines, and realistic supplier negotiations—without real-world consequences.

### Problem
Current project management education focuses heavily on execution and monitoring, but **neglects the critical planning phase** where projects succeed or fail. Students graduate with theoretical knowledge but lack practical experience in:
- Procurement and supplier negotiation
- Constraint balancing (budget vs timeline vs quality)
- Strategic decision-making under uncertainty

**Evidence from Research:**
- All competitors (MIT Sloan, Cesim, SimProject, GoVenture) focus on execution, not planning
- No existing tool offers AI-powered negotiation for realistic supplier interactions
- Norwegian universities must use English-only tools, reducing local relevance

### The Gap
Students need a **safe space to practice planning decisions** before entering the workforce, where mistakes have real consequences.

---

## 2. Solution Overview

### Core Concept
Students play the role of project manager for Nye Hædda Barneskole (New Hædda Elementary School), a 700 MNOK construction project with a May 15, 2026 deadline. Their task: **negotiate with AI suppliers to procure 15 WBS items within budget and timeline constraints.**

### Gameplay Loop
1. **Review Constraints** - Budget: 700 MNOK, Deadline: May 15, 2026
2. **Select WBS Item** - Choose from 15 construction tasks (Grunnarbeid, Råbygg, etc.)
3. **Negotiate with AI Supplier** - Chat with realistic AI persona (Bjørn Eriksen, Kari Andersen, etc.)
4. **Commit to Plan** - Accept offer, update budget/timeline
5. **Repeat** - Complete all 15 WBS items
6. **Submit Plan** - Validate against constraints (budget ≤700 MNOK, deadline ≤May 15)
7. **Receive Feedback** - Pass (export session) or Fail (renegotiate)

### Key Innovation: AI Supplier Personas
5 distinct AI suppliers powered by Gemini 2.5, each with:
- **Unique personality** (skeptical, optimistic, pragmatic)
- **Hidden negotiation parameters** (initial_margin: 1.15-1.30, concession_rate: 0.03-0.07)
- **Realistic behavior** (walk away if demands unreasonable, reference past projects)

**Example:**
> **Bjørn Eriksen** (Totalentreprenør): Skeptical, values quality over speed, starts at 1.20 margin, willing to reduce 5% per round, walks away after 3 rounds.

---

## 3. Target Users

### Primary Persona: Sara (University Student)
- **Age:** 22, 3rd-year engineering student (NTNU)
- **Goal:** Learn project management for future career as construction PM
- **Pain Point:** Theoretical knowledge, no practical negotiation experience
- **Needs:** Safe practice environment, realistic scenarios, Norwegian context

### Secondary Persona: Magnus (Mid-Career Professional)
- **Age:** 35, construction project manager seeking upskilling
- **Goal:** Improve negotiation skills for better procurement outcomes
- **Pain Point:** Learns from mistakes on real projects (costly)
- **Needs:** Time-efficient, focused on planning phase

### Tertiary Persona: Prof. Eriksen (Educator)
- **Age:** 48, teaches PM at Norwegian university
- **Goal:** Engage students with practical, relevant learning tool
- **Pain Point:** Existing tools are English-only, execution-focused, time-consuming
- **Needs:** Norwegian language, 45-60 min duration (fits lecture), planning focus

---

## 4. MVP Scope (4-5 Weeks)

### Must-Have Features (15 items)
1. User authentication (Supabase JWT)
2. View project constraints (budget, deadline)
3. View WBS list (15 items from PDF)
4. Select WBS item → view requirements
5. **Choose supplier** from 3-5 AI personas
6. **Chat interface** with AI supplier (Norwegian)
7. **AI generates realistic offers** (cost, duration)
8. Accept offer → commit to plan
9. Real-time budget/timeline updates
10. **Renegotiation** (reopen completed WBS item)
11. Submit plan for validation
12. **Validation feedback** (budget/timeline pass/fail)
13. Success modal with session stats
14. **Export session** (JSON download with full history)
15. Help/documentation

### Out of Scope (Post-MVP)
- ❌ Execution phase (construction progress simulation)
- ❌ Precedence diagram visualization (beyond Gantt chart)
- ❌ Multi-user collaboration
- ❌ 3D building visualization
- ❌ VR/AR interface

### Technical Architecture
- **Frontend:** React + TypeScript + Tailwind CSS + Shadcn UI
- **Backend:** FastAPI (3 endpoints: auth, AI chat proxy, validation)
- **Storage:** localStorage (browser-based, no database)
- **AI:** Gemini 2.5 via PydanticAI (Google AI Studio API)
- **Auth:** Supabase (JWT-based, no database tables)
- **Hosting:** Vercel (frontend + serverless backend)

**Why localStorage?**
- Single-session focus (45-60 min)
- No cross-device resume needed (export-first design)
- Saves 1-2 weeks development time (no database setup)
- 5 MB limit sufficient for 40+ sessions (current usage: 62 KB)

---

## 5. Timeline & Budget

### Development Timeline (4-5 Weeks)

**Week 1: Static Data & Infrastructure (5-7 days)**
- Extract WBS from PDF → wbs.json
- Create supplier personas → suppliers.json
- Set up Supabase auth
- Deploy FastAPI backend (Vercel)
- Create base frontend (Login, Dashboard shell)

**Week 2: Frontend Implementation (5-7 days)**
- Dashboard UI (constraints, WBS list)
- Chat interface
- Modals (confirmation, success, error)
- localStorage integration
- Real-time updates

**Week 3: AI Integration & Prompt Engineering (5-7 days)**
- Integrate Gemini 2.5 API
- **Create 5 system prompts** (critical path)
- Test negotiations (10 samples per supplier)
- Tune concession_rate, patience
- Validation logic (budget/timeline check)

**Week 4: Validation & Visualization Foundation (5-7 days)**
- Validation logic (budget/timeline check)
- Basic Gantt chart view
- Bug fixes and edge case handling

**Week 5: Advanced Visualization & Polish (3-5 days)**
- Precedence diagram view
- History/timeline view
- Norwegian string validation
- Pilot test with 5-10 students
- Final QA

### Budget
**Development:** 4-5 weeks × 1 developer = **160-200 hours**
**API Costs:** Gemini 2.5 Flash (free tier: 15 RPM, 1M TPM) → $0 for pilot
**Hosting:** Vercel (free tier for MVP)

**Total MVP Cost:** Developer time only (no infrastructure costs)

---

## 6. Success Metrics

### Learning Outcomes
- **Pedagogical Goal 1:** 80% of students demonstrate budget constraint awareness (stay within 700 MNOK ±3%)
- **Pedagogical Goal 2:** 70% successfully balance timeline vs cost trade-offs
- **Pedagogical Goal 3:** Students complete avg 2-3 negotiation rounds per WBS item (indicates challenge)
- **Pedagogical Goal 4:** 90% complete simulation within 60 minutes

### User Engagement
- **Engagement 1:** 85% session completion rate (students finish all 15 WBS items)
- **Engagement 2:** 80% submit plan for validation (don't abandon mid-game)
- **Engagement 3:** Avg 20+ renegotiations per session (strategic rethinking)

### AI Quality
- **AI Realism:** 80% of students rate AI as "realistic" or "very realistic"
- **AI Robustness:** <5% of negotiations result in "broken" AI behavior

### Technical Performance
- **Performance 1:** UI responses <2 seconds (page loads, button clicks)
- **Performance 2:** AI responses 1-3 seconds (realistic thinking time)
- **Performance 3:** Zero localStorage quota errors during pilot

---

## 7. Unique Value Proposition

### Competitive Positioning
**vs. MIT Sloan PM Simulation:**
- ✅ Planning focus (vs execution)
- ✅ Norwegian language (vs English)
- ✅ 45-60 min (vs 2-4 hours)
- ✅ AI negotiation (vs system dynamics)

**vs. Cesim Project:**
- ✅ Single-player (vs team-based)
- ✅ Procurement focus (vs multi-project management)
- ✅ Norwegian context (vs generic scenarios)

**vs. SimProject:**
- ✅ Scenario-driven (vs tool-focused)
- ✅ AI interaction (vs static exercises)
- ✅ Realistic negotiation (vs WBS creation)

### Why Students Choose Us
1. **Realistic AI Negotiation** - Practice skills used daily in PM roles
2. **Norwegian Context** - Relatable scenario (local school construction)
3. **Time-Efficient** - Complete in single lecture, immediate feedback
4. **Safe to Fail** - Learn from mistakes without real-world consequences

### Why Universities Choose Us
1. **Planning Phase Focus** - Fills gap in existing PM curricula
2. **Norwegian Language** - No translation needed, culturally relevant
3. **Easy Integration** - 45-60 min fits lecture, web-based (no installation)
4. **Research-Backed** - Aligns with constructivist learning theory (learning by doing)

---

## 8. Risk Mitigation

### Risk 1: AI Negotiation Not Realistic Enough
- **Probability:** Medium (30%)
- **Impact:** High (core feature fails)
- **Mitigation:**
  - Allocate full week to prompt engineering (Week 3)
  - Use 2025 best practices (context engineering, tight personas)
  - Test with 10 sample negotiations per supplier
  - Backup: Reduce to 3 suppliers if tuning takes longer

### Risk 2: localStorage Insufficient
- **Probability:** Low (10%)
- **Impact:** Medium (requires architecture change)
- **Mitigation:**
  - Current usage (62 KB) well below limit (5 MB)
  - Add storage monitoring (warn at 80% capacity)
  - Fallback: Export session, clear storage

### Risk 3: Students "Game" the AI
- **Probability:** Medium (25%)
- **Impact:** Medium (learning objectives compromised)
- **Mitigation:**
  - Hidden negotiation parameters (students can't reverse-engineer)
  - Realistic walk-away behavior (AI refuses unreasonable demands)
  - Success metrics track negotiation quality, not just completion

### Risk 4: 4-5 Week Timeline Too Tight
- **Probability:** Low (15%)
- **Impact:** Medium (delayed launch)
- **Mitigation:**
  - Simplified architecture (localStorage, minimal backend)
  - Clear MoSCoW prioritization (15 Must-Haves defined)
  - Buffer built into Week 5 (3-5 days for polish)
  - Visualization features (Epic 10) marked as "Should Have" for flexibility

---

## 9. Next Steps

### Immediate (Phase 2: Solutioning)
1. **Create Epics and Stories** - Break PRD into implementation tasks
2. **Test Design** - Define test strategy and test cases
3. **Solutioning Gate Check** - Final architecture review

### Week 1 (Development Kickoff)
1. Extract WBS from PDF
2. Create supplier persona JSON files
3. Set up Supabase auth
4. Deploy FastAPI backend skeleton
5. Implement Login page

### Critical Path
- **Week 3 Prompt Engineering** is highest risk → allocate senior developer or PM with AI experience
- **Static Data Preparation** blocks Week 2 frontend → start immediately in Week 1

---

## 10. Stakeholder Alignment

### What We're Building
A 45-60 minute web-based simulation where Norwegian university students negotiate with AI suppliers to plan a 700 MNOK school construction project, learning budget constraints, timeline management, and procurement skills.

### What We're NOT Building (MVP)
- ❌ Full project lifecycle (execution, monitoring, closing)
- ❌ Multi-user collaboration or team-based play
- ❌ Advanced visualizations (3D, VR, complex Gantt charts)
- ❌ Multi-language support (Norwegian only for MVP)

### Why This Matters
**Educational Impact:** Students gain practical experience in the most critical (and most neglected) phase of project management—planning. Research shows planning errors account for 70%+ of project failures.

**Market Gap:** No existing tool combines planning focus + AI negotiation + Norwegian context. We're creating a category-defining product.

**Scalability:** MVP validates concept with Norwegian universities. Proven model expands to Nordic region, other industries (IT, healthcare), and global markets.

---

## Appendix: Key Documents

- **Proposal:** `docs/proposal.md` (Original vision, 700 MNOK budget, May 15 2026 deadline)
- **Brainstorming Executive Summary:** `docs/brainstorming-executive-summary.md` (Synthesis of 5 sessions)
- **PRD:** `docs/PRD.md` (35+ functional requirements, 30+ user stories)
- **UX Design:** `docs/ux-design-specification.md` (Wireframes, components, Norwegian UI)
- **Research Report:** `docs/research-report-2025-12-07.md` (AI prompts, localStorage, competitive analysis)
- **Validation Reports:**
  - `docs/validation-report-PRD-2025-12-07.md` (97% pass rate)
  - `docs/validation-report-UX-Design-2025-12-07.md` (96% pass rate)

---

**Document Status:** Complete and ready for stakeholder review.

**Approval:** Pending stakeholder sign-off before proceeding to Phase 2 (Solutioning).

**Contact:** [Project Owner Name] | [Email] | [Date]

---

**End of Product Brief**
