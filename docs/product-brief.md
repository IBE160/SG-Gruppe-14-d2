# Product Brief
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 2.0
**Date:** 2025-12-11
**Status:** Updated for POC Scope
**Project Phase:** Phase 0 Complete, POC Scope Defined

---

## Executive Overview

**Nye Hædda Barneskole** is an AI-powered project management simulation that teaches university students the critical planning phase of construction projects through realistic negotiation with **4 distinct AI agent roles** (3 suppliers + 1 owner). The **POC (Proof of Concept)** focuses on core negotiation mechanics with **3 negotiable work packages** within a challenging budget constraint.

**Key Differentiators:**
- ✅ **Only PM simulation focused on PLANNING** (vs execution)
- ✅ **4 AI agent roles** with distinct negotiation powers:
  - 3 Supplier agents (price/quality, time/cost, scope reduction)
  - 1 Owner agent (budget approval, **inflexible time constraint**)
- ✅ **Norwegian language** and construction context
- ✅ **40-50 minute POC experience** (focused on core mechanics)
- ✅ **Challenging budget constraint:** 310 MNOK available vs 345 MNOK baseline (user must negotiate)

**POC Scope Change (v2.0):**
- **From:** 15 negotiable WBS packages, 5 supplier personas
- **To:** 3 negotiable + 12 locked packages, 4 AI agents (Owner + 3 suppliers)
- **Rationale:** Focus on AI negotiation quality over quantity; prove concept with manageable scope

**Market Opportunity:** Norwegian universities (NTNU, UiO, UiB, HiOA) teaching PM courses to ~500-1,000 students annually. POC validates AI negotiation mechanics before expanding to full 15-package simulation.

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

### Core Concept (POC)
Students play the role of project manager for Nye Hædda Barneskole (New Hædda Elementary School), a 700 MNOK construction project with a May 15, 2026 **inflexible deadline**. Their task: **negotiate with 4 AI agents (3 suppliers + 1 owner) to procure 3 negotiable WBS packages within a challenging budget constraint.**

**Budget Challenge:**
- **Total project:** 700 MNOK
- **Already locked:** 650 MNOK (12 contracted suppliers - non-negotiable)
- **Available for 3 negotiable packages:** 310 MNOK
- **Baseline estimates for 3 packages:** 345 MNOK (105 + 60 + 180)
- **Challenge:** User must negotiate to reduce costs by 35-45 MNOK OR convince Owner to approve budget increase

### Gameplay Loop (POC)
1. **Review Constraints** - Budget: 310 MNOK available (of 700 total), Deadline: May 15, 2026 (inflexible)
2. **Select Negotiable WBS Item** - Choose from **3 blue-highlighted negotiable packages** (12 locked shown as gray/read-only)
3. **Choose Negotiation Partner** - Select **Supplier** (for cost/time/quality) OR **Owner** (for budget/scope)
4. **Negotiate with AI Agent** - Chat with realistic AI persona with distinct powers
5. **Explicit Accept/Reject** - User must actively click "Godta" or "Avslå" (NO automatic acceptance)
6. **Commit to Plan** - Update budget/timeline
7. **Repeat** - Complete all 3 negotiable WBS items
8. **Submit Plan** - Validate against constraints (3 negotiable + 12 locked ≤700 MNOK total, deadline ≤May 15)
9. **Receive Feedback** - Pass (export session) or Fail (renegotiate)

### Key Innovation: 4 AI Agent Roles
Powered by Gemini 2.5, each with **distinct negotiation capabilities:**

| Agent | Role | Negotiation Powers | Hidden Parameters |
|-------|------|-------------------|-------------------|
| **Anne-Lise Berg** | Owner (Municipality) | ✅ Budget increase (strong arguments required)<br>✅ Scope reduction approval<br>❌ **NEVER extends time** | max_budget_increase: 15% total<br>time_extension_allowed: **false** |
| **Bjørn Eriksen** | Supplier 1 (Grunnarbeid) | ✅ Price reduction<br>✅ Quality reduction | initial_margin: 1.20<br>min_cost: 88% baseline |
| **Kari Andersen** | Supplier 2 (Fundamentering) | ✅ Faster delivery for higher cost<br>✅ Time/cost tradeoffs | time_reduction_cost: +30% per 25% time reduction |
| **Per Johansen** | Supplier 3 (Råbygg) | ✅ Scope reduction proposals<br>✅ Price flexibility | scope_reduction_savings: 10-18 MNOK per feature |

**Example - Owner Negotiation:**
> **User:** "Can we extend deadline by 2 months?"
> **Anne-Lise Berg:** "Tidsfristen er ufravikelig. Skolen må stå klar til skolestart i august. Samfunnskostnaden ved forsinkelse er høyere enn økt budsjett." (Time is inflexible. School must be ready for August start. Societal cost of delay exceeds budget overruns.)

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

## 4. POC Scope (3-4 Weeks)

### Must-Have Features (16 items)
1. User authentication (Supabase JWT)
2. View project constraints (310 MNOK available, 700 MNOK total, May 15 deadline)
3. **View WBS list (15 total: 3 negotiable + 12 locked)**
   - 3 negotiable: Blue highlight, "Kan forhandles" badge, interactive
   - 12 locked: Gray, "Kontraktfestet" badge, read-only with pre-committed values
4. Select negotiable WBS item → view requirements
5. **Choose negotiation partner:** 3 suppliers OR 1 owner
6. **Chat interface** with AI agent (Norwegian)
7. **AI generates realistic offers** (cost, duration) based on agent role
8. **Explicit Accept/Reject** - User must click "✓ Godta" or "✗ Avslå" (NO automatic acceptance)
9. Accept offer → commit to plan
10. Real-time budget/timeline updates (tracks 3 negotiable + 12 locked)
11. **Renegotiation** (reopen completed WBS item)
12. **Owner AI negotiation:**
    - Budget increase requests (with argumentation quality evaluation)
    - Time extension requests (**100% rejection rate** with explanation)
    - Scope reduction approval
13. Submit plan for validation
14. **Validation feedback** (3 negotiable + 12 locked ≤700 MNOK, deadline ≤May 15)
15. Success modal with session stats
16. **Export session** (JSON download with full history, chat logs)

### Out of Scope (Post-POC)
- ❌ Negotiating all 15 WBS packages (POC: only 3 negotiable)
- ❌ Execution phase (construction progress simulation)
- ❌ Contract signing (commitment only, no formal contracts)
- ❌ Multi-user collaboration
- ❌ 3D building visualization
- ❌ VR/AR interface
- ❌ Automatic offer acceptance (must be explicit user action)

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
