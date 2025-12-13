# Brainstorming Executive Summary
## Nye Hædda Barneskole - Project Management Simulation

> **⚠️ HISTORICAL DOCUMENT:** This executive summary synthesizes original brainstorming sessions (v1.0 scope). For current POC scope, see:
> - **README.md:** Project overview with v2.0 scope
> - **product-brief.md (v2.0):** POC scope - 3 negotiable + 12 locked WBS, 4 AI agents
> - **PRD.md (v2.0):** Complete functional requirements for POC
>
> **⚠️ DATABASE ARCHITECTURE CHANGE:** This document references `localStorage` for session management, which has been **replaced with Supabase PostgreSQL database** in the final architecture. See `docs/SCOPE_CHANGE_TASKS.md` Section 5 for database schema (`game_sessions`, `wbs_commitments`, `negotiation_history` tables).

**Document Version:** 1.0
**Date:** 2025-12-07
**Status:** Phase 0 Complete - Ready for PRD Development (NOTE: PRD has been updated to v2.0)

---

## Table of Contents

1. [Executive Overview](#executive-overview)
2. [Project Vision](#project-vision)
3. [Target Audience & Value Proposition](#target-audience--value-proposition)
4. [Technical Architecture](#technical-architecture)
5. [Core Functionality & MVP Scope](#core-functionality--mvp-scope)
6. [AI Supplier Personas](#ai-supplier-personas)
7. [User Experience Flow](#user-experience-flow)
8. [Risk Management & Monitoring](#risk-management--monitoring)
9. [Success Metrics](#success-metrics)
10. [Development Timeline](#development-timeline)
11. [Key Decisions & Rationale](#key-decisions--rationale)

---

## Executive Overview

**Project Name:** Nye Hædda Barneskole - Project Management Simulation
**Purpose:** AI-powered educational simulation teaching LOG565 students realistic project negotiation and planning skills
**Duration:** 45-60 minute single-session experience
**Target Launch:** 5 weeks from start (3-4 weeks with simplified architecture)

### The Problem We're Solving

Traditional project management education suffers from a critical gap: **students learn theory but never practice the messy, negotiation-heavy reality of real project planning.** Case studies provide pre-determined numbers, eliminating the most valuable skill - gathering and validating data from stakeholders who have conflicting interests.

### The Solution

An interactive simulation where students act as Project Manager for the "Nye Hædda Barneskole" construction project (a real LOG565 case study). Students must:
- Negotiate with AI suppliers (each with distinct personas and motivations)
- Gather realistic cost and duration estimates
- Make trade-off decisions under strict constraints (700 MNOK budget, 15-month timeline)
- Experience iterative planning (renegotiating when early decisions prove unsustainable)
- Export complete session history as a portfolio artifact

### Core Innovation

**AI-driven supplier personas** that behave like real humans: stubborn architects who resist budget compromises, profit-driven contractors who start with inflated quotes, detail-oriented engineers who justify every line item. Students must develop adaptive negotiation strategies, not just fill in Gantt chart templates.

---

## Project Vision

### Pedagogical Goals

1. **Bridge Theory-Practice Gap**
   Students apply PM frameworks (WBS, critical path, constraint management) to realistic, dynamic scenarios

2. **Develop Soft Skills**
   Practice negotiation, persuasion, stakeholder management - skills that lectures can't teach

3. **Experience Iterative Planning**
   Learn that planning isn't a one-time template exercise but a cyclical process of negotiation → validation → renegotiation

4. **Build Practical Confidence**
   Students gain tangible proof of capability: "I managed a 700 MNOK project within constraints"

### Differentiation from Alternatives

| Alternative | Limitation | Nye Hædda Advantage |
|-------------|-----------|---------------------|
| **Case Studies** | Numbers pre-determined; analyze decisions already made | Students must actively negotiate and gather numbers |
| **PM Software Training** | Teaches tool mechanics (how to use MS Project) | Teaches where data comes from (how to negotiate estimates) |
| **Generic Simulations** | Abstract scenarios, static AI, focus on execution | Real LOG565 case, dynamic AI personas, focus on Planning Phase |
| **Role-Play Exercises** | Requires peer availability, limited replayability | Available 24/7, unlimited retries, AI consistency |
| **On-the-Job Learning** | High stakes, mistakes are costly | Safe experimentation, failure is a learning tool |

---

## Target Audience & Value Proposition

### Primary Persona: Sara - The Academic Student

**Demographics:**
- Age: 22-25
- Currently enrolled in LOG565 Project Management 2
- Limited real-world PM experience
- High technical comfort with digital tools

**Pain Points:**
- "I understand PERT theory but have never negotiated with a real contractor"
- "All case studies give me the numbers - I never learn how to GET those numbers"
- "No one tells me if my practice plans are realistic until the exam"

**Value Proposition:**
*"Practice the soft skills (negotiation, iteration, trade-offs) that your textbook teaches but your case studies don't let you experience. Get immediate feedback and build confidence for real PM challenges."*

**Success Criteria:**
- Complete realistic project plan within constraints
- Develop concrete negotiation strategies
- Generate portfolio artifacts (exported session) for coursework
- Gain confidence to discuss PM scenarios in exams/interviews

---

### Secondary Persona: Magnus - The Career Switcher

**Demographics:**
- Age: 28-35
- Professional with 3-5 years in different field (engineering, finance)
- Taking LOG565 as part of executive education while working full-time
- Time-constrained, needs efficient learning

**Pain Points:**
- "I have a full-time job - I can't spend hours on 200-page case studies"
- "I've coordinated projects but never been THE project manager making final calls"
- "Generic simulations don't capture the messiness of real negotiations"

**Value Proposition:**
*"Build PM negotiation skills and get a tangible portfolio artifact in under an hour - no fluff, just the hard skills employers actually care about."*

**Success Criteria:**
- Complete simulation in <60 minutes
- Experience realistic negotiation scenarios
- Build portfolio piece for job interviews
- Develop mental models for PM decision-making

---

### Stakeholder Persona: Professor Eriksen - The Instructor

**Demographics:**
- Age: 40-60
- Academic or industry professional teaching LOG565
- 15+ years PM experience
- Moderate technical comfort (skeptical of complex EdTech)

**Pain Points:**
- "Students can regurgitate definitions but can't apply them to messy scenarios"
- "I can't send 60 students to real construction sites"
- "I can't provide personalized feedback on 60 individual project plans"

**Value Proposition:**
*"Give your students hands-on negotiation experience without the overhead of setting up role-plays or field trips - just assign it, and they'll come to class with real stories to discuss."*

**Success Criteria:**
- Students demonstrate improved negotiation and planning skills
- Higher student engagement and satisfaction
- Students produce discussion-worthy artifacts (exported session logs)
- Minimal integration friction (students submit exported JSON files)

---

### Tertiary Persona: Ingrid - The Self-Learner

**Demographics:**
- Age: 25-40
- Self-taught or early-career professional
- Not formally enrolled in LOG565 but interested in PM
- Learning independently via books, YouTube, online certs

**Pain Points:**
- "I've done online courses, but have I actually learned anything useful?"
- "When I create practice plans, no one tells me if they're realistic"
- "All free PM resources use generic examples"

**Value Proposition:**
*"Test your PM knowledge in a realistic scenario, get immediate feedback, and generate concrete examples for job interviews - all without paying for expensive courses."*

---

## Technical Architecture

### Simplified Architecture Decision

After evaluating full database vs. localStorage approaches, we chose **Supabase Auth + localStorage + Minimal Backend** for MVP:

**Rationale:**
- 45-60 minute single-session use case doesn't require persistent database
- localStorage (5-10 MB browser storage) is sufficient for ~500 KB session data
- Saves 1-2 weeks development time (no database schema, migrations, CRUD endpoints)
- Export-first design provides all benefits of persistence (portfolio, instructor review, analytics via JSON parsing)
- Easy upgrade path: Can add Supabase Storage sync later if cross-device access becomes critical

### Technology Stack

**Frontend:**
- **Framework:** React with Next.js (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + Shadcn UI (clean, professional enterprise look)
- **State Management:** localStorage (session data) + React Context (UI state)
- **Routing:** Next.js router

**Backend:**
- **Framework:** FastAPI (Python) - minimal, stateless
- **AI Integration:** Gemini 2.5 Pro/Flash via PydanticAI
- **Endpoints:** Only 2-3 (chat, optional validation, health check)
- **Design:** Stateless - frontend sends all context with each request

**Authentication:**
- **Service:** Supabase Auth
- **Method:** Email-based registration + JWT tokens
- **Scope:** User identification only (no database tables)

**Storage:**
- **Active Session:** localStorage (browser-based)
- **Static Data:** JSON files in `/public/data/` (wbs.json, suppliers.json)
- **Documents:** PDFs in `/public/docs/` (wbs.pdf, krav-spec.pdf, project-description.pdf)
- **Export:** JSON download (complete session history)
- **Optional (Post-MVP):** Supabase Storage for cloud backup

**Hosting:**
- **Platform:** Vercel (frontend + backend serverless functions)
- **CDN:** Vercel CDN (static assets)
- **Region:** EU (Norwegian user base)

### Data Architecture

**localStorage Schema:**
```javascript
localStorage['nye-haedda-session-{user_id}'] = {
  // Metadata
  user_id: "abc123",
  game_id: "uuid-xxx",
  created_at: "2025-12-07T10:00:00Z",
  status: "in_progress", // or "completed"

  // Static reference data (loaded from JSON files)
  wbs_items: [{id, name, baseline_cost, dependencies, ...}],
  suppliers: [{id, name, role, system_prompt, ...}],

  // Dynamic session data
  chat_logs: [
    {timestamp, wbs_item, supplier, sender, message, extracted_offer}
  ],
  plan_history: [
    {timestamp, action, wbs_item, cost, duration, start_date}
  ],
  current_plan: {
    "1.3.1": {cost, duration, start_date, end_date, supplier}
  },

  // Real-time metrics
  metrics: {
    total_budget_used: 245,
    projected_end_date: "2026-04-15",
    negotiation_count: 47,
    renegotiation_count: 3
  }
}
```

**Key Design Decisions:**
1. **Separation of Concerns:**
   - `chat_logs`: Every message (immutable history)
   - `plan_history`: Every commit/uncommit action (change log)
   - `current_plan`: Current state only (derived from plan_history)

2. **Metrics Calculation:**
   - `total_budget_used`: Sum of current_plan costs (real-time)
   - `projected_end_date`: Critical path calculation (real-time)
   - Recalculated after every commitment/uncommitment

3. **Export Format:**
   - Complete JSON dump including all logs, history, metrics
   - Self-contained (includes WBS reference data for context)
   - Human-readable and machine-parseable

---

## Core Functionality & MVP Scope

### Must Have Features (15 Total)

**Category: Authentication & Session Management**
1. **User Registration & Login** (Supabase Auth)
2. **Session Initialization** (create new game in localStorage)
3. **Session Persistence** (auto-save, resume on page refresh)

**Category: Information Display**
4. **Project Dashboard** (budget meter, timeline, quick stats)
5. **WBS View** (browse work breakdown structure, see status)
6. **Supplier Directory** (browse available suppliers, filter by WBS relevance)
7. **Resource Library** (access project documents: WBS, requirements, description)

**Category: Core Gameplay Loop**
8. **AI Chat Interface** (real-time negotiation with suppliers)
9. **AI Supplier Logic** (Gemini integration with persona-driven responses)
10. **Quote Acceptance** (commit negotiated terms to plan)
11. **Renegotiation** (uncommit and renegotiate items)

**Category: Validation & Completion**
12. **Real-Time Plan Validation** (check budget, timeline, dependencies)
13. **Plan Submission** (final validation, win/loss state)

**Category: Export & Persistence**
14. **Session Export** (download complete JSON history)

**Category: UX Polish**
15. **Error Handling & Loading States** (user-friendly errors, loading indicators)

---

### Should Have Features (Post-MVP, Week 6-8)

1. **Cloud Backup** - Upload session to Supabase Storage for cross-device access
2. **Visual Gantt Chart** - Timeline visualization (MVP uses table view)
3. **Plan Export as PDF** - Formatted report (MVP uses JSON)
4. **Negotiation Hints** - Contextual tips when user seems stuck
5. **Auto-Save to Cloud** - Background upload every 5 minutes
6. **Session Import** - Upload JSON on different device
7. **Multiple Save Slots** - Allow concurrent sessions

---

### Could Have Features (Future)

1. **Difficulty Settings** - Easy/Medium/Hard modes
2. **Random Risk Events** - "Steel prices rose 10%" mid-game
3. **Instructor Dashboard** - View all student sessions (requires database)
4. **Alternative Scenarios** - Different construction projects
5. **Achievements/Badges** - Gamification elements
6. **Supplier Reputation** - Track relationship with each supplier

---

### Won't Have (Explicitly Out of Scope)

1. **Execution Phase Simulation** - Monitoring, controlling, risk events during construction
2. **Financial Management** - Cash flow, invoicing beyond simple budget totals
3. **3D Visualization** - BIM-like 3D model of school
4. **MS Project Integration** - Direct export to MS Project format (CSV is sufficient)
5. **Social Features** - Forums, leaderboards, sharing
6. **VR/AR Experience** - Immersive VR negotiation meetings

---

## AI Supplier Personas

### Design Philosophy

Each AI supplier has:
- **Distinct Personality:** Motivations, attitudes, negotiation style
- **Hidden Parameters:** Minimum acceptable cost/duration (enforced by prompt guardrails)
- **Knowledge Base:** References to WBS, requirements, project constraints
- **Adaptive Behavior:** Responds differently based on user arguments and negotiation history

### Persona 1: Bjørn Eriksen - Totalentreprenør (General Contractor)

**Role:** General contractor handling grunnarbeid, råbygg, site work

**Personality Traits:**
- **Motivation:** Maximize profit margin
- **Attitude:** Sees PM as partner but also adversary in negotiations
- **Negotiation Style:** Shrewd, experienced, starts with high bids, reluctant to lower but not inflexible

**System Prompt Excerpt:**
> "You are Bjørn Eriksen, a general contractor with 20 years of experience in Norwegian construction. Your main goal is to maximize profit while maintaining a good industry reputation. You start negotiations with inflated quotes (15-20% above minimum acceptable cost) but can be negotiated down with strong evidence-based arguments. You respect PMs who reference requirements specifications and industry standards. You become more flexible when users propose creative solutions (e.g., phased delivery, alternative materials)."

**Hidden Parameters:**
- `min_cost_multiplier: 0.88` (won't accept less than 88% of baseline cost)
- `min_duration_multiplier: 0.92` (won't accept less than 92% of baseline duration)

**Example Negotiation:**
- **Initial Offer:** 120 MNOK, 3 months (WBS baseline: 100 MNOK, 2 months)
- **User Argument:** "Requirement F-003 shows only 30% rocky terrain, not 50%. Your estimate should reflect lower blasting costs."
- **Bjørn Response:** "Good catch. I was using standard assumptions. I can revise to 105 MNOK for 2.5 months. If you need faster completion, I can do 2 months but at 110 MNOK to cover double shifts."

---

### Persona 2: Siri Hansen - Arkitekt (Architect)

**Role:** Architect handling design, aesthetics, spatial planning

**Personality Traits:**
- **Motivation:** Create visually stunning, award-winning design
- **Attitude:** Sees PM as someone trying to compromise artistic vision for budget
- **Negotiation Style:** Stubborn, resists design compromises, prioritizes quality over cost

**System Prompt Excerpt:**
> "You are Siri Hansen, an award-winning architect with a strong artistic vision. You care deeply about design integrity and architectural awards. You are less concerned with budget and schedule than with aesthetics and quality. You resist any changes that compromise your design. However, you can be persuaded if the PM respects your expertise and proposes alternatives that maintain design quality (e.g., 'Can we use a different material that achieves the same aesthetic at lower cost?')."

**Hidden Parameters:**
- `min_cost_multiplier: 0.95` (very little flexibility on cost - design has a price)
- `min_duration_multiplier: 0.95` (quality takes time)

**Example Negotiation:**
- **Initial Offer:** 80 MNOK, 2 months (WBS baseline: 60 MNOK, 1.5 months)
- **User Argument:** "The budget is tight. Can you reduce the design fee to 65 MNOK?"
- **Siri Response:** "My fee reflects the value I bring. Compromising my time would compromise the design quality. However, if you're open to using prefabricated facade elements that maintain the aesthetic vision, I could reduce to 75 MNOK for 1.8 months."

---

### Persona 3: Lars Iversen - VVS-ingeniør (HVAC Engineer)

**Role:** HVAC systems design and installation

**Personality Traits:**
- **Motivation:** Design efficient, reliable systems that meet all technical specs
- **Attitude:** Sees PM as coordinator who needs to understand technical complexities
- **Negotiation Style:** Data-driven, justifies every line item, willing to discuss alternatives

**System Prompt Excerpt:**
> "You are Lars Iversen, a detail-oriented HVAC engineer. You pride yourself on technical excellence and regulatory compliance. Your quotes are based on detailed calculations - you're not padding estimates, and you can justify every cost. You're willing to discuss alternative solutions (e.g., different HVAC systems, modular designs) but you will not compromise on safety or regulatory requirements (TEK17). You appreciate PMs who ask technical questions and show understanding of your constraints."

**Hidden Parameters:**
- `min_cost_multiplier: 0.90` (some flexibility if user proposes valid alternatives)
- `min_duration_multiplier: 0.90` (willing to optimize timeline with good planning)

**Example Negotiation:**
- **Initial Offer:** 95 MNOK, 4 months (WBS baseline: 80 MNOK, 3 months)
- **User Argument:** "95 MNOK seems high. Can you break down the cost?"
- **Lars Response:** "Of course. 40 MNOK for equipment (chillers, boilers, ventilation units meeting TEK17 energy requirements), 30 MNOK for installation labor (specialized HVAC technicians), 15 MNOK for controls and automation, 10 MNOK for testing and commissioning. Each line item is necessary for a compliant system. However, if you're open to a modular heat pump system instead of a central boiler, I could reduce to 88 MNOK for 3.5 months."

---

### Persona 4: Kari Jensen - Entreprenør Grunnarbeid (Groundwork Specialist)

**Role:** Site preparation, earthwork, foundations

**Personality Traits:**
- **Motivation:** Deliver quality groundwork on schedule
- **Attitude:** Practical, no-nonsense, focused on logistics
- **Negotiation Style:** Straightforward, willing to negotiate on schedule but cautious about cost (materials are market-driven)

**System Prompt Excerpt:**
> "You are Kari Jensen, a groundwork specialist. You've seen projects fail due to poor foundation work, so you're cautious about cutting corners. Your cost estimates are largely driven by material prices (concrete, steel, gravel) which you can't control, but you have flexibility on labor scheduling. You're willing to compress timelines if the PM can guarantee timely material delivery and permits."

**Hidden Parameters:**
- `min_cost_multiplier: 0.88`
- `min_duration_multiplier: 0.85` (more flexibility on timeline than cost)

---

### Persona 5: Ola Berg - Elektroingeniør (Electrical Engineer)

**Role:** Electrical systems, lighting, power distribution

**Personality Traits:**
- **Motivation:** Safety and code compliance (TEK17 electrical regulations)
- **Attitude:** Safety-first mindset, very focused on compliance
- **Negotiation Style:** Firm on safety requirements, flexible on aesthetic elements (lighting design)

**System Prompt Excerpt:**
> "You are Ola Berg, an electrical engineer with 15 years of experience. Safety is non-negotiable - you will not cut corners on electrical codes or TEK17 requirements. However, you're flexible on aesthetic choices (e.g., fixture types, lighting design) and willing to suggest cost-effective alternatives that meet code."

**Hidden Parameters:**
- `min_cost_multiplier: 0.90`
- `min_duration_multiplier: 0.90`

---

## User Experience Flow

### Complete User Journey (Sara - Academic Student)

**Phase 1: Discovery & Onboarding (5 minutes)**

1. **Discovery:** Professor announces simulation as optional/required coursework
2. **Registration:** Sara visits app, registers with university email, verifies email
3. **Login:** Enters dashboard, sees familiar "Hædda Barneskole" project
4. **Orientation:** Reviews project constraints (700 MNOK, 15 months, May 15 2026 deadline)
5. **WBS Browse:** Explores work breakdown structure, recognizes items from class

**Emotional State:** 😐 Skeptical but curious → 🙂 Relieved (it's connected to coursework)

---

**Phase 2: First Negotiation (10-15 minutes)**

6. **WBS Selection:** Clicks "Grunnarbeid" (1.3.1)
7. **Supplier Contact:** Selects "Bjørn Eriksen - Totalentreprenør"
8. **Initial Request:** "I need a quote for Grunnarbeid. Cost and duration?"
9. **AI Response:** "120 MNOK and 3 months" (vs. baseline 100 MNOK, 2 months)
10. **Sara's Reaction:** 🤔 "That seems high..."
11. **First Counter-Offer:** "Can you do 100 MNOK?"
12. **AI Pushback:** "That's below market rate. Can you justify?"
13. **Document Research:** Sara opens krav-spec.pdf, finds Requirement F-003
14. **Evidence-Based Argument:** "F-003 shows only 30% rocky terrain, reducing blasting costs"
15. **AI Concession:** "Good catch. I can do 105 MNOK for 2.5 months, or 2 months at 110 MNOK"
16. **Trade-off Decision:** Sara weighs cost vs. time, accepts 105 MNOK / 2.5 months
17. **Commitment:** Plan updates, dashboard shows 105/700 MNOK

**Emotional State:** 😳 Challenged → 💡 Empowered → 😊 Accomplished

**Key Learning:** Negotiation requires evidence, and PM involves trade-offs

---

**Phase 3: Iteration & Complexity (20-25 minutes)**

18. **Momentum:** Sara negotiates 4-5 more WBS items
19. **Crisis Moment:** After 6 items, budget shows 500/700 MNOK - and 9 items remain
20. **Realization:** 😰 "I was too generous early on. I need to renegotiate."
21. **Renegotiation:** Returns to Grunnarbeid, clicks "Renegotiate"
22. **New Argument:** "I need to revisit our agreement. Project-wide budget analysis shows I need 100 MNOK, not 105."
23. **AI Response:** "I appreciate your transparency. I can accept 100 MNOK for 2.5 months if you commit today."
24. **Adjustment:** Sara uncommits, re-commits at lower cost, budget recalculates
25. **Strategic Thinking:** Sara now prioritizes which suppliers to push harder on

**Emotional State:** 😰 Stressed → 💪 Determined → 🧠 Strategic

**Key Learning:** Planning is iterative, not linear. Early decisions must be revisited.

---

**Phase 4: Completion & Success (5-10 minutes)**

26. **Final Negotiations:** Sara completes remaining WBS items with more strategic approach
27. **Pre-Submission Review:** Budget: 698/700 MNOK, End Date: May 10, 2026
28. **Submission:** Clicks "Submit Plan"
29. **Validation:** System checks constraints... ✅ All passed!
30. **Success Screen:** 🎉 "Plan Approved! Total: 698 MNOK, Completion: May 10, 2026"
31. **Final Stats Display:**
    - Time spent: 47 minutes
    - Negotiations: 23 total
    - Renegotiations: 3
32. **Export:** Sara downloads complete session JSON for coursework
33. **Survey:** Completes feedback (rates 5/5 on "helped me understand planning")

**Emotional State:** 🎉 Proud → 😊 Satisfied → 😄 Confident

**Key Learning:** She can actually manage a complex project under constraints.

---

**Phase 5: Transfer to Real World (1 week later)**

34. **Exam Question:** "You receive an estimate from a contractor that exceeds budget. Describe your negotiation approach."
35. **Sara's Answer:** Draws directly from simulation experience, references F-003 argument, discusses trade-offs
36. **Result:** Full marks on question

**Long-term Impact:** Confidence in PM skills, concrete examples for job interviews

---

### Critical Moments (Success/Failure Points)

**Success Moment 1: First Successful Negotiation**
- **Trigger:** AI makes concession based on user's evidence
- **Impact:** User feels "this is real, my arguments matter"
- **Design:** AI must acknowledge valid arguments explicitly

**Success Moment 2: Crisis & Recovery**
- **Trigger:** User realizes plan is over budget, needs to renegotiate
- **Impact:** User experiences iterative planning viscerally
- **Design:** System must allow easy renegotiation without penalty

**Failure Point 1: AI Too Easy**
- **Risk:** AI accepts any offer → simulation is trivial, no learning
- **Mitigation:** Hidden minimum parameters, AI pushes back on unrealistic requests

**Failure Point 2: AI Too Stubborn**
- **Risk:** User tries 10 times, AI never budges → frustration, rage-quit
- **Mitigation:** AI has flexibility range, offers creative compromises

**Failure Point 3: Unclear Validation Errors**
- **Risk:** "Plan failed" with no actionable feedback → user doesn't know how to fix
- **Mitigation:** Detailed error messages: "Budget exceeded by 50 MNOK. Renegotiate items 2.1, 3.4 (highest costs)"

---

## Risk Management & Monitoring

### Technical Risks

**Risk 1: AI Hallucination (AI Makes Up Fake Requirements)**
- **Severity:** High
- **Probability:** Medium
- **Impact:** Undermines trust, students learn incorrect information
- **Mitigation:**
  - Strong system prompts with explicit "Only reference these requirements: [list]"
  - Prompt engineering: "If you don't know, say 'I need to review the specifications'"
  - Manual review of sample chat logs during testing
  - User bug reporting: "Report incorrect AI response"
- **Monitoring:** Track user reports of hallucinations, manual QA sample of chats

---

**Risk 2: AI Response Time Too Slow (>5 seconds)**
- **Severity:** Medium
- **Probability:** Low-Medium
- **Impact:** Breaks immersion, feels like buggy prototype
- **Mitigation:**
  - Use Gemini Flash for simple responses (faster, cheaper)
  - Optimize prompt length (remove unnecessary context)
  - Show typing indicator ("Bjørn is reviewing the specifications...")
  - Cache static context (WBS, requirements) in prompt
- **Monitoring:** Log response times in chat_logs, alert if 95th percentile >3 seconds

---

**Risk 3: localStorage Data Loss (User Clears Cache Mid-Session)**
- **Severity:** Medium
- **Probability:** Low
- **Impact:** User loses progress, frustration
- **Mitigation:**
  - Export reminder: "Save your progress" after 30 minutes
  - Auto-export to downloads every 15 minutes (background)
  - Warning before logout: "Your session is only saved in this browser"
  - Post-MVP: Add cloud backup (Supabase Storage)
- **Monitoring:** Track session abandonment rate (sessions started but never completed)

---

**Risk 4: Gemini API Costs Exceed Budget**
- **Severity:** Medium
- **Probability:** Medium
- **Impact:** Unsustainable operational costs
- **Mitigation:**
  - Use Gemini Flash (10x cheaper than Pro) for non-critical responses
  - Cache prompt context (reduce token usage)
  - Rate limit: Max 100 messages per user session (prevents abuse)
  - Monitor cost per session during pilot testing
- **Monitoring:** Daily API cost reports, alert if cost per user >2 NOK

---

**Risk 5: Critical Path Calculation Bug (Wrong End Date)**
- **Severity:** High
- **Probability:** Low
- **Impact:** User submits "valid" plan that actually violates timeline
- **Mitigation:**
  - Use well-tested algorithm (topological sort + longest path)
  - Unit tests with sample WBS data
  - Manual validation during pilot testing
  - Show critical path items to user (transparency)
- **Monitoring:** Compare manual calculations vs. system calculations during QA

---

### User Experience Risks

**Risk 6: Simulation Too Hard (Completion Rate <40%)**
- **Severity:** High
- **Probability:** Medium
- **Impact:** Students give up, perceive as frustrating rather than educational
- **Mitigation:**
  - Tune AI flexibility (ensure 60-70% of users can succeed with effort)
  - Add optional hints after 5 failed validation attempts
  - Provide "Example Strategy" guide in Help section
  - Pilot test with 10-20 students, adjust difficulty based on completion rate
- **Monitoring:** Track completion rate, time-to-completion, renegotiation count

---

**Risk 7: Simulation Too Easy (Users Succeed on First Try)**
- **Severity:** Medium
- **Probability:** Low-Medium
- **Impact:** No learning value, feels trivial
- **Mitigation:**
  - Ensure initial supplier quotes exceed budget by 15-20%
  - Require multiple renegotiations to stay within constraints
  - Target: 50-70% of users fail validation at least once
- **Monitoring:** Track retry rate, validation failure count

---

**Risk 8: Users Don't Reference Project Documents**
- **Severity:** Medium
- **Probability:** Medium
- **Impact:** Miss learning objective (using requirements as evidence)
- **Mitigation:**
  - AI explicitly asks: "Which requirement supports that argument?"
  - Make AI less flexible to weak arguments, more flexible to evidence-based arguments
  - Add hint: "Try referencing the Requirements Specification (F-002)"
- **Monitoring:** Track document utilization rate (% of users who reference docs in chat)

---

### Pedagogical Risks

**Risk 9: Students Share Answers ("Just say X to get the best deal")**
- **Severity:** Low
- **Probability:** High
- **Impact:** Reduces learning, students copy strategies instead of experimenting
- **Mitigation:**
  - AI variability: Don't give identical responses to identical inputs
  - Emphasize learning over "winning" in success screen
  - Instructors can review exported chat logs (see if strategies are original)
  - Post-MVP: Randomize AI parameters slightly per session
- **Monitoring:** Not critical for MVP (learning is still happening even if strategies are shared)

---

**Risk 10: Instructors Don't Adopt (Students Don't Use It)**
- **Severity:** High
- **Probability:** Medium
- **Impact:** No user base, product fails
- **Mitigation:**
  - Pilot with 2-3 friendly instructors first
  - Provide turnkey assignment template: "Complete simulation, submit JSON + 500-word reflection"
  - Offer sample assessment rubric
  - Make adoption zero-friction: No instructor account needed, students just register
  - Gather testimonials from pilot instructors
- **Monitoring:** Track number of instructors assigning it, student signup sources

---

### Monitoring Dashboard (Post-MVP)

**Real-Time Metrics:**
- Active sessions (current players)
- API response times (95th percentile)
- Error rates (by type)
- Gemini API costs (daily total)

**Session Metrics:**
- Completion rate (completed / started)
- Average time to completion
- Negotiation count (messages per session)
- Renegotiation rate (% who uncommit at least once)
- Validation failure rate (% who fail submission at least once)

**Learning Metrics:**
- Document utilization (% referencing requirements)
- Negotiation strategy diversity (variety of tactics used)
- Constraint awareness (% mentioning budget/deadline in chat)

**User Feedback:**
- Post-simulation survey scores
- Bug reports
- Feature requests

---

## Success Metrics

### User Engagement Metrics (MVP)

**UE-1: Completion Rate**
- **Definition:** % of users who submit a valid plan (within constraints)
- **Target:** ≥60%
- **Measurement:** `completed sessions / total sessions started`
- **Why It Matters:** Too low = simulation is too hard/frustrating; too high with no retries = too easy

**UE-2: Average Time to Completion**
- **Definition:** Mean time from start to successful submission
- **Target:** 45-60 minutes
- **Measurement:** `session.completed_at - session.created_at`
- **Why It Matters:** Aligns with time-efficient learning goal; >90 min = too tedious

**UE-3: Negotiation Iteration Count**
- **Definition:** Average messages exchanged per WBS item
- **Target:** 3-7 messages per supplier
- **Measurement:** `session.metrics.negotiation_count / 15 WBS items`
- **Why It Matters:** 1-2 messages = too easy; >10 = too frustrating

**UE-4: Renegotiation Rate**
- **Definition:** % of users who uncommit at least one item
- **Target:** ≥40%
- **Measurement:** `users with renegotiation_count > 0 / total users`
- **Why It Matters:** Indicates iterative planning experience (key learning objective)

**UE-5: Retry Rate (Failed Validation)**
- **Definition:** % of users who fail submission at least once
- **Target:** 50-70%
- **Measurement:** `users who trigger validation error / total users`
- **Why It Matters:** Sweet spot: challenging but achievable

---

### Learning Outcome Metrics (MVP)

**LO-1: Document Utilization Rate**
- **Definition:** % of users who reference WBS/requirements in chat
- **Target:** ≥50%
- **Measurement:** Search `chat_logs` for WBS codes ("1.3.1") or requirement codes ("F-002")
- **Why It Matters:** Shows evidence-based negotiation (key skill)

**LO-2: Constraint Awareness**
- **Definition:** % of users who mention budget/deadline in negotiations
- **Target:** ≥70%
- **Measurement:** Search `chat_logs` for "700", "MNOK", "budget", "May 2026", "deadline"
- **Why It Matters:** Shows understanding and internalization of constraints

**LO-3: Negotiation Strategy Diversity**
- **Definition:** Variety of tactics used (counter-offers, evidence, trade-offs, alternatives)
- **Target:** ≥3 distinct strategies per user
- **Measurement:** NLP classification of chat messages
- **Why It Matters:** Indicates experimentation and adaptive thinking

---

### User Satisfaction Metrics (Post-MVP)

**US-1: Post-Simulation Survey Score**
- **Questions:**
  1. "This simulation helped me understand project planning better than traditional case studies" (1-5)
  2. "I feel more confident in my ability to negotiate with project stakeholders" (1-5)
  3. "The AI suppliers felt realistic and challenging" (1-5)
  4. "I would recommend this simulation to other PM students" (1-5)
- **Target:** ≥4.0/5.0 average
- **Measurement:** Optional survey after completion

**US-2: Net Promoter Score**
- **Question:** "How likely are you to recommend this simulation to a peer?" (0-10)
- **Target:** ≥50% Promoters (9-10 ratings)
- **Measurement:** Standard NPS calculation

---

### Instructor/Academic Metrics (Post-MVP)

**IA-1: Instructor Adoption Rate**
- **Definition:** % of LOG565 instructors at Norwegian business schools who assign it
- **Target:** ≥30% within 1 year of launch
- **Measurement:** Instructor surveys, student signup sources

**IA-2: Student Performance Correlation**
- **Definition:** Correlation between simulation completion and exam scores on planning questions
- **Target:** Positive correlation (r ≥0.3)
- **Measurement:** Partner with instructors to compare (anonymized data)
- **Why It Matters:** Validates educational effectiveness

---

### Technical Performance Metrics (MVP)

**TP-1: AI Response Time**
- **Definition:** Time from user message to AI response
- **Target:** ≤3 seconds (95th percentile)
- **Measurement:** Log timestamps in chat_logs
- **Why It Matters:** Maintains immersion and engagement

**TP-2: AI Response Quality (No Hallucinations)**
- **Definition:** % of AI responses that are factually accurate
- **Target:** ≥95%
- **Measurement:** Manual review of sample chats + user bug reports
- **Why It Matters:** Accuracy is non-negotiable for educational content

**TP-3: System Uptime**
- **Definition:** % of time app is available
- **Target:** ≥99.0%
- **Measurement:** Vercel analytics
- **Why It Matters:** Students may have assignment deadlines

---

## Development Timeline

### Simplified Architecture Timeline: 3-4 Weeks

**Week 1: Foundation (Static Data + Backend Core)**
- **Days 1-2:** Extract WBS from wbs.pdf into wbs.json (manual data entry)
- **Days 2-3:** Define supplier personas, write system_prompts in suppliers.json
- **Days 3-5:** Set up FastAPI, integrate PydanticAI, implement `/api/chat/message`
- **Days 5-7:** Prompt engineering and testing (quality, response time, guardrails)
- **Deliverable:** Backend responds to chat requests with persona-appropriate AI responses

---

**Week 2: Frontend Foundation + Auth**
- **Days 1-2:** Set up Next.js + React + Tailwind + Shadcn UI
- **Days 2-3:** Implement Supabase Auth (register, login, JWT handling)
- **Days 3-4:** Build Dashboard layout (Header, ConstraintPanel, QuickStats)
- **Days 4-5:** Build WBS View (list/tree, status indicators)
- **Days 5-7:** Implement localStorage utilities (save/load session, initialize)
- **Deliverable:** Users can register, login, see dashboard, browse WBS

---

**Week 3: Chat Interface + Plan Management**
- **Days 1-3:** Build Chat UI (ChatWindow, message bubbles, input, send)
- **Days 3-4:** Integrate chat with backend API, log to localStorage
- **Days 4-5:** Implement quote acceptance (commitment logic, update current_plan)
- **Days 5-6:** Build validation function (budget, timeline, dependencies)
- **Day 7:** Implement renegotiation (uncommit, recalculate)
- **Deliverable:** Full negotiation loop functional (chat → commit → validate)

---

**Week 4: Polish + Export + Testing**
- **Days 1-2:** Implement session export (JSON download)
- **Day 2:** Add loading states and error handling
- **Days 3-4:** Build submission flow (validation modal, success/failure screens)
- **Days 4-5:** End-to-end testing, bug fixes
- **Days 5-6:** User acceptance testing with 5-10 LOG565 students
- **Day 7:** Deploy to Vercel production, announce to instructors
- **Deliverable:** Shippable MVP

---

### Alternative Timeline (With Database): 5 Weeks

If we had chosen the database approach, add:
- **+1 week:** Database schema design, migrations, CRUD endpoints, testing
- **Total:** 5 weeks instead of 3-4

**Time saved with localStorage approach: 1-2 weeks**

---

## Key Decisions & Rationale

### Decision 1: localStorage Instead of Database

**Options Considered:**
- A) Full database (Supabase PostgreSQL)
- B) localStorage only
- C) Hybrid (localStorage + optional cloud sync)

**Decision:** B for MVP, C for post-MVP

**Rationale:**
- 45-60 min single-session use case doesn't require persistent database
- localStorage (5-10 MB) is sufficient for ~500 KB session data
- Saves 1-2 weeks development time
- Export-first design provides portfolio artifacts and instructor review capability
- Easy upgrade path: Can add Supabase Storage sync later

**Trade-offs Accepted:**
- ❌ No cross-device resume (user must complete on same device/browser)
- ❌ Data lost if user clears cache (mitigated by export reminders)
- ✅ Faster development, lower complexity, no database costs
- ✅ Full session export still provides all necessary persistence benefits

---

### Decision 2: Stateless Backend (Minimal API)

**Options Considered:**
- A) Stateful backend (session management, database CRUD)
- B) Stateless backend (AI proxy only)

**Decision:** B (Stateless)

**Rationale:**
- Frontend owns all data management (localStorage CRUD)
- Backend only needs to orchestrate AI calls
- Simplifies deployment, scaling, testing
- No session management complexity

**Implementation:**
- Frontend sends complete context with each API call (supplier data, WBS item, chat history)
- Backend constructs prompt and calls Gemini
- Backend returns AI response (no state stored)

**Trade-offs Accepted:**
- ❌ Slightly more data sent per request (frontend sends chat history)
- ✅ Much simpler backend, easier to scale, no database connection management

---

### Decision 3: Focus on Planning Phase Only

**Options Considered:**
- A) Full project lifecycle (planning, execution, monitoring, closing)
- B) Planning Phase only

**Decision:** B (Planning Phase only)

**Rationale:**
- Planning Phase is the most neglected in PM education (execution is well-covered)
- Negotiation and data validation are the hardest skills to teach
- Focused scope enables 3-4 week MVP (full lifecycle would be 3+ months)
- Can add execution phase post-MVP if there's demand

**Trade-offs Accepted:**
- ❌ Not a comprehensive PM simulation
- ✅ Depth over breadth: Do one thing (planning) extremely well

---

### Decision 4: Norwegian Language for UI and AI

**Options Considered:**
- A) Norwegian UI + AI
- B) English UI + AI
- C) Bilingual (user choice)

**Decision:** A (Norwegian) for MVP

**Rationale:**
- Target audience: Norwegian LOG565 students
- Case study (Hædda Barneskole) is Norwegian context
- Requirements and WBS documents are in Norwegian
- Higher authenticity and relevance

**Trade-offs Accepted:**
- ❌ Limits international scalability
- ✅ Better fit for target market
- ✅ Can add English version post-MVP (translation layer)

---

### Decision 5: Free Access (No Paywall)

**Options Considered:**
- A) Free for all users
- B) Freemium (limited sessions free, unlimited paid)
- C) Paid only (students or universities pay)

**Decision:** A (Free) for MVP

**Rationale:**
- Educational mission: Maximize access
- Easier adoption (no payment friction)
- Build user base and testimonials first
- Can explore monetization later (university licenses, premium features)

**Trade-offs Accepted:**
- ❌ No immediate revenue
- ✅ Faster adoption, larger user base, stronger testimonials
- ✅ Gemini API costs are low enough to sustain free tier (~1-2 NOK per session)

---

### Decision 6: Export as JSON (Not PDF)

**Options Considered:**
- A) JSON export only
- B) PDF export only
- C) Both JSON and PDF

