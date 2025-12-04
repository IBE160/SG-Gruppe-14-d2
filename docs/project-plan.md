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

- **Brainstorming (Next Steps)**
    - [ ] **/run-agent-task analyst *brainstorm "Audience and Core Value"**
        - *Goal: Define User Personas, Value Proposition, and Success Metrics.*
    - [ ] **/run-agent-task analyst *brainstorm "Core Functionality and Scope"**
        - *Goal: Define MVP features, Data Flow, and Visualization needs.*

- [ ] **Research**
    - [ ] /run-agent-task analyst *research "..."*
        - *File: `research-technical-date.md`*

- [ ] **Product Brief**
    - [ ] /run-agent-task analyst *product-brief "Read the brainstorming sessions, research, and @proposal.md to create a product brief."*
        - *File: `product-brief.md`*

---

## Phase 1: Planning

- [ ] **/run-agent-task pm *prd**
    - *File: `PRD.md`*
- [ ] **/run-agent-task pm *validate-prd**
    - *File: `validation-report-date.md`*
- [ ] **/run-agent-task ux-designer *create-ux-design {prompt / user-input-file}**
    - *File: `ux-design-specification.md`*
- [ ] **/run-agent-task ux-designer *validate-ux-design {prompt / user-input-file}**

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
