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
    - *Description: Complete Product Requirements Document with 14 sections, 35+ functional requirements, 30+ user stories, technical specs.*
- [x] **/run-agent-task pm *validate-prd**
    - *File: `validation-report-PRD-2025-12-07.md`*
    - *Description: Comprehensive validation checklist with 111 review items across completeness, clarity, consistency, feasibility, alignment, user-centricity, and actionability. Result: 97% pass rate (34/35 items passed).*
- [x] **/run-agent-task ux-designer *create-ux-design**
    - *File: `ux-design-specification.md`*
    - *Description: Complete UX Design Specification with 9 sections: Design Principles, Visual Design System (colors, typography, spacing), Wireframes (Login, Dashboard, Chat, Modals), User Flows (3 detailed flows), Component Specifications (5 components with TSX code), Interaction Patterns, Responsive Design (desktop + tablet), Accessibility (WCAG 2.1 Level A), Implementation Notes (Tailwind, Shadcn, Norwegian strings).*
- [x] **/run-agent-task ux-designer *validate-ux-design**
    - *File: `validation-report-UX-Design-2025-12-07.md`*
    - *Description: UX Design validation with 90+ review items across Visual Design System, Wireframes, User Flows, Components, Interactions, Responsive Design, Accessibility, Implementation Readiness, PRD Alignment. Result: 96% pass rate (119.5/124 items), APPROVED for implementation.*

---

## Phase 2: Solutioning

- [x] **/run-agent-task architect *create-architecture {prompt / user-input-file}**
    - *File: `architecture.md` (Note: Key decisions captured in `brainstorming-technical-architecture-report.md`)*
- [ ] **/run-agent-task pm *create-epics-and-stories {prompt / user-input-file}**
    - *File: `epics.md`*
- [ ] **/run-agent-task tea *test-design {prompt / user-input-file}**
- [ ] **/run-agent-task architect *solutioning-gate-check {prompt / user-input-file}**

---

## Phase 3: Implementation

- [ ] **/run-agent-task sm *sprint-planning {prompt / user-input-file}**
    - *File: `sprint-artifacts/sprint-status.yaml`*
- ... (Detailed implementation tasks remain unchanged)

---

## BMAD Workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">