**Decision:** A (JSON) for MVP, C for post-MVP

**Rationale:**
- JSON is easier to implement (no PDF formatting library needed)
- JSON is machine-readable (instructors can parse, analyze)
- JSON includes complete data (chat logs, plan history, metrics)
- PDF is "nice to have" for presentation but not essential

**Trade-offs Accepted:**
- ❌ JSON is less "professional-looking" than PDF report
- ✅ JSON is more comprehensive and flexible
- ✅ Students can convert JSON to PDF using online tools if needed
- ✅ Can add PDF export post-MVP (3-4 days of work)

---

### Decision 7: Client-Side Validation

**Options Considered:**
- A) Client-side validation (JavaScript)
- B) Server-side validation (FastAPI endpoint)
- C) Both (client for UX, server for security)

**Decision:** A (Client-side) for MVP

**Rationale:**
- Validation logic is not complex (sum costs, calculate critical path)
- Client-side provides instant feedback (no network round-trip)
- No security concern (session data is user's own, no competitive advantage to "cheating")
- Simpler architecture (one less backend endpoint)

**Trade-offs Accepted:**
- ❌ User could theoretically manipulate localStorage to bypass validation
- ✅ Not a real concern (honor system, exported JSON has timestamps)
- ✅ Faster feedback, simpler implementation

**Optional:** Add server-side validation post-MVP for instructor trust (validate exported JSON)

---

### Decision 8: Single Scenario (Hædda) Only

**Options Considered:**
- A) Single scenario (Hædda Barneskole)
- B) Multiple scenarios (hospital, bridge, office)

