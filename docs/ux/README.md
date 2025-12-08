# UX Design Diagrams & Mockups

This folder contains SVG vector diagrams and high-fidelity mockups that visualize the user experience, workflows, and system architecture for the **Nye Hædda Barneskole Project Management Simulation**.

All diagrams are created in **Norwegian** to match the application language and are fully scalable vector graphics (SVG) for use in documentation, presentations, and development reference.

---

## Contents

- **Workflow Diagrams (01-07):** Process flows, decision trees, and system visualizations
- **High-Fidelity Mockups (mockup-01 to mockup-07):** Pixel-perfect UI designs for all pages and modals

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

## High-Fidelity Mockup Index

### Mockup 01. Login Page
**File:** `mockup-01-login-page.svg`

**Description:** Complete login page design with:
- Clean, centered card layout with gradient background
- Email and password input fields with proper styling
- "Remember me" checkbox and "Forgot password" link
- Primary login button and registration link
- Info panel with welcome message
- UiA branding and LOG565 course attribution

**Viewport:** 1440x900px (standard desktop)

**Use Cases:**
- Frontend implementation reference for authentication
- Visual design approval
- Supabase Auth integration guide

---

### Mockup 02. Registration Page
**File:** `mockup-02-registration-page.svg`

**Description:** Registration form with right-side feature panel:
- Full name, email (UiA), password, and confirm password fields
- Real-time password strength indicator (weak/medium/strong)
- Terms and conditions checkbox
- Right-side benefits panel with 4 feature highlights:
  - Save progress
  - Track performance
  - Compete with others (coming soon)
  - 100% private (GDPR-compliant)
- Time estimate badge: 45-60 minutes
- Green color scheme to differentiate from login

**Viewport:** 1440x900px

**Use Cases:**
- Registration flow implementation
- Form validation patterns
- Marketing/feature communication

---

### Mockup 03. Dashboard (Full Detail)
**File:** `mockup-03-dashboard-full.svg`

**Description:** Complete main dashboard with realistic data:
- **Header:** Navigation tabs (Dashboard, Leverandører), help button, user menu
- **Constraints Panel:**
  - Budget progress bar (450/700 MNOK = 64%)
  - Deadline tracker (15. mai 2026)
  - Expected completion (10. april 2026 ✓ with 35-day margin)
- **Quick Stats Bar:** 8/15 WBS completed, 32 negotiations, auto-save status
- **WBS List (left 2/3):**
  - Filter tabs (All/Completed/Remaining)
  - 5 WBS items shown: 2 completed (green), 1 in-progress (yellow), 2 pending (gray)
  - Critical path indicators (red 🔴)
  - Supplier names and cost/duration data
- **Action Panel (right 1/3):**
  - "Send Inn Plan" primary button (disabled until 15/15 complete)
  - Export to JSON button
  - Tips panel
  - Progress statistics mini-chart
  - Reset simulation button (red)

**Viewport:** 1920x1080px (full HD)

**Use Cases:**
- Primary frontend implementation reference
- Component layout and hierarchy
- Real data visualization examples

---

### Mockup 04. Chat Interface (Full Detail)
**File:** `mockup-04-chat-interface-full.svg`

**Description:** Complete chat negotiation interface:
- **Left Sidebar (400px):**
  - Supplier list with 15 items
  - Search functionality
  - Filter tabs (All/Online/Active)
  - Supplier cards showing: avatar, name, status (online/completed), WBS assignment
  - Active chat highlighted with blue border
  - Unread message badges
- **Chat Window (main):**
  - Chat header: Supplier name, status, WBS context, export/close buttons
  - Welcome message with negotiation tips
  - 4 messages shown: User → AI → User → AI (typing)
  - Real negotiation example: Råbygg 200 MNOK → 190 MNOK
  - Message timestamps
  - Input area with text field and two buttons: "Send" and "Aksepter tilbud" (green)
- **Floating Help Tooltip:** Negotiation strategy tips

**Viewport:** 1920x1080px

**Use Cases:**
- Chat UI implementation
- Message layout and styling
- Real-time typing indicators
- Supplier list design

---

### Mockup 05. Success Modal
**File:** `mockup-05-success-modal.svg`

**Description:** Celebration modal shown when plan is approved:
- **Success Icon:** Large green checkmark with confetti decoration
- **Title:** "Gratulerer! 🎉" with subtitle
- **Summary Box (green):**
  - Total cost: 695 MNOK (5 MNOK under budget ✓)
  - End date: 10. april 2026 (35 days before deadline ✓)
  - WBS tasks: 15/15 completed ✓
