# Nye Hædda Barneskole - AI Project Management Simulation

**Course:** IBE160 Programmering med KI
**Group:** SG-Gruppe-14-d2
**Project Status:** POC Development Phase
<!-- LAST_UPDATED_START -->
Last Updated: 2025-12-16 00:17:09
<!-- LAST_UPDATED_END -->

---

## Project Overview

An AI-powered educational simulation teaching project management negotiation skills through realistic AI agent interactions. Students act as Project Manager for a 700 MNOK school construction project, negotiating with **4 distinct AI agents** (3 suppliers + 1 owner) to complete 3 work packages within challenging budget and time constraints.

### Key Features (POC Scope)

- **4 AI Agent Roles:**
  - 1 Owner (Municipality) - Budget approval, inflexible time constraint
  - 3 Suppliers - Price/quality, time/cost tradeoffs, scope reduction
- **3 Negotiable WBS Packages** (12 pre-contracted)
- **Budget Challenge:** 310 MNOK available vs 345 MNOK baseline
- **Inflexible Deadline:** May 15, 2026 (enforced via Owner AI)
- **Explicit Accept/Reject:** No automatic offer acceptance
- **Norwegian Language:** All interactions in Norwegian

---

---

## New Files Added

<!-- NEW_FILES_START -->
- [AI_AGENT_SYSTEM_PROMPTS.md](docs/AI_AGENT_SYSTEM_PROMPTS.md)
- [API_DATABASE_INTEGRATION_GUIDE.md](docs/API_DATABASE_INTEGRATION_GUIDE.md)
- [BUDGET_MODEL_VERIFICATION.md](docs/BUDGET_MODEL_VERIFICATION.md)
- [CONSISTENCY_AUDIT_REPORT_DEC_12.md](docs/CONSISTENCY_AUDIT_REPORT_DEC_12.md)
- [DATABASE_FIX_SUMMARY.md](docs/DATABASE_FIX_SUMMARY.md)
- [DATABASE_INCONSISTENCY_REPORT.md](docs/DATABASE_INCONSISTENCY_REPORT.md)
- [DOCUMENTATION_UPDATE_SUMMARY_DEC_13.md](docs/DOCUMENTATION_UPDATE_SUMMARY_DEC_13.md)
- [IMPLEMENTATION_PLAN_DEC_9-15.md](docs/IMPLEMENTATION_PLAN_DEC_9-15.md)
- [PRD.md](docs/PRD.md)
- [REPOSITORY_VERIFICATION_COMPLETE.md](docs/REPOSITORY_VERIFICATION_COMPLETE.md)
- [REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md](docs/REVISED_IMPLEMENTATION_PLAN_DEC_12-18.md)
- [Refleksjonsrapport Gruppe 14-D2.pdf](docs/Refleksjonsrapport Gruppe 14-D2.pdf)
- [SCOPE_CHANGE_TASKS.md](docs/SCOPE_CHANGE_TASKS.md)
- [V2_CONSISTENCY_VERIFICATION.md](docs/V2_CONSISTENCY_VERIFICATION.md)
- [VISUALIZATION_FEATURES_CONFIRMATION.md](docs/VISUALIZATION_FEATURES_CONFIRMATION.md)
- [bmm-workflow-status.yaml](docs/bmm-workflow-status.yaml)
- [brainstorming-executive-summary.md](docs/brainstorming-executive-summary.md)
- [brainstorming-session-audience-and-core-value-2025-12-07.md](docs/brainstorming-session-audience-and-core-value-2025-12-07.md)
- [brainstorming-session-core-functionality-and-scope-2025-12-07.md](docs/brainstorming-session-core-functionality-and-scope-2025-12-07.md)
- [brainstorming-session-results-2025-12-02.md](docs/brainstorming-session-results-2025-12-02.md)
- [brainstorming-session-results-risk-and-monitoring-2025-12-02.md](docs/brainstorming-session-results-risk-and-monitoring-2025-12-02.md)
- [brainstorming-session-results-user-interactions-2025-12-02.md](docs/brainstorming-session-results-user-interactions-2025-12-02.md)
- [brainstorming-technical-architecture-report.md](docs/brainstorming-technical-architecture-report.md)
- [consistency-audit-report-2025-12-07.md](docs/consistency-audit-report-2025-12-07.md)
- [data/Bygging.pdf](docs/data/Bygging.pdf)
- [data/concept.pdf](docs/data/concept.pdf)
- [data/krav-spec.pdf](docs/data/krav-spec.pdf)
- [data/project-description.pdf](docs/data/project-description.pdf)
- [data/prop-task.md](docs/data/prop-task.md)
- [data/proposal-checklist.yaml](docs/data/proposal-checklist.yaml)
- [data/proposal-example.md](docs/data/proposal-example.md)
- [data/simulation-description.pdf](docs/data/simulation-description.pdf)
- [data/wbs.pdf](docs/data/wbs.pdf)
- [epics.md](docs/epics.md)
- [images/bmad-workflow.svg](docs/images/bmad-workflow.svg)
- [product-brief.md](docs/product-brief.md)
- [project-plan.md](docs/project-plan.md)
- [proposal.md](docs/proposal.md)
- [research-report-2025-12-07.md](docs/research-report-2025-12-07.md)
- [solutioning-gate-check.md](docs/solutioning-gate-check.md)
- [test-design.md](docs/test-design.md)
- [ux-design-specification.md](docs/ux-design-specification.md)
- [ux/UI_flows/FINAL_FILES_README.md](docs/ux/UI_flows/FINAL_FILES_README.md)
- [ux/UI_flows/FINAL_MOCKUP_INVENTORY.md](docs/ux/UI_flows/FINAL_MOCKUP_INVENTORY.md)
- [ux/UI_flows/FLOW_DIAGRAMS_INDEX.md](docs/ux/UI_flows/FLOW_DIAGRAMS_INDEX.md)
- [ux/UI_flows/QUALITY_CHECK_REPORT.md](docs/ux/UI_flows/QUALITY_CHECK_REPORT.md)
- [ux/UI_flows/V2_MOCKUP_INVENTORY.md](docs/ux/UI_flows/V2_MOCKUP_INVENTORY.md)
- [ux/UI_flows/final-flow-01-complete-user-journey.svg](docs/ux/UI_flows/final-flow-01-complete-user-journey.svg)
- [ux/UI_flows/final-flow-02-authentication-process.svg](docs/ux/UI_flows/final-flow-02-authentication-process.svg)
- [ux/UI_flows/final-flow-03-negotiation-strategies.svg](docs/ux/UI_flows/final-flow-03-negotiation-strategies.svg)
- [ux/UI_flows/final-screen-01-login-page.svg](docs/ux/UI_flows/final-screen-01-login-page.svg)
- [ux/UI_flows/final-screen-02-dashboard-main.svg](docs/ux/UI_flows/final-screen-02-dashboard-main.svg)
- [ux/UI_flows/final-screen-03-chat-interface.svg](docs/ux/UI_flows/final-screen-03-chat-interface.svg)
- [ux/UI_flows/v2-flow-01-complete-journey.svg](docs/ux/UI_flows/v2-flow-01-complete-journey.svg)
- [ux/UI_flows/v2-flow-02-authentication.svg](docs/ux/UI_flows/v2-flow-02-authentication.svg)
- [ux/UI_flows/v2-flow-03-negotiation-strategy.svg](docs/ux/UI_flows/v2-flow-03-negotiation-strategy.svg)
- [ux/functional_flows/FLOW_CREATION_SUMMARY.md](docs/ux/functional_flows/FLOW_CREATION_SUMMARY.md)
- [ux/functional_flows/README.md](docs/ux/functional_flows/README.md)
- [ux/functional_flows/flow-01-validation-rules.svg](docs/ux/functional_flows/flow-01-validation-rules.svg)
- [ux/functional_flows/flow-02-budget-calculation.svg](docs/ux/functional_flows/flow-02-budget-calculation.svg)
- [ux/functional_flows/flow-03-ai-agent-negotiation.svg](docs/ux/functional_flows/flow-03-ai-agent-negotiation.svg)
- [ux/functional_flows/flow-04-commitment-uncommitment.svg](docs/ux/functional_flows/flow-04-commitment-uncommitment.svg)
- [ux/functional_flows/flow-05-state-management.svg](docs/ux/functional_flows/flow-05-state-management.svg)
- [ux/functional_flows/flow-06-error-handling.svg](docs/ux/functional_flows/flow-06-error-handling.svg)
- [ux/functional_flows/flow-07-critical-path-timeline.svg](docs/ux/functional_flows/flow-07-critical-path-timeline.svg)
- [ux/functional_flows/visualization-01-gantt-chart.svg](docs/ux/functional_flows/visualization-01-gantt-chart.svg)
- [ux/functional_flows/visualization-02-precedence-diagram.svg](docs/ux/functional_flows/visualization-02-precedence-diagram.svg)
- [validation-report-PRD-2025-12-07.md](docs/validation-report-PRD-2025-12-07.md)
- [validation-report-UX-Design-2025-12-07.md](docs/validation-report-UX-Design-2025-12-07.md)
<!-- NEW_FILES_END -->