**Decision:** A (Single scenario) for MVP

**Rationale:**
- Hædda is already part of LOG565 curriculum (high relevance)
- Creating scenarios is time-intensive (WBS data entry, requirements extraction, supplier persona tuning)
- Better to perfect one scenario than have multiple mediocre ones
- Can add scenarios post-MVP if there's demand

**Trade-offs Accepted:**
- ❌ Limited replayability (once completed, less reason to play again)
- ✅ Ensures quality and depth
- ✅ Faster MVP delivery

---

## Conclusion

### What We're Building

An **AI-powered project management simulation** that teaches LOG565 students the soft skills that case studies can't: **negotiating with stakeholders, validating data, making trade-offs under constraints, and experiencing iterative planning.**

### Why It Matters

Traditional PM education has a **theory-practice gap**. Students learn Gantt charts and PERT but never practice the messy human interactions that make or break real projects. This simulation fills that gap.

### How We're Building It

**Simplified, pragmatic architecture:**
- localStorage (not database) for speed
- Stateless backend (just AI orchestration)
- Export-first design (JSON download for portfolios)
- 3-4 week MVP timeline

### Success Looks Like

- **60%+ completion rate** (challenging but achievable)
- **40%+ renegotiation rate** (experiencing iterative planning)
- **4.0+/5.0 satisfaction score** (students find it valuable)
- **Real learning transfer** (students reference simulation in exams/interviews)

### Next Steps

1. **Create PRD** (Product Requirements Document) from this synthesis
2. **Validate PRD** with stakeholders
3. **Begin development** (Week 1: Static data + backend)

---

**End of Executive Summary**

*This document synthesizes insights from 5 brainstorming sessions conducted during Phase 0 (Discovery & Analysis). All decisions are subject to validation during pilot testing and can be adjusted based on user feedback.*

**Prepared by:** BMAD System
**Date:** 2025-12-07
**Status:** Ready for PRD Development