- **Achievement Badges:**
  - 💰 Budsjettmester (Under budget)
  - ⏱️ Tidsmester (Before deadline)
  - 🤝 Forhandler (32 negotiations)
  - ✨ Førstegangs (First plan)
- **Action Buttons:**
  - Export plan (JSON) - green
  - View detailed report - blue
  - Start new simulation - text link

**Viewport:** 1920x1080px (modal overlay)

**Use Cases:**
- Success feedback design
- Export functionality
- Achievement system (post-MVP)

---

### Mockup 06. Error/Validation Modal
**File:** `mockup-06-error-validation-modal.svg`

**Description:** Error modal shown when plan exceeds constraints:
- **Error Icon:** Large red exclamation mark
- **Error Summary (red):**
  - Budget overage: 715 MNOK / 700 MNOK
  - Required reduction: -15 MNOK (highlighted)
- **Problematic WBS Items (yellow box):**
  - Top 3 most expensive items listed:
    1. Råbygg: 200 MNOK (highest!)
    2. Grunnarbeid: 105 MNOK
    3. Elektrisk: 65 MNOK
- **Recommendations (blue box):**
  - 5 actionable tips for reducing budget
  - "Go back to Råbygg and negotiate from 200 → 185"
  - "Optimize timeline to reduce costs"
  - "Contact project owner for budget increase"
  - etc.
- **Action Buttons:**
  - "Back and negotiate again" (blue)
  - "Reset entire plan" (red, destructive)
  - Help link at bottom

**Viewport:** 1920x1080px (modal overlay)

**Use Cases:**
- Error handling and user guidance
- Validation feedback design
- Helpful error messages (not just "Error!")

---

### Mockup 07. Help/Onboarding Modal
**File:** `mockup-07-help-onboarding-modal.svg`

**Description:** Multi-tab help system with step-by-step guide:
- **Header:** "Velkommen til simulatoren! 👋" with subtitle
- **6 Tabs:** Kom i gang (active), Forhandling, WBS & Budsjett, Tips & Triks, FAQ, Ressurser
- **Step-by-Step Guide (6 steps):**
  1. Review project constraints (blue)
  2. Select WBS task (green)
  3. Negotiate with AI supplier (yellow)
  4. Accept offer when satisfied (purple)
  5. Repeat for all 15 tasks (blue)
  6. Submit plan for validation (green)
- **Info Box:** Estimated time 45-60 minutes, auto-save enabled
- **Bottom Actions:**
  - "Start simulering nå!" (blue, primary)
  - "Les mer dokumentasjon" (gray, secondary)
  - Video tutorial button
- **Progress Dots:** 1/6 pages (for multi-page onboarding)

**Viewport:** 1920x1080px (modal overlay)

**Use Cases:**
- User onboarding flow
- In-app help system
- Tutorial content structure

---

### Mockup 08. Gantt Chart View
**File:** `mockup-08-gantt-chart-view.svg`

**Description:** Interactive Gantt chart showing project timeline:
- **Header Navigation:** Dashboard, Gantt, Precedence tabs + History button (top right)
- **Controls Panel:**
  - View modes: Month/Week/Day (Month active)
  - Zoom slider
  - Filters: Critical path, Dependencies, Milestones (all checked)
  - Export to PNG button
- **Timeline Header:** Jan 2025 → Mar 2026 (15 months) with grid lines
- **Today Line:** Blue dashed vertical line (mid-March 2025)
- **Task Bars:**
  - Green = Completed (1.1, 1.2, 1.3.1, 1.3.2)
  - Yellow = In-progress (1.4.1 Råbygg at 45%)
  - Gray = Planned (1.4.2, 1.5.1, 1.5.2, 1.5.3, 1.8)
  - Red critical path outline on critical tasks
- **Dependencies:** Gray arrows showing task relationships
- **Critical Path:** Red dashed arrows (1.1 → 1.2 → 1.3.1 → 1.3.2 → 1.4.1 → 1.4.2 → 1.8)
- **Milestone:** Diamond shape for 1.8 Inspeksjon
- **Legend:** Color coding explanation, expected completion date

**Viewport:** 1920x1080px

**Use Cases:**
- Visual project timeline tracking
- Critical path analysis
- Dependency visualization
- Progress monitoring over time
- Export for reports/presentations

---

### Mockup 09. Precedence Diagram (AON Network)
**File:** `mockup-09-precedence-diagram.svg`

**Description:** Activity-on-Node (AON) network diagram showing task dependencies:
- **Header Navigation:** Same as Gantt (with History button top right)
- **Controls Panel:**
  - Layout modes: Left→Right (active), Top→Bottom, Hierarchical
  - Filters: Critical path only (checked), Earliest/Latest times, Slack time (checked)
  - Export to PNG button