---

## Repository Structure

```
/docs/               # Complete project documentation
  ├── PRD.md                          # Product Requirements Document (v2.0)
  ├── product-brief.md                # Product Brief (v2.0 - POC scope)
  ├── AI_AGENT_SYSTEM_PROMPTS.md      # Complete AI agent system prompts
  ├── ux-design-specification.md      # UX/UI design specification
  ├── epics.md                        # User stories and epics
  ├── SCOPE_CHANGE_TASKS.md           # Scope change implementation guide
  └── research-report-2025-12-07.md   # Market and technical research

/docs/ux/            # SVG mockups and wireframes
/frontend/           # React + TypeScript frontend
/backend/            # FastAPI backend (AI proxy)
```

---

## Quick Start

### Documentation

1. **Start here:** [Product Brief](docs/product-brief.md) - Overview and POC scope
2. **Requirements:** [PRD.md](docs/PRD.md) - Complete functional requirements
3. **AI Agents:** [AI_AGENT_SYSTEM_PROMPTS.md](docs/AI_AGENT_SYSTEM_PROMPTS.md) - System prompts for all 4 agents
4. **Design:** [UX Design Specification](docs/ux-design-specification.md) - UI/UX requirements
5. **Implementation:** [Epics & User Stories](docs/epics.md) - Development backlog

