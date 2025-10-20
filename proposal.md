## Case Title
AI-Driven Simulation for Construction Project Management

## Background
Construction projects are complex and exposed to schedule, resource, and risk uncertainty. A simulation-based learning tool can help students understand how AI supports planning and execution decisions in realistic project scenarios.

## Purpose
Build an application that simulates the planning and execution of a construction project and uses AI to support decisions on scheduling, resource utilization, and risk response.

## Target Users
Students and instructors in programming/AI and project management courses; junior project managers who need hands-on decision support and scenario exploration.

## Core Functionality
Simulate a construction project from inputs (scope/WBS, resources, costs/tempo, risks/events, milestones, change requests) to outputs (Gantt schedules, cost forecasts, risk exposure, scenario outcomes, recommended actions).

### Must Have (MVP)
- Feature 1: Define project scope/WBS, resource capacity, and cost/productivity parameters.
- Feature 2: Model risks/events, milestones, and change requests with dependencies.
- Feature 3: Run simulations that generate Gantt schedules, cost forecasts, and risk exposure with AI-recommended actions.

### Nice to Have (Optional Extensions)
- Feature 4: Scenario comparison (what‑if/Monte Carlo), dashboards, and exports (CSV/PDF).
- Feature 5: Version control with audit log and role‑based access. 

## Data Requirements
What information needs to be stored and managed?

- Data entity 1: Projects & WBS – title, description, hierarchy, estimates.
- Data entity 2: Resources – roles, capacity, rates.
- Data entity 3: Parameters – cost/tempo/productivity settings.
- Data entity 4: Risks/Events – likelihood, impact, triggers, responses.
- Data entity 5: Milestones – names, target dates, dependencies.
- Data entity 6: Change Requests – description, status, approvals.
- Data entity 7: Simulation Results – schedules (Gantt), cost forecasts, risk exposure, recommendations.
- Data entity 8: Users & Audit – account data, version history, decision log.

## User Stories (Optional)
Brief scenarios describing how users will interact with the system

1. As a student, I want to enter a WBS and resource capacities so that I can generate a feasible project schedule.
2. As a student, I want to simulate risk events and compare scenarios so that I can choose an effective risk response.
3. As an instructor, I want an audit trail of decisions so that I can review each team’s planning rationale.

## Technical Constraints
Any specific requirements or limitations

- Must support authentication; project data may be confidential.
- Version control and audit logging recommended; no online purchases/sales.
- Should be responsive and persist data reliably; reasonable compute time for simulations.

## Success Criteria
How will you know the application is successful?

- Criterion 1: Users can input scope/resources/parameters and produce valid Gantt schedules.
- Criterion 2: The system generates cost forecasts, risk exposure, and actionable recommendations.
- Criterion 3: Users can run and compare scenarios and record approvals/changes.