- **Network Nodes (boxes):**
  - Green boxes = Completed (4 nodes)
  - Yellow box = In-progress (1.4.1 Råbygg 45%)
  - White boxes = Planned (10 nodes)
  - Red thick border = Critical path nodes (8 total)
  - Each node shows: ID, name, duration, cost, status, slack time
- **Arrows:**
  - Gray = Normal dependencies
  - Red thick = Critical path arrows
- **START/END Nodes:** Circular markers
- **Grid Background:** Light dots for visual reference
- **Info Panels (bottom):**
  - Critical Path Summary (red): 8 tasks, 335 days total, ends April 10 2026
  - Parallel Paths (blue): Non-critical tasks with slack times
  - Progress Stats (green): 4/15 completed, 1 in-progress, 10 remaining
  - Network Statistics (yellow): Total nodes, dependencies, criticality percentage

**Viewport:** 1920x1080px

**Use Cases:**
- Critical path method (CPM) analysis
- Identifying bottlenecks
- Understanding task dependencies
- Float/slack time calculations
- Network optimization

---

### Mockup 10. History/Timeline Pane
**File:** `mockup-10-history-timeline-pane.svg`

**Description:** Version control and change tracking system:
- **Left Sidebar (400px):**
  - Timeline list showing all 32 events chronologically
  - Filter buttons: All, Negotiations, Plan changes
  - Each event shows:
    - Version number badge (colored dot)
    - Event title (e.g., "Forhandling med Entreprenør Råbygg AS")
    - Key changes (price, duration)
    - Timestamp
    - Version number
  - Current event highlighted in blue
  - Completed events in white with green checkmarks
  - Vertical timeline line connecting events
- **Right Panel (comparison view):**
  - Split screen: Before (red) vs After (green)
  - Toggle buttons: Gantt view (active), Precedence diagram, Table view
  - Version headers: "Før (Versjon 7)" vs "Etter (Versjon 8)"
  - Summary stats: Total budget and end date comparison
  - **Gantt Comparison:**
    - Timeline showing changed tasks
    - Red bar (removed/old values)
    - Green bar (added/new values)
    - Savings indicator box
    - Collapsed unchanged tasks section
  - **Cascade Effects Panel (blue):**
    - 5 numbered effects of the change:
      1. End date improvement (20 May → 10 April)
      2. Budget improvement (715 → 695 MNOK)
      3. Critical path shortened
      4. Dependent tasks can start earlier
      5. Plan now valid ✓
  - **Change Summary Stats:**
    - Economic impact: -15 MNOK (2.1% savings)
    - Time impact: -5 days (1.5% reduction)
  - **Action Buttons:**
    - Go to Version 7 (blue)
    - Compare other versions (gray)
    - Use Version 8 / current (green)
    - Export history (JSON/PDF)
- **Close History Button:** Top right (red, to return to main view)

**Viewport:** 1920x1080px

**Use Cases:**
- Version control and audit trail
- Understanding decision impact
- Comparing "what-if" scenarios
- Rolling back to previous versions
- Learning from negotiation history
- Demonstrating progress to instructors
- Compliance and documentation

---

## How to Use These Diagrams & Mockups

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

**2025-12-08:** Complete UX design package created
- **7 Workflow Diagrams:**
  - 01: User Journey Flow
  - 02: Dashboard Layout (wireframe)
  - 03: Chat Negotiation Flow
  - 04: Validation Decision Tree
  - 05: WBS Dependency Visualization
  - 06: Mobile Responsive Comparison
  - 07: AI Negotiation Strategy
- **10 High-Fidelity Mockups:**
  - mockup-01: Login Page (1440x900)
  - mockup-02: Registration Page (1440x900)
  - mockup-03: Dashboard Full Detail (1920x1080)
  - mockup-04: Chat Interface Full Detail (1920x1080)
  - mockup-05: Success Modal (overlay)
  - mockup-06: Error/Validation Modal (overlay)
  - mockup-07: Help/Onboarding Modal (overlay)
  - mockup-08: Gantt Chart View (1920x1080) ⭐ NEW
  - mockup-09: Precedence Diagram (1920x1080) ⭐ NEW
  - mockup-10: History/Timeline Pane (1920x1080) ⭐ NEW
- **Total:** 17 SVG files + 1 README
- **Total size:** ~220 KB (highly optimized)

---

**For questions or diagram requests, contact the UX team or create an issue in the repository.**
