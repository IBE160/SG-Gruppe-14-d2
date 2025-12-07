# Research Report: Technical Validation and Competitive Analysis
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 1.0
**Research Date:** 2025-12-07
**Researcher:** Technical Analyst
**Status:** Complete

---

## Executive Summary

This research report validates critical technical assumptions and analyzes the competitive landscape for the Nye Hædda Barneskole Project Management Simulation. Three research areas were investigated:

1. **AI Prompt Engineering for Negotiation Agents** - Best practices for realistic role-playing AI
2. **localStorage Limits and Offline-First Patterns** - Technical validation of our architecture
3. **Competitive Analysis** - Existing PM simulation tools in educational market

**Key Findings:**
- ✅ Our AI supplier persona approach aligns with 2025 best practices (single-responsibility agents, tight personas)
- ✅ localStorage 5-10 MB assumption is valid (browser limit is 5-10 MB)
- ⚠️ Competitive tools exist but focus on process execution, not planning/negotiation
- ✅ Our Norwegian-language, AI-negotiation focus creates unique market position

**Critical Recommendations:**
1. Implement structured system prompts for each supplier persona (Section 2.4)
2. Add storage monitoring to prevent quota overflow (Section 3.4)
3. Differentiate from competitors by emphasizing AI negotiation realism (Section 4.5)

---

## Table of Contents

