# UX/UI Flow Diagrams - Complete Index

**Location:** `/docs/ux/flows/`
**Created:** 2025-12-12
**Purpose:** Detailed technical flow diagrams for frontend developers

---

## 📁 QUICK ACCESS

### Flow Diagrams (7 files):

1. **[flow-01-validation-rules.svg](flows/flow-01-validation-rules.svg)** - Budget & time validation logic
2. **[flow-02-budget-calculation.svg](flows/flow-02-budget-calculation.svg)** - 3-tier budget model calculation
3. **[flow-03-ai-agent-negotiation.svg](flows/flow-03-ai-agent-negotiation.svg)** - AI agent negotiation rules
4. **[flow-04-commitment-uncommitment.svg](flows/flow-04-commitment-uncommitment.svg)** - Accept/reject flow
5. **[flow-05-state-management.svg](flows/flow-05-state-management.svg)** - Frontend/backend sync
6. **[flow-06-error-handling.svg](flows/flow-06-error-handling.svg)** - Error messages & modals
7. **[flow-07-critical-path-timeline.svg](flows/flow-07-critical-path-timeline.svg)** - CPM timeline calculation

### Visualizations (2 files):

8. **[visualization-01-gantt-chart.svg](flows/visualization-01-gantt-chart.svg)** - Gantt chart (15 WBS packages)
9. **[visualization-02-precedence-diagram.svg](flows/visualization-02-precedence-diagram.svg)** - Precedence diagram (AON)

### Documentation:

- **[README.md](flows/README.md)** - Complete guide to all flow diagrams
- **[FLOW_CREATION_SUMMARY.md](flows/FLOW_CREATION_SUMMARY.md)** - Creation summary & verification

---

## 🎯 WHAT THESE FLOWS COVER

### Business Rules & Game Logic:

- ✅ Budget constraints (390/310/700 MNOK)
- ✅ 35 MNOK deficit challenge
- ✅ Timeline constraints (15 May 2026 deadline - INFLEXIBLE)
- ✅ AI agent negotiation rules (hidden parameters, concession rates)
- ✅ Validation rules (budget + time)
- ✅ Critical path calculation (CPM method)

### User Interaction Flows:

- ✅ Commitment flow (explicit accept with modal confirmation)
- ✅ Uncommitment flow (revert with warning modal)
- ✅ Error handling (user-friendly Norwegian messages)
- ✅ State management (optimistic updates, sync patterns)

### Technical Implementation:

- ✅ Code examples (TypeScript/JavaScript)
- ✅ API endpoint specifications
- ✅ Database schema interfaces
- ✅ React state structure
- ✅ Calculation formulas

---

## 💡 HOW TO USE

### For Frontend Developers:

**Building UI components?**
→ See `flow-02-budget-calculation.svg` for progress bars and budget display
→ See `flow-04-commitment-uncommitment.svg` for modal design
→ See `flow-06-error-handling.svg` for error message format

**Managing state?**
→ See `flow-05-state-management.svg` for React state structure

**Need validation?**
→ See `flow-01-validation-rules.svg` for client-side validation rules

### For Backend Developers:

**Building API?**
→ See `flow-01-validation-rules.svg` for server-side validation
→ See `flow-03-ai-agent-negotiation.svg` for Google Gemini integration
→ See `flow-05-state-management.svg` for session management

**Calculating timeline?**
→ See `flow-07-critical-path-timeline.svg` for CPM algorithm

### For QA/Testing:

**Creating test cases?**
→ All flows document edge cases and validation rules
→ Use error scenarios from `flow-06-error-handling.svg`
→ Test budget calculations from `flow-02-budget-calculation.svg`

---

## 🔑 KEY CONCEPTS

### Budget Model (3-Tier):

```
Tier 1: Tilgjengelig (0-310 MNOK)     → Dynamisk, endres ved commitment
Tier 2: Låst (390 MNOK)               → Konstant, endres aldri
Tier 3: Totalt (390 + used)           → Dynamisk, valideres mot 700 MNOK
```

### Validation Rules:

```
Budget: total ≤ 700 MNOK (hard limit)
Time:   project_end ≤ 15 May 2026 (inflexible)
```

### Critical Path:

```
WBS 1.3.1 (Grunnarbeid)      60 days
    ↓ (finish-to-start)
WBS 1.3.2 (Fundamentering)   45 days
    ↓ (finish-to-start)
WBS 1.4.1 (Råbygg)           90 days
────────────────────────────────────
Total Critical Path:         195 days (baseline)
```

### AI Agent Rules:

```
Suppliers (3):
- Can negotiate: Price, quality, duration
- Cannot: Change scope (requires Owner approval)
- Minimum price: 85-88% of baseline
- Become firmer after 3-4 negotiation rounds

Owner (1):
- Can approve: Budget increase (max 15% = 47 MNOK), scope reduction
- Cannot: Time extension (NEVER ALLOWED)
- Requires: Strong justification for budget increase
```

---

## ✅ VERIFICATION

All flow diagrams are:

- ✅ **Consistent** with PRD.md budget model (390/310/700 MNOK)
- ✅ **Complete** - All critical rules documented
- ✅ **Accurate** - Verified against AI_AGENT_SYSTEM_PROMPTS.md
- ✅ **Production-ready** - Includes concrete code examples
- ✅ **Bilingual** - Norwegian for UI, English for code

---

## 🔗 RELATED FILES

### Main Mockups:

- `/docs/ux/final-screen-02-dashboard-main.svg` - Dashboard with 3-tier budget
- `/docs/ux/final-screen-03-chat-interface.svg` - Chat with accept/reject buttons
- `/docs/ux/final-flow-01-complete-user-journey.svg` - Complete user journey
- `/docs/ux/final-flow-03-negotiation-strategies.svg` - 3 negotiation strategies

### Core Documentation:

- `/docs/PRD.md` - Product Requirements Document
- `/docs/AI_AGENT_SYSTEM_PROMPTS.md` - AI agent system prompts
- `/docs/ux-design-specification.md` - UX design specifications
- `/docs/BUDGET_MODEL_VERIFICATION.md` - Budget model verification report

### Implementation Plans:

- `/docs/IMPLEMENTATION_PLAN_DEC_9-15.md` - Sprint 1-2 plan
- `/docs/REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md` - Sprint 1-4 roadmap

---

## 📊 FILE STATISTICS

**Total files:** 11 (9 SVG + 2 MD)
**Total size:** ~135 KB
**Lines of documentation:** ~2,000+
**Code examples:** 50+
**Business rules documented:** 30+

---

## 🎯 CONCLUSION

These flow diagrams provide **complete technical specifications** for implementing the Nye Hædda Barneskole POC.

**Use these flows to:**

- ✅ Understand all business rules and game logic
- ✅ Implement frontend components (UI, state, validation)
- ✅ Build backend API (validation, AI integration, database)
- ✅ Create comprehensive test cases
- ✅ Onboard new developers quickly

**All flows are production-ready and can be used directly in Sprint 1-4 implementation.**

---

**Created:** 2025-12-12
**Location:** `/docs/ux/flows/`
**Status:** Complete ✅
