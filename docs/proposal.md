## Case Title

Project Management Simulation: Nye Hædda Barneskole

## Background

This project is based on the educational case "Nye Hædda Barneskole", a construction project for a new elementary school in Hædda municipality. In the context of the course LOG565 Project Management 2, students are often exposed to theory but lack the opportunity to experience the chaotic and negotiation-heavy "Planning Phase" of a project. Real-world project management involves not just scheduling tasks, but actively eliciting realistic estimates from suppliers and contractors who may have conflicting interests or inflated initial quotes. Existing simulations often provide static data for Gantt charts, missing the crucial soft skill of negotiation and data validation.

## Purpose

The purpose of this application is to provide an interactive, AI-enhanced simulation where players act as the Project Manager for the "Nye Hædda Barneskole" project. The core pedagogical goal is to train players in **gathering and negotiating project data**.

Unlike standard simulations where task duration and costs are given, here the player must:

1. Analyze the provided Work Breakdown Structure (WBS) and Requirements (given in the simulation).
2. Contact specific "Suppliers" (simulated by AI agents) to get estimates.
3. **Negotiate** with these suppliers because their initial quotes will cumulatively exceed the project's strict budget (700 MNOK) and timeline (15 months). Any negotiation can be continued at a later point in order to get a plan within the project scope.
4. An important role is the project owner. The project manager can also ask for change in budget/time constraints as well in order to solve the problem of exceeding limits.
5. Construct a valid Project Plan (Gantt chart data) based on these negotiations, with critical path shown.

The MVP focuses strictly on the **Planning Phase**, specifically the collection and validation of task data.

## Target Users

**Free Registered Users**

- **Who:** Students in project management courses (LOG565) and aspiring project managers.
- **Goal:** To practice the iterative process of creating a realistic project plan under constraints.
- **Access:** Full access to the single-player simulation. No payment walls or subscription tiers.

## Core Functionality

### Must Have (MVP)

**1. Registration & Authentication**

- Email-based registration and login via **Supabase Auth**.
- Persistent user profiles to save simulation progress.

**2. Simulation Context & Dashboard**

- **Project Overview:** Displays the strict constraints:
  - **Budget:** 700 Million NOK.
  - **Deadline:** May 15, 2026 (15 months duration).
  - **Scope:** defined by the WBS and Requirements specifications.
- **Resource Library:** Access to digital versions of the project documents (Project Description, WBS, Requirements Specification).

**3. AI Supplier Interaction System (The "Game Loop")**

- **AI Agents:** Distinct AI personas representing key stakeholders/suppliers defined in the case (e.g., "Totalentreprenør", "Arkitekt", "VVS-ingeniør").
- **Behavior:**
  - Agents hold "hidden" realistic parameters (min cost, min duration) but initially offer "inflated" estimates.
  - Agents react to player arguments based on the Requirements Specification (e.g., "We need to reduce costs because requirement F-002 implies...").
- **Chat Interface:** A dedicated chat window to converse with selected suppliers to request quotes for specific WBS items.

**4. Project Planning Tool**

- **WBS View:** Interactive list of tasks based on the provided `wbs.pdf`.
- **Data Entry:** Players cannot manually "invent" numbers. They must "commit" numbers obtained from the AI negotiations into the plan slots (Duration, Cost, Start Date, Dependencies).
- **Real-time Validation:** The system calculates the current Total Cost and Projected End Date based on entered data.

**5. Win/Loss Condition**

- **Validation:** The simulation ends when the player submits a plan where:
  - All WBS items have assigned data.
  - Total Budget $\le$ 700 MNOK.
  - Finish Date $\le$ May 15, 2026.
  - Quality standards (implied by supplier acceptance) are met.

### Nice to Have (Future Extensions)

- **Visual Gantt Chart:** A graphical representation of the schedule (MVP will use a table view).
- **Risk Events:** Random events during the negotiation phase (e.g., "Steel prices rose 10%").
- **Multiplayer:** Collaborative planning where different players handle different sub-contracts.
- **Instructor Dashboard:** For teachers to view student negotiation logs.

## Data Requirements

**User Data**

- `users`: ID, email, created_at (Managed by Supabase).

**Simulation Data**

- `games`: ID, user_id, status (in_progress, completed), current_budget_used, current_end_date.
- `wbs_items`: Static table containing the definitions from `wbs.pdf` (ID, Name, Description, Parent_ID).
- `suppliers`: Static table defining AI personas (Role, System_Prompt, Negotiation_Stance).

**Game State**

- `plan_entries`: Linked to `games` and `wbs_items`. Stores the player's negotiated values (cost, duration, start_date).
- `chat_logs`: History of conversations between the User and AI Suppliers (for context retention and review).

## User Flows

### Flow 1: The Planning Loop (MVP)

1. **Onboarding:** User logs in and sees the "Nye Hædda Barneskole" dashboard. They see the total budget (0 / 700 MNOK used) and the empty schedule.
2. **Task Analysis:** User selects WBS Item 1.3.1 "Grunnarbeid" (Groundwork).
3. **Supplier Contact:** User opens the "Suppliers" tab and selects the "Entreprenør grunnarbeid" (Groundwork Contractor).
4. **Negotiation:**
   * *User:* "I need a quote for the groundwork. Duration and cost."
   * *AI:* "Based on current rates, we can do it in 3 months for 120 MNOK."
   * *User:* "That's too high. The budget is tight, and we have a WBS estimate of 100 MNOK. Can we optimize?"
   * *AI:* "If we run double shifts, we can do 2.5 months, but cost stays 120 MNOK. Or we reduce scope..."
   * *User negotiates until:* AI agrees to "2 months, 105 MNOK".
