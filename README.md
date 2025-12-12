# Nye Hædda Barneskole - AI Project Management Simulation

**Course:** IBE160 Programmering med KI
**Group:** SG-Gruppe-14-d2
**Project Status:** POC Development Phase
**Last Updated:** 2025-12-11

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
- **Auth:** Supabase (JWT-based)
- **Storage:** localStorage (browser-based, no database)
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