1. [Research Topic 1: AI Prompt Engineering for Negotiation Agents](#1-research-topic-1-ai-prompt-engineering-for-negotiation-agents)
2. [Research Topic 2: localStorage Limits and Offline-First Patterns](#2-research-topic-2-localstorage-limits-and-offline-first-patterns)
3. [Research Topic 3: Competitive Analysis of PM Simulation Tools](#3-research-topic-3-competitive-analysis-of-pm-simulation-tools)
4. [Synthesis and Recommendations](#4-synthesis-and-recommendations)
5. [Sources](#5-sources)

---

## 1. Research Topic 1: AI Prompt Engineering for Negotiation Agents

### 1.1 Research Objective

**Goal:** Validate our approach of using 5 distinct AI supplier personas and identify best practices for prompt engineering to ensure realistic negotiation behavior.

**Context:** Our PRD defines 5 supplier personas (Bjørn Eriksen, Kari Andersen, Per Johansen, Silje Henriksen, Tor Kristoffersen) with hidden parameters (initial_margin, concession_rate, patience). We need to ensure this approach aligns with 2025 AI agent best practices.

---

### 1.2 Key Findings

#### **Finding 1.1: Context Engineering Over Prompt Engineering**

**Source:** Anthropic Engineering (2025)

> "Context engineering moves beyond finding the right words for prompts to answering the broader question of 'what configuration of context is most likely to generate our model's desired behavior?'"

**Relevance:** Our approach of providing suppliers with WBS documents, requirement specs, and project context aligns with this. We're not just prompting "be a supplier," we're giving the AI the full context (documents, project constraints) to reason from.

**Recommendation:** ✅ Our document sidebar (Section 3.3 of UX Design) is validated—AI needs access to WBS, kravspec, project description.

---

#### **Finding 1.2: Tight Personas for Consistency**

**Source:** Lakera AI (2025), PromptHub (2025)

> "Defining tight personas leads to more tailored, context-specific responses. The tighter the persona, the more consistent the structure of the responses, especially for long-form answers such as sales negotiation preparation."

**Analysis:** Our 5 supplier personas are currently defined with:
- Name, company, role
- Personality traits (skeptical, optimistic, pragmatic)
- Hidden parameters (initial_margin: 1.15-1.30)

**Gap:** We lack explicit tone, voice style, and core philosophy for each persona.

**Recommendation:** ⚠️ Enhance persona definitions with:
- **Tone:** (e.g., "Professional but guarded" for Bjørn)
- **Voice Style:** (e.g., "Uses short sentences, cites experience" for Kari)
- **Core Philosophy:** (e.g., "Quality over speed" for Per)

---

#### **Finding 1.3: Single-Responsibility Agents**

**Source:** UiPath (2025)

> "Start with single-responsibility agents with one clear goal and narrow scope. Broad prompts decrease accuracy while narrow scopes ensure consistent performance."

**Relevance:** Each of our 5 suppliers has ONE goal: Negotiate the best deal for ONE WBS item.

**Validation:** ✅ Our approach is correct. Each AI agent is scoped to:
- Single WBS item negotiation
- Single supplier role
- Clear constraints (cost range, time range)

**Anti-pattern Avoided:** We're NOT using a single "general supplier AI" that handles all negotiations.

---

#### **Finding 1.4: Multi-Step Reasoning for Complex Tasks**

**Source:** The Agent Architect (2025)

> "System prompts should incorporate chain-of-thought style reasoning and explicitly define task decomposition, reasoning methods, and output formats."

**Application to Our Project:**

**Current Approach (Implicit):**
```
User: "Trenger pristilbud for Grunnarbeid"
AI: "120 MNOK, 3 måneder"
```

**Improved Approach (Explicit Reasoning):**
```
User: "Trenger pristilbud for Grunnarbeid"
AI Internal Reasoning (not shown to user):
1. Check WBS item requirements (F-003, K-023)
2. Calculate base cost from market rates
3. Apply initial_margin (1.20 for Bjørn)
4. Estimate duration based on dependencies
5. Formulate offer

AI Response: "Basert på spesifikasjonene (F-003, K-023) estimerer jeg 120 MNOK og 3 måneder."
```

**Recommendation:** ⚠️ Update system prompts to include explicit reasoning steps (for internal coherence, not user-facing).

---

#### **Finding 1.5: AI as Behind-the-Scenes Advisor (Not Participant)**

**Source:** Harvard PON AI Negotiation Summit (MIT, March 2025)

> "AI can add value to negotiations by offering advice, assistance, training, and research support. Many presenters described how AI can serve as a behind-the-scenes advisor."

**Note:** This finding is about AI assisting human negotiators, not AI as negotiation counterpart.

**Relevance to Our Project:** We're inverting this—AI IS the negotiation counterpart. This is intentional for educational purposes (students practice negotiating WITH AI, not being advised BY AI).

**Validation:** ✅ Our approach is valid for learning context. Students need to practice negotiation skills, not rely on AI advisors.

---

### 1.3 Validated Best Practices for Our AI Suppliers

| Best Practice | Our Current Approach | Status | Action Needed |
|--------------|---------------------|--------|---------------|
| **Context Engineering** | Documents sidebar (WBS, kravspec) | ✅ GOOD | None |
| **Tight Personas** | 5 distinct suppliers with traits | ⚠️ PARTIAL | Add tone, voice, philosophy |
| **Single-Responsibility** | 1 supplier = 1 WBS item | ✅ GOOD | None |
| **Multi-Step Reasoning** | Implicit in prompts | ⚠️ PARTIAL | Add explicit reasoning steps |
| **Structured Output** | Cost + duration format | ✅ GOOD | None |

---

### 1.4 Recommended System Prompt Structure

Based on 2025 best practices, here's a template for our supplier personas:

```markdown
# System Prompt: Bjørn Eriksen - Totalentreprenør

## Role and Identity
You are Bjørn Eriksen, owner of Totalentreprenør AS, a well-established Norwegian construction company. You specialize in large-scale groundwork and foundation projects.

## Personality and Communication Style
- **Tone:** Professional, slightly cautious, experienced
- **Voice:** Direct, uses short sentences, often references past projects
- **Philosophy:** "Kvalitet tar tid, men varer lenger" (Quality takes time, but lasts longer)
- **Demeanor:** Skeptical of tight deadlines, values thoroughness over speed

## Negotiation Parameters (HIDDEN from user)
- initial_margin: 1.20 (20% markup on base cost)
- concession_rate: 0.05 (willing to reduce 5% per negotiation round)
- patience: 3 (will walk away after 3 rounds if demands unreasonable)
- min_acceptable_margin: 1.10 (10% minimum profit)

## Task Instructions
1. **Receive Request:** User asks for quote on specific WBS item
2. **Analyze Requirements:** Review WBS description, kravspec (F-codes, K-codes)
3. **Calculate Base Cost:** Use market rates for materials, labor, equipment
4. **Apply Markup:** Add initial_margin to base cost
5. **Estimate Duration:** Consider dependencies, resource availability
6. **Formulate Offer:** Present cost and duration with brief justification
7. **Negotiate:** If user pushes back:
   - Round 1: Reduce by concession_rate (to 1.15 margin)
   - Round 2: Reduce by concession_rate again (to 1.10 margin)
   - Round 3: Hold firm or walk away if below min_acceptable_margin

## Reasoning Structure (Internal)
For each response, think through:
1. What are the technical requirements? (F-codes, K-codes)
2. What is the base cost estimate?
3. What margin am I applying?
4. How does this compare to user's expectations?
5. Am I being reasonable given project constraints?

## Output Format
Always structure offers as:
"Basert på [reason], estimerer jeg [cost] MNOK og [duration] måneder."

Example:
"Basert på kravspesifikasjon F-003 (fundamental depth 1.5m) og K-023 (quality grade A), estimerer jeg 120 MNOK og 3 måneder for Grunnarbeid."

## Norwegian Language
- Use formal "De" or informal "du" based on user's approach
- Use Norwegian construction terminology (grunnarbeid, råbygg, etc.)
- Be culturally appropriate (Norwegian business norms: direct but polite)

## Constraints
- Never reveal hidden parameters (initial_margin, concession_rate)
- Stay in character at all times
- Only negotiate for assigned WBS item
- If user asks about other items, redirect: "Det må du diskutere med [other supplier]"
```

**Time Investment:** Creating 5 detailed system prompts (1-2 hours per prompt) = 5-10 hours total

**ROI:** High—realistic AI behavior is critical to learning objectives

---

### 1.5 Prompt Engineering Timeline

Based on PRD Section 13 (Dependencies), we have 1 week allocated for prompt engineering (Week 3). Research suggests this is TIGHT but feasible.

**Week 3 Recommended Schedule:**
- **Day 1-2:** Draft 5 system prompts using template above
- **Day 3:** Test with 10 sample negotiations (2 per supplier)
- **Day 4:** Tune concession_rate and patience based on test results
- **Day 5:** Final validation with edge cases (unreasonable demands, perfect alignment)

**Backup Plan:** If 1 week insufficient, reduce to 3 suppliers (Bjørn, Kari, Per) to simplify testing.

---

## 2. Research Topic 2: localStorage Limits and Offline-First Patterns

### 2.1 Research Objective

**Goal:** Validate our assumption that localStorage (5-10 MB) is sufficient for storing game session data and identify potential pitfalls.

**Context:** Our architecture uses localStorage for:
- WBS items (15 items × ~200 bytes = 3 KB)
- Suppliers (5 suppliers × ~300 bytes = 1.5 KB)
- Chat logs (100 messages × ~500 bytes = 50 KB)
- Plan history (20 entries × ~400 bytes = 8 KB)
- Total estimate: ~62 KB per session

**Question:** Is 5-10 MB limit safe? What are edge cases?

---

### 2.2 Key Findings

#### **Finding 2.1: localStorage Limit is 5-10 MB Across Browsers**

**Source:** Stack Overflow (2025), MDN Web Docs (2025)

> "localStorage is limited to 10 MiB of data maximum on all browsers, with browsers able to store up to 5 MiB of local storage per origin. In practice, approximately 5,200,000 characters can be stored successfully across all top browsers."

**Calculation:**
- 5 MB = 5,000,000 bytes
- UTF-16 encoding (JavaScript default) = 2 bytes per character
- Effective storage: ~2.5 million characters or 5 MB

**Our Usage:**
- 62 KB per session (conservative estimate)
- 5 MB / 62 KB = ~80 sessions
- Single session duration: 45-60 minutes
- Users unlikely to store >80 sessions (would require 60+ hours of usage)

**Validation:** ✅ Our 5-10 MB assumption is VERY SAFE. Even with 50% overhead for JSON serialization, we can store 40+ sessions.

---

#### **Finding 2.2: localStorage is Synchronous and Blocks Main Thread**

**Source:** LogRocket (2025), RxDB (2025)

> "localStorage operates as a non-async blocking API, which means operations can potentially block the main thread, leading to slower application performance. Both sessionStorage and localStorage are synchronous in nature, blocking the execution of other JavaScript code until operations are completed."

**Relevance:** Our app reads/writes localStorage on:
- Page load (read entire session)
- Quote acceptance (write plan update)
- Plan submission (read entire session for validation)

**Risk:** If session data is large (e.g., 500 KB JSON), synchronous parse could freeze UI for 10-50ms.

**Mitigation (PRD NFR-1):** "UI responses within 2 seconds" already accounts for this. localStorage read/write is <100ms even for large sessions.

**Recommendation:** ✅ No action needed. Our session sizes (62 KB) are small enough that synchronous operations are imperceptible.

---

#### **Finding 2.3: Lack of Indexing and Search**

**Source:** RxDB (2025)

> "Lack of indexing capabilities, making it challenging to perform efficient searches or iterate over data based on specific criteria."

**Relevance:** We're NOT searching across sessions. Each session is isolated (single game instance). When user loads app:
1. Check localStorage for `current_session_id`
2. Load that session's data
3. Render

**Validation:** ✅ No indexing needed for our use case.

---

#### **Finding 2.4: Multi-Tab Performance Issues**

**Source:** RxDB (2025)

> "In multi-tab environments, one tab's localStorage operations can impact the performance of other tabs."

**Relevance:** Users unlikely to run 2 simultaneous game sessions. However, if they open Dashboard in Tab 1 and Chat in Tab 2 (same session), both tabs access same localStorage.

**Edge Case:** User accepts quote in Tab 2 (chat) → localStorage updated → Tab 1 (dashboard) shows stale data.

**Solution:** Use `storage` event listener to sync tabs:
```javascript
window.addEventListener('storage', (e) => {
  if (e.key === 'current_session') {
    // Reload session data
    loadSession();
  }
});
```

**Recommendation:** ⚠️ Add multi-tab sync to PRD (FR-9: Real-time updates across tabs). Low priority for MVP, document as known limitation.

---

#### **Finding 2.5: Offline-First Patterns for 2025**

**Source:** LogRocket (2025)

> "In 2025, offline-first is a core pillar of resilient user experience design. Key patterns include:
> - Cache-First Fetching: Service workers serve responses from cache immediately
> - Client-First Updates: User actions update local state immediately
> - Storage Monitoring: Proactively checking storage usage and warning users when approaching limits"

**Relevance:** Our architecture is already client-first (localStorage updates immediately, no backend sync for MVP).

**Gap:** We lack storage monitoring.

**Recommendation:** ⚠️ Add storage quota check:
```javascript
function checkStorageQuota() {
  const used = JSON.stringify(localStorage).length;
  const limit = 5000000; // 5 MB
  const percentage = (used / limit) * 100;

  if (percentage > 80) {
    console.warn(`localStorage 80% full (${used} / ${limit} bytes)`);
    // Show warning toast to user
  }
}
```

---

#### **Finding 2.6: IndexedDB as Alternative for Larger Datasets**

**Source:** LogRocket (2025), MDN (2025)

> "IndexedDB may be more suitable for scenarios where performance is a concern or when dealing with larger datasets, allowing for non-blocking operations."

**Relevance:** If we expand beyond MVP (e.g., store 100+ sessions, multi-user scenarios), IndexedDB would be better.

**Decision for MVP:** ✅ localStorage is sufficient. IndexedDB adds complexity (async API, IndexedDB wrapper library) without clear benefit for 62 KB sessions.

**Post-MVP:** Consider IndexedDB if:
- Multi-session history (user wants to review past 50 games)
- Export feature creates large JSON files (>500 KB)
- Analytics tracking requires storing detailed event logs

---

### 2.3 Validation of Our Architecture Decision

| Architecture Decision | Research Validation | Status |
|----------------------|-------------------|--------|
| **localStorage for session data** | 5-10 MB limit sufficient for 40+ sessions | ✅ VALID |
| **No database for MVP** | Saves 1-2 weeks dev time, acceptable tradeoff | ✅ VALID |
| **Export-first design** | Aligns with offline-first 2025 patterns | ✅ VALID |
| **Single-session focus** | No indexing/search needed | ✅ VALID |
| **Synchronous operations** | <100ms for 62 KB data, acceptable | ✅ VALID |

**Overall Assessment:** ✅ Our localStorage-based architecture is well-justified and aligns with 2025 web app best practices for offline-first, single-session applications.

---

### 2.4 Recommended Enhancements

**Priority: Low (Post-MVP)**

1. **Storage Monitoring:**
   - Add quota check on app load
   - Warn user at 80% capacity
   - Offer to clear old sessions

2. **Multi-Tab Sync:**
   - Listen for `storage` events
   - Reload session data when another tab updates

3. **Graceful Degradation:**
   - If localStorage full, offer to export current session and clear storage
   - Prevent data loss with try/catch on localStorage.setItem()

**Implementation Time:** 2-3 hours total

**ROI:** Low for MVP (edge cases), Medium for production (user trust)

---

## 3. Research Topic 3: Competitive Analysis of PM Simulation Tools

### 3.1 Research Objective

**Goal:** Identify existing PM simulation tools in the educational market and analyze how our product differentiates.

**Questions:**
1. What PM simulation tools exist for university education?
2. What features do they offer?
3. How does Nye Hædda Barneskole compare?
4. What is our unique value proposition?

---

### 3.2 Competitive Landscape

#### **Competitor 1: MIT Sloan Project Management Simulation**

**Source:** MIT Sloan Teaching Resources Library (2025), Forio (2025)

**Description:** "A realistic, interactive system dynamics 'management flight simulator' in which participants play the role of project managers for a complex project. Used by thousands of people, from undergraduates to seasoned project managers and executives."

**Key Features:**
- System dynamics model (scope, resources, schedule)
- Real-time decision-making
- Complexity management (scope creep, resource allocation)
- Time-based progression (project execution phases)

**Target Audience:** MBA students, executives, seasoned PMs

**Pricing:** Not publicly listed (enterprise licensing)

**Strengths:**
- ✅ Established brand (MIT Sloan)
- ✅ Used by thousands globally
- ✅ Realistic system dynamics

**Weaknesses:**
- ❌ Focus on EXECUTION, not planning
- ❌ No AI negotiation component
- ❌ English-only (not localized for Norwegian)
- ❌ Complex interface (steep learning curve)

---

#### **Competitor 2: Cesim Project Management Simulation**

**Source:** Cesim (2025)

**Description:** "A team-based, interactive project management simulation that allows participants to experience the dynamics of managing a project that is part of a broader, multi-project program with interdependent projects."

**Key Features:**
- Multi-project program management
- Team-based collaboration
- Interdependencies between projects
- Competitive element (teams compete)

**Target Audience:** University business schools, executive education

**Pricing:** Enterprise licensing (used by Tampere University, EDHEC, Coventry University)

**Strengths:**
- ✅ Team collaboration focus
- ✅ Multi-project complexity
- ✅ Used by reputable universities

**Weaknesses:**
- ❌ Focus on EXECUTION and monitoring
- ❌ No procurement/negotiation phase
- ❌ Generic scenarios (not Norwegian construction context)
- ❌ Requires facilitator/instructor

---

#### **Competitor 3: SimProject (Simulation Powered Learning)**

**Source:** SimProject (2025)

**Description:** "Equips learners with real tools like Project Charters, Gantt Charts, and Work Breakdown Structures, all within a live, interactive simulation. Entirely web-based, no software installation needed."

**Key Features:**
- Project charter creation
- Gantt chart interaction
- WBS development
- Risk management tools

**Target Audience:** Undergraduate PM courses, certificate programs

**Pricing:** Web-based subscription model

**Strengths:**
- ✅ Web-based (no installation)
- ✅ Focus on PM TOOLS (charters, WBS, Gantt)
- ✅ Beginner-friendly

**Weaknesses:**
- ❌ Tool-focused, not scenario-driven
- ❌ No AI interaction
- ❌ Static learning (not dynamic negotiation)
- ❌ Generic scenarios

---

#### **Competitor 4: GoVenture Project Management**

**Source:** GoVenture (2025)

**Description:** "Simulation and video-based training experience for learning and practicing project management designed for schools, universities, nonprofits, and businesses."

**Key Features:**
- Video-based training modules
- Interactive decision points
- Project lifecycle simulation
- Cost/time tracking

**Target Audience:** K-12, universities, nonprofits

**Pricing:** Institutional licensing

**Strengths:**
- ✅ Video-based (multimedia learning)
- ✅ Accessible for beginners
- ✅ Full project lifecycle

**Weaknesses:**
- ❌ Video-based = less interactive
- ❌ No AI negotiation
- ❌ Generic scenarios (not contextualized)
- ❌ Focus on process, not planning decisions

---

### 3.3 Competitive Feature Matrix

| Feature | MIT Sloan | Cesim | SimProject | GoVenture | **Nye Hædda** |
|---------|-----------|-------|------------|-----------|---------------|
| **Phase Focus** | Execution | Execution | Tools | Lifecycle | **PLANNING** ✅ |
| **AI Negotiation** | ❌ | ❌ | ❌ | ❌ | **✅ 5 AI suppliers** |
| **Norwegian Language** | ❌ | ❌ | ❌ | ❌ | **✅ nb_NO** |
| **Realistic Context** | Generic | Generic | Generic | Generic | **✅ Norwegian construction** |
| **Single-Player** | ✅ | ❌ Team | ✅ | ✅ | **✅** |
| **Web-Based** | ✅ | ✅ | ✅ | ✅ | **✅** |
| **Procurement Focus** | ❌ | ❌ | ❌ | ❌ | **✅** |
| **WBS Integration** | Partial | Partial | ✅ | Partial | **✅ From PDF** |
| **Time Commitment** | 2-4 hours | 4-8 hours | 1-2 hours | 2-3 hours | **45-60 min** ✅ |
| **Beginner-Friendly** | ❌ | ❌ | ✅ | ✅ | **✅** |

---

### 3.4 Market Gaps Identified

**Gap 1: PLANNING Phase Neglected**
- All competitors focus on execution, monitoring, or tool usage
- NONE focus on the critical planning phase (procurement, resource allocation, constraint balancing)

**Gap 2: No AI-Powered Negotiation**
- Existing tools use static scenarios or pre-programmed responses
- No tools leverage modern LLMs for realistic, adaptive negotiation

**Gap 3: Generic Scenarios**
- Most tools use generic "software development" or "product launch" scenarios
- None contextualized to specific industries (construction, healthcare, etc.)

**Gap 4: Norwegian Language**
- All identified tools are English-only
- Norwegian universities must use translated materials or teach in English

**Gap 5: Long Time Commitment**
- Existing simulations require 2-8 hours (full class session or homework)
- Difficult to integrate into single 90-minute lecture

---

### 3.5 Our Unique Value Proposition

**Nye Hædda Barneskole fills 5 market gaps:**

1. **Planning-Phase Focus** - Only tool focused on procurement and constraint balancing
2. **AI Negotiation** - Realistic, adaptive supplier personas powered by Gemini 2.5
3. **Norwegian Context** - Localized language, realistic Norwegian construction scenario
4. **Procurement Emphasis** - Deep focus on supplier selection, negotiation, renegotiation
5. **Time-Efficient** - 45-60 minute experience fits within single lecture

**Target Market:** Norwegian universities (NTNU, UiO, UiB, HiOA) teaching PM courses

**Competitive Positioning:**
- vs. MIT Sloan: More accessible, Norwegian context, planning focus
- vs. Cesim: Single-player, Norwegian, planning vs execution
- vs. SimProject: AI-driven vs static, scenario-driven vs tool-driven
- vs. GoVenture: Interactive negotiation vs video-based

---

### 3.6 Competitive Threats

**Threat 1: MIT Sloan Brand**
- Prestigious brand may attract Norwegian universities despite language barrier
- Mitigation: Emphasize Norwegian context, local relevance

**Threat 2: Cesim Expansion**
- Cesim could add planning phase or Norwegian localization
- Mitigation: First-mover advantage, AI negotiation hard to replicate

**Threat 3: AI Tools Becoming Commodity**
- If all tools add AI negotiation, our differentiation weakens
- Mitigation: Focus on Norwegian context + specific construction scenario

**Threat 4: OpenProject/Trello for Real Projects**
- Universities may prefer students work on REAL projects vs simulations
- Mitigation: Simulation allows controlled learning, no real-world consequences

---

### 3.7 Market Opportunity

**Total Addressable Market (TAM):**
- Norwegian universities with PM courses: ~10 institutions
- Students per year: ~500-1,000 students (estimate)
- Potential expansion: Other Nordic countries (Sweden, Denmark), other industries (IT, healthcare)

**Strategic Positioning:**
- Start: Norwegian universities, construction PM courses
- Expand: Nordic region, other engineering disciplines
- Long-term: Global market with localized scenarios (UK construction, US healthcare)

---

## 4. Synthesis and Recommendations

### 4.1 Cross-Topic Insights

**Insight 1: AI Negotiation is Our Killer Feature**
- Research confirms: No competitor has AI-powered negotiation
- 2025 best practices: We can implement this realistically
- Recommendation: ✅ Double down on AI quality—this is our moat

**Insight 2: Technical Architecture is Sound**
- localStorage validated as sufficient for our use case
- Offline-first patterns align with 2025 best practices
- Recommendation: ✅ Proceed with current architecture, no changes needed

**Insight 3: Norwegian Context is Underserved**
- Market gap: All tools are English-only
- Local relevance: Nye Hædda scenario resonates with Norwegian students
- Recommendation: ✅ Emphasize Norwegian language and context in marketing

---

### 4.2 Critical Recommendations

#### **Recommendation 1: Invest in AI Prompt Engineering (HIGH PRIORITY)**

**Action:** Allocate 1 week (Week 3) to create 5 detailed system prompts using template in Section 1.4

**Justification:**
- AI negotiation is our unique differentiator
- 2025 best practices require tight personas, structured reasoning
- Competitors cannot easily replicate this

**Success Criteria:**
- Each supplier feels distinct (personality, tone, negotiation style)
- Students cannot "game" the AI with simple prompts
- Negotiations feel realistic and challenging

**Time Investment:** 5-10 hours
**ROI:** High—core value proposition depends on this

---

#### **Recommendation 2: Add Storage Monitoring (MEDIUM PRIORITY)**

**Action:** Implement localStorage quota check (Section 2.5, Finding 2.5)

**Justification:**
- Prevents silent failures when storage full
- Aligns with 2025 offline-first best practices
- Low effort (2-3 hours), high reliability gain

**Success Criteria:**
- User warned at 80% capacity
- Graceful fallback (offer to export + clear storage)

**Time Investment:** 2-3 hours
**ROI:** Medium—edge case, but critical for user trust

---

#### **Recommendation 3: Emphasize Planning Focus in Marketing (HIGH PRIORITY)**

**Action:** Position product as "Only PM simulation focused on PLANNING, not execution"

**Justification:**
- Market gap: All competitors focus on execution
- Students need planning skills (often neglected in curriculum)
- Clear differentiation in crowded market

**Marketing Message:**
> "While other tools teach you to EXECUTE a project, Nye Hædda teaches you to PLAN one—the most critical phase where success is determined."

**Time Investment:** N/A (marketing, not development)
**ROI:** High—clarifies unique value proposition

---

#### **Recommendation 4: Document Multi-Tab Limitation (LOW PRIORITY)**

**Action:** Add to PRD Known Limitations: "Multi-tab sync not supported in MVP"

**Justification:**
- Edge case (users unlikely to open 2 tabs)
- Solution exists (storage event listener) but adds complexity
- Transparent documentation builds trust

**Time Investment:** 10 minutes (documentation)
**ROI:** Low—edge case, but good practice

---

### 4.3 Risk Mitigation

**Risk 1: AI Negotiation Not Realistic Enough**
- **Probability:** Medium (30%)
- **Impact:** High (core feature fails)
- **Mitigation:**
  - Allocate full week to prompt engineering (Week 3)
  - Test with 10 sample negotiations per supplier
  - Have backup plan: Reduce to 3 suppliers if tuning takes longer

**Risk 2: Competitors Add AI Negotiation**
- **Probability:** Low (10% in next 12 months)
- **Impact:** Medium (reduces differentiation)
- **Mitigation:**
  - First-mover advantage: Build brand with Norwegian universities
  - Norwegian context still differentiates even if AI becomes commodity
  - Continuous improvement: Keep enhancing AI personas

**Risk 3: localStorage Insufficient for Future Features**
- **Probability:** Low (20% if we expand beyond MVP)
- **Impact:** Medium (requires architecture change)
- **Mitigation:**
  - Current usage (62 KB) well below limit (5 MB)
  - If needed, migrate to IndexedDB post-MVP (3-5 days work)
  - Export-first design means no data lock-in

---

### 4.4 Success Metrics

To validate research assumptions, track these metrics during pilot testing:

**AI Negotiation Quality:**
- Student feedback: "AI felt realistic" (target: >80% agree)
- Negotiation rounds: Average 2-3 rounds per WBS item (indicates challenge)
- Detection: Students unable to "break" AI with edge cases

**Technical Performance:**
- localStorage usage: <100 KB per session (current estimate: 62 KB)
- Load times: <2 seconds (current NFR)
- No localStorage quota errors during 10-student pilot

**Market Differentiation:**
- Survey: "What makes Nye Hædda different from other PM tools?" → Planning focus, AI negotiation (target: >70% mention)

---

## 5. Sources

### AI Prompt Engineering for Negotiation Agents

- [The Ultimate Guide to Prompt Engineering in 2025 | Lakera](https://www.lakera.ai/blog/prompt-engineering-guide)
- [PromptHub Blog: Prompt Engineering for AI Agents](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents)
- [Effective context engineering for AI agents | Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Introduction to AI Agents | Prompt Engineering Guide](https://www.promptingguide.ai/agents/introduction)
- [Prompt Engineering in 2025: Tips + Best Practices | Orq.ai](https://orq.ai/blog/what-is-the-best-way-to-think-of-prompt-engineering)
- [Best practices for LLM prompt engineering | Palantir](https://www.palantir.com/docs/foundry/aip/best-practices-prompt-engineering)
- [Technical Tuesday: 10 best practices for building reliable AI agents in 2025 | UiPath](https://www.uipath.com/blog/ai/agent-builder-best-practices)
- [4 Essential Tips for Writing System Prompts That Make Your AI Agents Actually Work | The Agent Architect](https://theagentarchitect.substack.com/p/4-tips-writing-system-prompts-ai-agents-work)
- [From Agent to Advisor: How AI Is Transforming Negotiation | Harvard PON](https://www.pon.harvard.edu/daily/negotiation-skills-daily/from-agent-to-advisor-how-ai-is-transforming-negotiation/)
- [Best AI Prompt Engineering Techniques in 2025 for Precision Output | Kanerika](https://kanerika.com/blogs/ai-prompt-engineering-best-practices/)

### localStorage Limits and Offline-First Patterns

- [Offline-first frontend apps in 2025: IndexedDB and SQLite in the browser and beyond | LogRocket](https://blog.logrocket.com/offline-first-frontend-apps-2025-indexeddb-sqlite/)
- [Using localStorage in Modern Applications - A Comprehensive Guide | RxDB](https://rxdb.info/articles/localstorage.html)
- [What is the max size of localStorage values? | Stack Overflow](https://stackoverflow.com/questions/2989284/what-is-the-max-size-of-localstorage-values)
- [Storage quotas and eviction criteria | MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)
- [Client-side storage | MDN Learn](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Client-side_APIs/Client-side_storage)
- [Web Storage API | MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
- [Understanding Browser Storage APIs: A Guide for Web Developers in 2025 | RDPCore](https://blog.rdpcore.com/en/understanding-browser-storage-apis-a-guide-for-web-developers-in-2025)
- [Browser Storage Types and Their Maximum Limits | DEV Community](https://dev.to/vishwas/browser-storage-types-and-their-maximum-limits-174f)
- [Please Stop Using Local Storage | Randall Degges](https://www.rdegges.com/2018/please-stop-using-local-storage/)
- [Managing HTML5 Offline Storage | Chrome for Developers](https://developer.chrome.com/docs/apps/offline_storage)

### Competitive Analysis of PM Simulation Tools

- [Simulation Powered Learning - Learn By Doing (SimProject)](https://simulationpl.com/)
- [18 Best Project Management Software For Education In 2025 | The Digital Project Manager](https://thedigitalprojectmanager.com/tools/best-project-management-software-for-education/)
- [Project Management Business Simulation | Cesim Project](https://www.cesim.com/simulations/cesim-project-management-simulation)
- [Project Management Training Simulation for Education | GoVenture](https://www.goventure.net/pm)
- [Project Management Simulation | MIT Sloan](https://mitsloan.mit.edu/teaching-resources-library/project-management-simulation)
- [Simulation-Based Training in Project Management Education | PMI](https://www.pmi.org/learning/library/simulation-based-training-project-management-education-6342)
- [Project management software for universities | OpenProject](https://www.openproject.org/project-management-universities-research/)
- [Best Simulation Software with Project Management 2025 | GetApp](https://www.getapp.com/it-management-software/simulation/f/project-notes/)
- [Project Management Simulation: Scope, Resources, Schedule | Forio](https://forio.com/store/harvard-project-management-simulation/)
- [Education Project Management Software | Zoho Projects](https://www.zoho.com/projects/education-project-management.html)

---

**End of Research Report**

**Next Steps:**
1. Incorporate recommendations into PRD (if not already covered)
2. Use AI prompt template (Section 1.4) during Week 3 implementation
3. Add storage monitoring to technical backlog (Section 2.5)
4. Update marketing materials to emphasize planning focus (Section 4.2)

**Document Status:** Complete and ready for stakeholder review.
