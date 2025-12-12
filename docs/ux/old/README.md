# UX Design - Nye Hædda School Simulator

This is the complete UX design package for the Nye Hædda School project simulator. All mockups use a unified design system with Inter font, consistent color palette, and professional styling.

> ⚠️ **Important Update (December 2024)**: All mockups have been redesigned with a new naming convention `nhb-*`. The old files (`01-user-journey-flow.svg`, `mockup-01-login-page.svg`, etc.) are deprecated and should not be used.

---

## 📋 File Naming Convention

All files follow the format: **`nhb-[nr]-[category]-[name].svg`**

- **nhb** = Nye Hædda Barneskole (Norwegian school name)
- **[nr]** = Sequence number (01-20)
- **[category]** = flow | screen | modal | component
- **[name]** = Descriptive name

---

## 📚 Table of Contents

1. [Flowcharts](#-flowcharts-flows) - 3 files
2. [Screen Mockups](#-screen-mockups-screens) - 7 files
3. [Modal Windows](#-modal-windows-modals) - 5 files
4. [Components](#-components) - 2 files
5. [Design System](#-design-system)
6. [User Flow](#-user-flow)
7. [How to Use Files](#-how-to-use-files)

---

## 🗺️ Flowcharts (Flows)

Flowcharts showing user journeys, authentication, and AI logic.

### nhb-01-flow-complete-user-journey.svg
**Description:** Complete user journey from registration to export
- Shows all main steps: Registration → Login → Dashboard → Negotiation → Validation → Success
- Includes decision points and loops
- Error paths and retry logic
- Visualizes the entire game loop

**Dimensions:** 1400x1000px
**Use Cases:** Onboarding, developer reference, project presentations

---

### nhb-02-flow-authentication.svg
**Description:** Supabase authentication flow (registration + login)
- Registration with email verification
- Login flow with error handling
- Session management (JWT tokens)
- Password reset flow
- Includes code snippets for Supabase integration

**Dimensions:** 1400x1000px
**Use Cases:** Backend auth implementation, security testing

---

### nhb-03-flow-negotiation-strategy.svg
**Description:** Gemini AI negotiation logic and strategies
- Shows how AI suppliers make decisions
- Supplier personalities (Bjørn: pragmatic, Emma: impatient)
- Patience mechanics (patience: 1-3)
- Price reduction calculations
- 5 negotiation strategies for users

**Dimensions:** 1600x1000px
**Use Cases:** AI prompt engineering, game balancing, testing

---

## 🖥️ Screen Mockups (Screens)

Full-screen mockups of all main pages in the application.

### nhb-07-screen-login.svg
**Description:** Login page with error handling
- Centered card layout with gradient background
- Email and password fields with validation
- "Remember me" checkbox
- Inline error messages (red border + text)
- Link to registration
- UiA branding

**Dimensions:** 1200x900px
**Use Cases:** Frontend implementation, Supabase Auth

---

### nhb-08-screen-dashboard.svg
**Description:** Main overview with budget tracking and WBS list
- Header with navigation and user menu
- **Constraint Panel:** Budget bar (450/700 MNOK), deadline (May 15, 2026)
- **Quick Stats:** 8/15 completed, 32 negotiations, auto-save
- **WBS List:** 15 tasks with status (pending/negotiating/committed)
- **Action Sidebar:** "Submit Plan", export, tips, reset
- Real-time budget and timeline updates

**Dimensions:** 1400x1000px
**Use Cases:** Main implementation, component hierarchy, data visualization

---

### nhb-09-screen-chat.svg
**Description:** AI chat interface for negotiation
- Chat window with message history (user + AI)
- Supplier info in sidebar (Bjørn Eriksen - Eriksen Bygg AS)
- Typing indicator ("Bjørn is reviewing specifications...")
- "Accept offer" button on AI offers
- Documents panel (WBS, requirements, project description)
- Negotiation status (messages, offers, patience)

**Dimensions:** 1400x1000px
**Use Cases:** Chat UI, Gemini integration, real-time communication

---

### nhb-10-screen-gantt-chart.svg
**Description:** Gantt chart with critical path
- Timeline header (Jan 2025 - May 2026)
- Task bars: Green (completed), Yellow (in progress 45%), Gray (planned)
- Critical path marked with red border
- "Today" marker (blue dashed line)
- Dependency arrows (gray normal, red critical)
- Zoom slider and view options (month/week/day)
- Project status panel at bottom

**Dimensions:** 1600x1000px
**Use Cases:** Timeline visualization, critical path analysis, export to PNG

---

### nhb-11-screen-precedence-diagram.svg
**Description:** AON precedence diagram with dependencies
- Activity-on-Node (AON) network diagram
- Nodes: Green (completed), Yellow (in progress), White (planned), Red border (critical)
- Each node shows: ID, name, duration, cost, slack
- Dependency arrows with direction
- Critical path panel: 15.5 months, 0 days slack
- Selected task details at bottom
- Layout options (hierarchical/horizontal)

**Dimensions:** 1600x1000px
**Use Cases:** CPM analysis, dependency visualization, bottleneck identification

---

### nhb-12-screen-history-timeline.svg
**Description:** History with diff view and rollback
- Chronological timeline (left): All events from session created to plan approved
- Event types: Negotiation, Budget warning, Renegotiation, Validation, Success
- Detail panel (right): Before/After comparison
- Diff view: Red (removed), Green (added)
- Impact analysis: Budget, timeline, critical path
- Negotiation context: Reason, strategy, reaction
- "Restore to this point" button

**Dimensions:** 1400x1000px
**Use Cases:** Version control, audit trail, "what-if" scenarios

---

### nhb-15-screen-registration.svg
**Description:** Registration page with validation
- Fields: Full name, email, password, confirm password
- Real-time password strength indicator (weak/medium/strong)
- Password requirements checklist (8+ chars, number, uppercase)
- Inline error messages (red border + text)
- Terms checkbox (must be accepted)
- Button disabled until all fields are valid
- Link to login

**Dimensions:** 1200x900px
**Use Cases:** Registration, form validation, Supabase auth

---

## 🔲 Modal Windows (Modals)

Modal dialogs for critical decisions and feedback.

### nhb-16-modal-supplier-selection.svg
**Description:** Select supplier before negotiation starts
- Shows WBS task context (1.3.1 - Foundation Work)
- 5 supplier cards with profile info
- Each supplier: Name, company, specialties, personality description
- Recommended matches highlighted (⭐)
- Selected supplier marked with blue border + checkmark
- "Start negotiation with [name]" button

**Dimensions:** 1200x900px (modal overlay)
**Use Cases:** Supplier selection, persona system, chat initiation

---

### nhb-17-modal-commitment-confirm.svg
**Description:** Confirm commitment to offer
- Shows WBS task, supplier, cost, duration
- Calculated start and end dates (based on dependencies)
- Warning: "This will update your project plan"
- "Cancel" and "Confirm" buttons
- Data table layout for overview

**Dimensions:** 1000x700px (modal overlay)
**Use Cases:** Commitment confirmation, plan update

---

### nhb-18-modal-help-onboarding.svg
**Description:** Onboarding and help guidance
- Welcome message with 💡 icon
- 4 step-by-step instructions:
  1. Understand budget and deadline
  2. Select WBS tasks
  3. Negotiate with AI
  4. Submit plan
- Tips box with best practices
- "Skip" and "Start simulator" buttons
- Shown on first login

**Dimensions:** 1000x800px (modal overlay)
**Use Cases:** First-time user experience, in-app help

---

### nhb-19-modal-success.svg
**Description:** Success message after approved plan
- Large green checkmark with 🎉 confetti
- Stats table:
  - Total cost: 698 MNOK (under budget ✓)
  - Completion date: April 10, 2026 (before deadline ✓)
  - Time spent: 47 minutes
  - Negotiations: 32
  - Renegotiations: 3
- "Export session (JSON)" button (primary)
- "Start new game" button (secondary)

**Dimensions:** 1000x800px (modal overlay)
**Use Cases:** Success feedback, export functionality, session completion

---

### nhb-20-modal-error-validation.svg
**Description:** Validation error with solution suggestions
- Large red X with error icon
- Error list (red background):
  - Budget exceeded: 750/700 MNOK (+50 MNOK)
  - Project delayed: May 20, 2026 (5 days over deadline)
- Suggestions section (gray background):
  - Top 3 most expensive tasks to renegotiate
  - Specific cost amounts highlighted
  - Tip: "Focus on the three most expensive first"
- "Back to planning" button

**Dimensions:** 1000x800px (modal overlay)
**Use Cases:** Error handling, user guidance, retry logic

---

## 🧩 Components

Reusable UI components with various states.

### nhb-13-component-wbs-card.svg
**Description:** WBS task card (pending/negotiating/committed)
- **4 states:**
  1. **Pending (gray):** Not started, "Negotiate" button active
  2. **Negotiating (yellow):** Negotiating, shows latest offer and message count
  3. **Committed (green):** Completed, shows supplier, cost, dates
  4. **Hover:** Blue border, highlighted buttons
- Each card shows: WBS ID, name, description, dependencies, requirements
- Actions: "Negotiate", "Continue chat", "Renegotiate", "View details"
- Status indicator: Colored circle (gray/yellow/green)

**Dimensions:** 420x150px per card
**Use Cases:** Dashboard WBS list, component library

---

### nhb-14-component-navigation.svg
**Description:** Top navigation with user menu
- **Logo/Brand:** "NHB" circle icon + "Nye Hædda Barneskole" text
- **Navigation links:** Dashboard (active, blue underline), Gantt Chart, Precedence Diagram
- **Right-side actions:**
  - Help icon (?) → Opens onboarding modal
  - History icon (🕒) → Opens history page
  - User avatar (initials) → Toggle user menu
- **User menu (dropdown):**
  - User info (name + email)
  - Settings
  - Export session
  - Start new game
  - Log out (red)

**Dimensions:** 1300x70px
**Use Cases:** Global navigation, all pages

---

## 🎨 Design System

### Typography
- **Font family**: Inter (sans-serif)
- **Titles**: 24-32px, font-weight: 700
- **Headings**: 16-22px, font-weight: 600
- **Body text**: 13-14px, font-weight: 500
- **Small text**: 10-11px
- **Code**: Courier New, monospace (for code snippets)

### Color Palette

#### Primary Colors
- **Blue (Primary)**: `#3B82F6` - Actions, active state, links
- **Green (Success)**: `#10B981` - Completed, success, positive values
- **Yellow (Warning)**: `#F59E0B` - Warnings, in progress, decisions
- **Red (Error)**: `#EF4444` - Errors, critical path, destructive actions

#### Neutral Colors
- **Text (Dark)**: `#111827` - Main text
- **Text (Medium)**: `#374151` - Labels
- **Text (Light)**: `#6B7280` - Secondary text
- **Background**: `#F9FAFB` - Page background
- **Card**: `#FFFFFF` - Cards, modals
- **Borders**: `#E5E7EB`, `#D1D5DB` - Borders

#### State Colors
- **Not started**: `#9CA3AF` (gray)
- **In progress**: `#F59E0B` (yellow/orange)
- **Completed**: `#10B981` (green)
- **Critical**: `#EF4444` (red)

### Spacing and Layout
- **Border radius**: 6-12px (depending on component size)
- **Card padding**: 20-60px
- **Gap between elements**: 15-30px
- **Shadows**: `drop-shadow(0 4px 12px rgba(0, 0, 0, 0.08))`

### Icons
- **Emojis**: Used sparingly for personality (📊, 📈, 🔀, ✓, 🎉)
- **Unicode symbols**: Arrows (→, ↓), checkmarks (✓), warning (!)

---

## 🔗 User Flow

### Complete flow from start to finish:

1. **`nhb-15-screen-registration.svg`** → Register new user with Supabase
2. **`nhb-07-screen-login.svg`** → Log in (or resume session)
3. **`nhb-18-modal-help-onboarding.svg`** → First-time onboarding (optional, can skip)
4. **`nhb-08-screen-dashboard.svg`** → Main overview
   - View budget (0/700 MNOK) and deadline (May 15, 2026)
   - Select a WBS task to negotiate (e.g., 1.3.1 Foundation Work)
5. **`nhb-16-modal-supplier-selection.svg`** → Select supplier (e.g., Bjørn Eriksen)
6. **`nhb-09-screen-chat.svg`** → Negotiate with AI
   - Receive initial offer (120 MNOK, 3 months)
   - Argue for lower price or shorter time
   - AI provides counter-offer based on strategy and personality
   - Click "Accept offer" when satisfied
7. **`nhb-17-modal-commitment-confirm.svg`** → Confirm commitment
   - View offer summary
   - Click "Confirm" → Plan updates
8. **`nhb-08-screen-dashboard.svg`** → Back to dashboard
   - Budget updated (105 MNOK spent)
   - WBS task 1.3.1 marked as completed (green)
   - Timeline adjusted
9. **Repeat steps 4-8** for all 15 WBS tasks
10. **`nhb-08-screen-dashboard.svg`** → When all 15 tasks completed, click "Submit Plan"
11. **Validation:**
    - **SUCCESS** (budget ≤700 MNOK AND date ≤May 15, 2026):
      → **`nhb-19-modal-success.svg`** → Congratulations! Export session or start new game
    - **ERROR** (budget >700 MNOK OR date >May 15, 2026):
      → **`nhb-20-modal-error-validation.svg`** → View errors and suggestions → Back to step 4 for renegotiation

### Visualizations (available anytime):
- **`nhb-10-screen-gantt-chart.svg`** → Click "📈 Gantt Chart" in navigation
- **`nhb-11-screen-precedence-diagram.svg`** → Click "🔀 Precedence Diagram" in navigation
- **`nhb-12-screen-history-timeline.svg`** → Click "🕒 History" icon

### Help functions:
- **`nhb-18-modal-help-onboarding.svg`** → Click "?" icon in navigation anytime
- **`nhb-14-component-navigation.svg`** → User menu: Export, Settings, Log out

---

## 📖 How to Use Files

### In documentation
Reference mockups in Markdown files:
```markdown
![Dashboard](ux/nhb-08-screen-dashboard.svg)
```

### In presentations
SVG files scale perfectly for slides. Import to PowerPoint, Google Slides, or Figma.

### For development
Use as reference during implementation:
- **Frontend developers:** See `nhb-08` (Dashboard), `nhb-09` (Chat), `nhb-13` (WBS Card)
- **Backend developers:** See `nhb-02` (Auth), `nhb-03` (AI Logic), `nhb-20` (Validation)
- **UX designers:** All files provide visual specifications

### For testing
Create test cases based on flows:
- User journey (`nhb-01`): End-to-end test scenarios
- Validation (`nhb-20`): Edge case testing (over budget, delayed)
- Negotiation (`nhb-03`, `nhb-09`): AI response quality testing

---

## 📐 Dimensions

| Type | Width | Height | Purpose |
|------|--------|-------|--------|
| Flow diagram | 1400-1600px | 1000px | Complex flowcharts |
| Screen mockup | 1400px | 1000px | Full-screen views |
| Modal | 500-1000px | 400-800px | Central dialogs |
| Component | Varies | Varies | Reusable elements |

---

## 🛠️ Technical Implementation

Mockups are created in **SVG format** for:
- ✅ Vector-based (scalable without quality loss)
- ✅ Text-searchable (grep, find)
- ✅ Easy to edit in text editor (XML structure)
- ✅ Small file sizes (~10-30 KB per file)
- ✅ Version control-friendly (diff support in Git)
- ✅ Direct viewing in browsers and Figma

### Editing SVG Files

**Method 1: Text Editor** (recommended for small changes)
1. Open `.svg` file in VS Code or other editor
2. Modify text content, colors (`fill="#..."`), or coordinates
3. Preview in browser (drag-and-drop) or VS Code SVG preview extension
4. Commit changes to Git

**Method 2: Visual Editor** (for major redesigns)
- **Figma** (online, free for individual use)
- **Adobe Illustrator** (paid)
- **Inkscape** (free, open source)
- **SVGator** (online animation)

---

## 🔄 Update Log

### Version 2.0 (December 9, 2024) ⭐ CURRENT
- ✅ **Complete redesign** of all mockups
- ✅ **New unified file naming convention** (`nhb-[nr]-[category]-[name]`)
- ✅ **Inter font** throughout (previously mixed fonts)
- ✅ **Consistent color palette** from UX Design Specification
- ✅ **Detailed annotations** on all files (specs, interactions, technical details)
- ✅ **English language** throughout
- ✅ **17 professional SVG mockups:**
  - 3 Flowcharts
  - 7 Screen mockups
  - 5 Modal windows
  - 2 Components
- ✅ **Total size:** ~300 KB (optimized)

### Version 1.0 (December 8, 2024)
- ⚠️ **DEPRECATED**: Old files are obsolete:
  - `01-user-journey-flow.svg` → Replaced by `nhb-01-flow-complete-user-journey.svg`
  - `02-dashboard-layout.svg` → Replaced by `nhb-08-screen-dashboard.svg`
  - `mockup-01-login-page.svg` → Replaced by `nhb-07-screen-login.svg`
  - `mockup-02-registration-page.svg` → Replaced by `nhb-15-screen-registration.svg`
  - `mockup-03-dashboard-full.svg` → Replaced by `nhb-08-screen-dashboard.svg`
  - `mockup-04-chat-interface-full.svg` → Replaced by `nhb-09-screen-chat.svg`
  - `mockup-05-success-modal.svg` → Replaced by `nhb-19-modal-success.svg`
  - `mockup-06-error-validation-modal.svg` → Replaced by `nhb-20-modal-error-validation.svg`
  - `mockup-07-help-onboarding-modal.svg` → Replaced by `nhb-18-modal-help-onboarding.svg`
  - `mockup-08-gantt-chart-view.svg` → Replaced by `nhb-10-screen-gantt-chart.svg`
  - `mockup-09-precedence-diagram.svg` → Replaced by `nhb-11-screen-precedence-diagram.svg`
  - `mockup-10-history-timeline-pane.svg` → Replaced by `nhb-12-screen-history-timeline.svg`
- ⚠️ **Use only the new `nhb-*` files from version 2.0**

---

## 📖 See Also

- **[UX Design Specification](../ux-design-specification.md)** - Complete design specification
- **[PRD](../PRD.md)** - Product Requirements Document
- **[Epics](../epics.md)** - All user stories and epics
- **[Test Design](../test-design.md)** - Testing strategy
- **[Architecture](../architecture.md)** - Technical stack
- **[Proposal](../proposal.md)** - Project overview

---

## ✉️ Contact

For questions about UX design or mockups, contact the UX team or create an issue in the repository.

---

**Last updated:** December 9, 2024
**Designed by:** Claude Code AI Agent
**Project:** Nye Hædda Barneskole PM Simulator
**Version:** 2.0