### Key Documents Summary

| Document | Purpose | Status |
|----------|---------|--------|
| PRD.md (v2.0) | Complete requirements for POC | ✅ Updated |
| product-brief.md (v2.0) | Executive summary and scope | ✅ Updated |
| AI_AGENT_SYSTEM_PROMPTS.md | AI agent implementation specs | ✅ Complete |
| SCOPE_CHANGE_TASKS.md | Migration guide from v1.0 to v2.0 | ✅ Complete |
| ux-design-specification.md | UI/UX design requirements | 🔄 In Progress |
| epics.md | User stories and sprint planning | 🔄 In Progress |

---

## POC Scope Highlights (v2.0)

**Changed from v1.0:**
- From 15 → 3 negotiable WBS packages
- From 5 suppliers → 4 AI agents (3 suppliers + 1 owner)
- Added Owner AI role with budget/scope negotiation
- Inflexible time constraint (100% enforcement)
- Explicit accept/reject flow (no automatic acceptance)

**Budget Model:**
- Total: 700 MNOK
- Locked: 650 MNOK (12 pre-contracted suppliers)
- Available: 310 MNOK (for 3 negotiable packages)
- Challenge: Baseline estimates = 345 MNOK (35 MNOK shortfall)

**Rationale:** Focus on AI negotiation quality over quantity; prove concept with manageable scope before expanding to full 15-package simulation.

---

## Tech Stack

- **Frontend:** React 18 + TypeScript + Tailwind CSS + Shadcn UI
- **Backend:** FastAPI (Python 3.11+) + PydanticAI
- **AI:** Google Gemini 2.5 Flash
- **Auth:** Supabase Auth (JWT-based authentication)
- **Database:** Supabase PostgreSQL (game sessions, user data, negotiation history)
- **Hosting:** Vercel (frontend + serverless backend)

---

## Development Timeline

- **Week 1:** Static data, infrastructure, auth ✅
- **Week 2:** Frontend UI, WBS display, chat interface 🔄
- **Week 3:** AI integration, 4 agent prompts, negotiation logic
- **Week 4:** Validation, mockups, testing

**Estimated Completion:** December 15-18, 2025

---

## License

Academic project for IBE160 Programmering med KI course.

---

## Contact

**Course:** IBE160 - Programmering med KI
**Institution:** [University Name]
**Group:** SG-Gruppe-14-d2
