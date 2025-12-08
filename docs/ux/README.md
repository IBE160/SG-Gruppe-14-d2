# UX Design Diagrams

This folder contains SVG vector diagrams that visualize the user experience, workflows, and system architecture for the **Nye Hædda Barneskole Project Management Simulation**.

All diagrams are created in **Norwegian** to match the application language and are fully scalable vector graphics (SVG) for use in documentation, presentations, and development reference.

---

## Diagram Index

### 01. User Journey Flow
**File:** `01-user-journey-flow.svg`

**Description:** Complete user journey from login to successful plan submission, showing all major steps:
- Login authentication
- Dashboard overview
- WBS task selection
- Supplier selection
- AI negotiation loop
- Plan validation (success/failure paths)

**Use Cases:**
- Onboarding documentation for new users
- Developer reference for implementing the core game loop
- Stakeholder presentations

---

### 02. Dashboard Layout
**File:** `02-dashboard-layout.svg`

**Description:** Detailed wireframe of the main dashboard view (desktop 1024px+):
- Header with user menu and help button
- Project constraints panel (budget progress bar, deadline status)
- Quick stats (WBS completion, negotiation count)
- Two-column layout: WBS list (left, 2/3 width) + Action buttons (right, 1/3 width)
- Individual WBS item cards showing status (completed/pending)

**Use Cases:**
- Frontend implementation reference
- UI/UX testing baseline
- Responsive design starting point

---

### 03. Chat Negotiation Flow
**File:** `03-chat-negotiation-flow.svg`

**Description:** Example of a complete negotiation session with an AI supplier:
- Initial high-price quote from AI (120 MNOK, 90 days)
- User arguments based on budget constraints
- AI counter-offers with justification (110 MNOK)
- Final user push (105 MNOK)
- AI acceptance and data commit

Shows realistic Norwegian dialogue and negotiation dynamics.

**Use Cases:**
- AI prompt engineering reference
- User training materials
- Chat UI implementation guide

---

### 04. Validation Decision Tree
**File:** `04-validation-decision-tree.svg`

**Description:** Decision tree showing the plan validation logic:
1. Check: All WBS items have data?
2. Check: Total cost ≤ 700 MNOK?
3. Check: Projected end date ≤ 15. mai 2026?
4. Success: Show completion modal
5. Failure: Show specific error modal with recommendations

Includes error handling paths and retry loops.

**Use Cases:**
- Backend validation logic implementation
- Testing edge cases (over budget, delayed project)
- Error modal design reference

---

### 05. WBS Dependency Visualization
**File:** `05-wbs-dependency-visualization.svg`

**Description:** Complete WBS structure showing all 15 tasks organized by phase:
- 1.1-1.2: Prosjektering (Architect, RIB)
- 1.3: Grunnarbeider (Groundwork, Foundation)
- 1.4: Råbygg (Shell, Roof/Walls)
- 1.5: Tekniske fag (Electrical, HVAC, Ventilation)
- 1.6: Innvendig (Interior walls, Flooring)
- 1.7-1.8: Ferdigstillelse (Painting, Inspection)

**Critical path highlighted in red** (longest dependency chain affecting deadline).

**Use Cases:**
- Understanding project structure
- Critical path algorithm implementation
- Dependency validation logic
- Gantt chart feature (post-MVP)

---

### 06. Mobile Responsive Comparison
**File:** `06-mobile-responsive-comparison.svg`

**Description:** Side-by-side comparison of layouts across breakpoints:
- **Desktop (1024px+):** 2-column layout, full features
- **Tablet Landscape (768px):** 1-column with sticky actions
- **Tablet Portrait (640px):** Compact vertical layout
- **Mobile (<640px):** Not supported in MVP (marked with warnings)

Includes a feature comparison table showing what works on each device.

**Use Cases:**
- Responsive design implementation
- Device testing checklist
- Stakeholder explanation of mobile strategy

---

### 07. AI Negotiation Strategy
**File:** `07-ai-negotiation-strategy.svg`

**Description:** Technical deep-dive into how AI suppliers negotiate:
- **System Prompt:** Persona definition (professional Norwegian contractor)
- **Context:** Project constraints and requirements
- **Guardrails:** Hardcoded min/max cost/duration limits (prevents AI hallucination)
- **5-step negotiation flow:** Initial offer → User argues → Counteroffer → User pushes → Final acceptance
- **Difficulty levels:** Easy (0.3 resistance), Medium (0.6 resistance), Hard (0.9 resistance)

**Use Cases:**
- Backend AI integration (PydanticAI + Gemini 2.5 Flash)
- Prompt engineering
- Balancing game difficulty
- Testing AI agent behavior

---

## How to Use These Diagrams

### In Documentation
Reference diagrams in Markdown files:
```markdown
![User Journey Flow](ux/01-user-journey-flow.svg)
```

### In Presentations
SVG files scale perfectly for slides. Import into PowerPoint, Google Slides, or Figma.

### For Development
Use as reference during implementation:
- **Frontend devs:** Refer to 02 (Dashboard), 03 (Chat), 06 (Responsive)
- **Backend devs:** Refer to 04 (Validation), 05 (Dependencies), 07 (AI Logic)
- **UX designers:** All diagrams provide visual specifications

### For Testing
Create test cases based on flows:
- User journey (01): End-to-end test scenarios
- Validation tree (04): Edge case testing (over budget, delayed)
- Negotiation (03, 07): AI response quality testing

---

## Design Notes

### Visual Style
- **Color Palette:** Matches UX Design Specification
  - Blue (#2563EB): Primary actions, headers
  - Green (#16A34A): Success states, completed items
  - Yellow (#F59E0B): Warnings, decisions, in-progress
  - Red (#DC2626): Errors, critical path, not supported
  - Gray (#F3F4F6): Neutral panels, pending items

### Typography
- **Sans-serif fonts** for readability
- **Monospace** for code snippets (in diagram 07)
- **Norwegian language** throughout (except technical code)

### Accessibility
- High contrast text/background combinations
- Color is supplemented with icons (✅, ⭕, ❌) for colorblind users
- Clear labels and legends on all diagrams

---

## Updating Diagrams

All diagrams are **pure SVG** (no external dependencies). To edit:

1. Open `.svg` file in any text editor
2. Modify text content, colors, or layout
3. Preview in browser or VS Code SVG preview extension
4. Commit changes to repository

**Recommended tools:**
- **Text editor:** VS Code with SVG preview extension
- **Visual editor:** Figma, Adobe Illustrator, Inkscape (free)
- **Online editor:** SVGator, Method Draw

---

## Related Documentation

- **UX Design Specification:** `../ux-design-specification.md` (full component details)
- **PRD:** `../PRD.md` (functional requirements)
- **Epics:** `../epics.md` (user stories and implementation plan)
- **Architecture:** `../architecture.md` (technical stack)
- **Proposal:** `../proposal.md` (project overview and context)

---

## Changelog

**2025-12-08:** Initial creation of 7 UX diagrams
- 01: User Journey Flow
- 02: Dashboard Layout
- 03: Chat Negotiation Flow
- 04: Validation Decision Tree
- 05: WBS Dependency Visualization
- 06: Mobile Responsive Comparison
- 07: AI Negotiation Strategy

---

**For questions or diagram requests, contact the UX team or create an issue in the repository.**