5. **Commitment:** User clicks "Accept Quote" in the chat. The values (2 months, 105 MNOK) are auto-filled into the `plan_entries` for Item 1.3.1.
6. **Review:** Dashboard updates. Total Cost: 105/700 MNOK.
7. **Iteration:** User repeats for all critical path items (Råbygg, Tekniske fag, etc.).
8. **Completion:** Once all items are filled, User clicks "Submit Plan".
   * *If Budget > 700M:* System rejects: "Plan over budget. Renegotiate."
   * *If Date > May 15, 2026:* System rejects: "Project delayed. Renegotiate."
   * *Success:* "Plan Approved! You saved the project."

## Technical Specifications

### Frontend

- **Framework:** Next.js  (App Router) for a responsive, server-side rendered React application.
- **Language:** TypeScript.
- **Styling:** Tailwind CSS with **Shadcn UI** for a clean, professional, "enterprise" look suitable for a project management tool.
- **State Management:** Zustand.
- **Localization:** UI text in **Norwegian** (as per instructions), Code/Docs in English.

### Backend

- **Framework:** **FastAPI (Python)**. Python is chosen for its superior ecosystem for AI/LLM integration (PydanticAI, LangChain compatibility).
- **Database:** **Supabase** (PostgreSQL). Used for Auth, Persistence, and Real-time updates (if needed for chat). Only develop remotely. No local database.
- **AI Integration:**
  * **Service:** Gemini 2.5 pro/flash
  * **Logic:** The FastAPI backend will act as the orchestrator using pydantic AI. It will hold the "System Prompts" for each supplier persona (e.g., "You are a stubborn architect who cares about aesthetics over budget...").
  * **Language:** The AI agents will be prompted to communicate in **Norwegian** to align with the application's language requirement.
  * **Prompt Engineering:** Critical component. Prompts must include the specific constraints from `krav-spec.pdf` and `wbs.pdf` so the AI argues consistently.

### Infrastructure

- **Hosting:** Vercel (Frontend & Backend).
- **Auth:** Supabase Auth.

## Timeline and Milestones

**Total Duration:** 5 Weeks

| Phase                          | Week   | Focus                                                                          | Deliverables                                                        |
| ------------------------------ | ------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **1. Analysis & Design** | Week 1 | Study `project-description.pdf`, `wbs.pdf`. Define AI Personas. DB Schema. | Database Schema, System Prompts for 5 key suppliers, UI Wireframes. |
| **2. Setup & Proto**     | Week 2 | Init Next.js + FastAPI. Basic Auth. Chat Interface.                            | Working Chat UI connected to a "Dummy" AI agent.                    |
| **3. Core Logic**        | Week 3 | Implement WBS logic, Plan validation engine, Prompt Engineering.               | Full WBS tree view. AI agents responding with specific case data.   |
| **4. Integration**       | Week 4 | Connect Chat to Plan. "Commit" functionality. State persistence.               | Playable loop: Negotiate -> Save Data -> Validate.                  |
| **5. Polish & Launch**   | Week 5 | UI Polish (Norwegian translations), Testing limits, Bug fixes.                 | Final MVP Release.                                                  |

## Risks and Mitigation

* **Risk:** AI Hallucination (Suppliers agreeing to 0 cost).
  * *Mitigation:* Strong system prompts with "Guardrails" (Minimum values defined in the prompt context that they cannot go below).
* **Risk:** Game too hard/easy.
  * *Mitigation:* Configurable "Difficulty" variable in the AI prompt that adjusts their resistance to negotiation.
* **Risk:** Token Costs.
  * *Mitigation:* Use cheaper models (Gemini Flash/GPT-4o-mini) for general chit-chat, switch to stronger models for final negotiation logic. Cache repetitive queries.

## Success Criteria

1. **Playability:** A user can complete the full "Planning Loop" (negotiate all WBS items) in under 45 minutes.
2. **AI Realism:** The AI suppliers reference actual project documents (e.g., "TEK17 requirements") during the chat.
3. **Constraint Enforcement:** The system correctly flags plans that exceed the 700 MNOK budget or the May 2026 deadline.

---

## Document History

### Version 1.0 (Original)
- Timeline: 5 weeks
- Database: Supabase PostgreSQL
- State Management: Zustand
- AI Model: Gemini 2.5 Pro/Flash

### Version 1.1 (2025-12-07 Update)

**Timeline Optimization:**
- **Timeline updated to 3-4 weeks** (from 5 weeks)
- **Reason:** Simplified architecture decision saves 1-2 weeks development time

**Architecture Changes:**
- **Database:** Changed from Supabase PostgreSQL to **localStorage** for MVP
  - **Rationale:** 45-60 minute single-session use case validated as sufficient for localStorage (5MB browser limit >> 62KB session size)
  - **Validation:** Research Report Section 2 confirms feasibility (localStorage can store 80+ sessions)
  - **Auth preserved:** Supabase Auth still used for JWT-based authentication

- **State Management:** React Context API preferred over Zustand for simplicity
  - Zustand remains optional for future complexity

- **AI Model:** Gemini 2.5 Flash preferred for MVP (cost-effective, 1-3 sec response)
  - Pro available as fallback if quality issues arise

**References:**
- Detailed justification: `brainstorming-session-core-functionality-and-scope-2025-12-07.md`
- Technical validation: `research-report-2025-12-07.md` Section 2
- Final specification: `PRD.md` Sections 7-8
