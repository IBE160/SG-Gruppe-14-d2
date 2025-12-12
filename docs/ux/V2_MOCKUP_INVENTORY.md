# v2.0 POC Mockup Inventory
**Date:** 2025-12-12
**Status:** In Progress (6 of 17 complete)
**Scope:** Complete redesign for POC scope (3 negotiable WBS, 4 AI agents, 390/310/700 MNOK budget)

---

## Completion Status

### ✅ COMPLETED (6/17)

#### User Flows (3/3) ✅ COMPLETE
**Purpose:** Flow diagrams show the PROCESS and LOGIC, not visual design. These are for understanding the system architecture, decision points, and user journey.

1. **v2-flow-01-complete-journey.svg** ✅
   - **Type:** Process flow diagram
   - Complete user journey from login to success
   - Shows all 3 negotiable packages
   - Decision points for accept/reject
   - Budget model: 390/310/700 MNOK
   - Norwegian language

2. **v2-flow-02-authentication.svg** ✅
   - **Type:** Process flow diagram
   - Shows authentication LOGIC (login/register branching)
   - Different from v2-screen-01-login.svg which shows visual DESIGN
   - Supabase Auth flow
   - Login vs Register paths
   - Email verification
   - Norwegian language

3. **v2-flow-03-negotiation-strategy.svg** ✅ FIXED
   - **Type:** Strategy comparison diagram
   - 3 main negotiation strategies
   - Strategy 1: Reduced quality (Supplier)
   - Strategy 2: Reduced scope (Owner)
   - Strategy 3: Faster + Cost increase (Supplier → Owner)
   - Shows all 4 AI agents
   - Norwegian language

#### Screen Mockups (3/6) ⚠️ PARTIAL
**Purpose:** Screen mockups show the actual VISUAL DESIGN and UI layout. These are what developers use to build the interface.

4. **v2-screen-01-login.svg** ✅
   - **Type:** Visual screen mockup
   - Shows what login page LOOKS LIKE (different from v2-flow-02 which shows process)
   - Clean login form
   - Email + Password fields
   - "Registrer deg" link
   - Supabase security badge
   - Norwegian language

5. **v2-screen-02-dashboard.svg** ✅
   - **Type:** Visual screen mockup
   - **CRITICAL SCREEN** - Most complex mockup
   - **Scenario:** After 1 negotiation (WBS 1.3.2 completed at 55 MNOK)
   - 3-tier budget display:
     - Tilgjengelig: 55/310 MNOK (18%)
     - Låst: 390 MNOK (12 kontraktfestede leverandører)
     - Totalt: 445/700 MNOK (64%) ✓
   - **Key Challenge:** Shows 35 MNOK deficit from start
     - Baseline estimates: 345 MNOK (105+60+180)
     - Available budget: 310 MNOK
     - Must negotiate down by 35 MNOK minimum
   - WBS list showing:
     - WBS 1.3.1: 105 MNOK baseline (pending, needs negotiation)
     - WBS 1.3.2: 55 MNOK (completed, saved 5 MNOK)
     - WBS 1.4.1: 180 MNOK baseline (pending, needs negotiation)
     - 3 locked examples shown (30, 25, 35 MNOK)
   - Red warning panel explaining budget challenge
   - Solution panel with negotiation strategies
   - 4 AI agents panel (Owner + 3 suppliers)
   - Norwegian language

6. **v2-screen-03-chat.svg** ✅ FIXED
   - **Type:** Visual screen mockup
   - Chat interface with Kari Andersen
   - Message bubbles (user vs AI)
   - **Explicit Accept/Reject buttons** (critical feature)
   - "Forhandler med" toggle (Leverandør/Eier)
   - Document sidebar
   - Negotiation capabilities panel
   - Norwegian language
   - **Fixed:** Invalid SVG attributes removed, proper rendering

---

### ⏳ PENDING (11/17)

#### Screen Mockups (3/6) - Still Needed

7. **v2-screen-04-registration.svg** ⏳
   - Registration form
   - Name, Email, Password fields
   - Email verification message
   - Link to login
   - Norwegian language
   - **Estimated time:** 30 minutes

8. **v2-screen-05-gantt-chart.svg** ⏳
   - Gantt chart visualization
   - Show all 15 WBS items
   - 3 negotiable in blue (interactive)
   - 12 locked in gray (static)
   - Critical path highlighted (5 items, 3 negotiable)
   - Timeline: 15 months, deadline May 15, 2026
   - Norwegian language
   - **Estimated time:** 1 hour

9. **v2-screen-06-precedence-diagram.svg** ⏳
   - Precedence/Network diagram
   - AON (Activity on Node) format
   - Show dependencies
   - Critical path in red
   - 3 negotiable nodes in blue
   - 12 locked nodes in gray
   - Norwegian language
   - **Estimated time:** 1 hour

#### Component Mockups (0/2) - Still Needed

10. **v2-component-01-wbs-card.svg** ⏳
    - Standalone WBS card component
    - Two states:
      - Negotiable (blue border, "Kan forhandles" badge)
      - Locked (gray border, "Kontraktfestet" badge)
    - Show all data fields
    - Button states (Kontakt/Reforhandle)
    - Norwegian language
    - **Estimated time:** 30 minutes

11. **v2-component-02-navigation.svg** ⏳
    - Top navigation bar component
    - Logo/Title
    - User menu dropdown
    - Help button
    - Responsive design notes
    - Norwegian language
    - **Estimated time:** 20 minutes

#### Modal Mockups (0/6) - Still Needed

12. **v2-modal-01-supplier-owner-selection.svg** ⏳
    - Modal for selecting negotiation partner
    - Two options:
      - Leverandør (3 choices: Bjørn/Kari/Per)
      - Eier (Anne-Lise Berg)
    - Show capabilities for each
    - Radio selection
    - Norwegian language
    - **Estimated time:** 40 minutes

13. **v2-modal-02-commitment-confirm.svg** ⏳
    - Confirmation modal before committing to plan
    - Show offer details (cost + duration)
    - Budget impact preview
    - Timeline impact preview
    - **Explicit Yes/No buttons**
    - Warning if over budget
    - Norwegian language
    - **Estimated time:** 30 minutes

14. **v2-modal-03-success.svg** ⏳
    - Success modal after plan submission
    - Summary of final plan:
      - Total cost vs budget
      - Completion date vs deadline
      - Number of negotiations
    - "Eksporter økt" button
    - "Se statistikk" button
    - Norwegian language
    - **Estimated time:** 30 minutes

15. **v2-modal-04-error-validation.svg** ⏳
    - Error modal for failed validation
    - List of errors:
      - Over budget (show by how much)
      - Past deadline (show new date)
      - Missing WBS items
    - "Reforhandle" button
    - Norwegian language
    - **Estimated time:** 30 minutes

16. **v2-modal-05-help-onboarding.svg** ⏳
    - Help/onboarding modal
    - Quick start guide:
      - 1. Review budget (310 MNOK available)
      - 2. Select WBS package
      - 3. Choose partner (Supplier/Owner)
      - 4. Negotiate
      - 5. Accept/Reject offer
      - 6. Complete all 3
      - 7. Submit plan
    - Close button
    - Norwegian language
    - **Estimated time:** 40 minutes

17. **v2-modal-06-owner-negotiation.svg** ⏳
    - Special modal for Owner (Anne-Lise Berg) chat
    - Highlight inflexible time constraint
    - Budget increase request form
    - Scope reduction approval flow
    - "Eier kan ALDRI forlenge tid" warning
    - Norwegian language
    - **Estimated time:** 40 minutes

---

## Design Specifications (Applied to All Mockups)

### Color Palette
- **Primary Blue:** #3B82F6 (negotiable items, CTAs)
- **Primary Dark:** #2563EB (hover states)
- **Success Green:** #10B981 (completed, success)
- **Warning Yellow:** #F59E0B (warnings, owner agent)
- **Error Red:** #EF4444 (errors, over budget)
- **Gray 900:** #111827 (primary text)
- **Gray 700:** #374151 (secondary text)
- **Gray 500:** #6B7280 (placeholders)
- **Gray 300:** #D1D5DB (borders)
- **Gray 100:** #F3F4F6 (backgrounds)
- **Gray 50:** #F9FAFB (page background)
- **White:** #FFFFFF (cards, modals)

### Typography
- **Font Family:** 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
- **Title:** 20-28px, font-weight: 700
- **Heading:** 16-18px, font-weight: 600-700
- **Body:** 13-14px, font-weight: 400-500
- **Small:** 11-12px, font-weight: 400
- **Button:** 12-15px, font-weight: 600

### Key UI Patterns
- **Cards:** White bg, 1px gray border, 8px border-radius, drop-shadow
- **Buttons Primary:** Blue bg, white text, 6px border-radius
- **Buttons Secondary:** White bg, gray border, gray text
- **Inputs:** White bg, gray border, 6px border-radius, 42px height
- **Modals:** White bg, 12px border-radius, centered, drop-shadow
- **Badges:** Colored bg, rounded-full, small text

### Budget Display (3-Tier)
**CRITICAL FEATURE - Must be consistent across all mockups:**

**Budget Model Logic:**
- Total budget: 700 MNOK
- Locked (12 contracted packages): 390 MNOK
- Available (for 3 negotiable): 310 MNOK
- Baseline estimates (3 packages): 345 MNOK
- **Deficit from start: 35 MNOK** (User must negotiate down)

**Display Format:**
```
Tier 1: Tilgjengelig (Available for 3 negotiable)
- Progress bar: X/310 MNOK (percentage)
- Color: Green if <280, yellow if 280-310, red if >310

Tier 2: Låst (Locked for 12 contracted)
- Text display only: "390 MNOK (12 kontraktfestede leverandører)"
- Color: Gray
- NOT editable, NOT negotiable

Tier 3: Totalt (Total validation)
- Text display: "X/700 MNOK (percentage) ✓/❌"
- Color: Green if ≤700, yellow if 680-700, red if >700
- Icon: ✓ if within budget, ❌ if over

Warning Banner (when needed):
- Show remaining baseline vs remaining budget
- Alert if deficit exists: "Underskudd: X MNOK"
```

### WBS Item States
1. **Negotiable (3 items):**
   - Blue left border (4px, #3B82F6)
   - Blue indicator dot
   - Badge: "💬 Kan forhandles" (blue bg)
   - Button: "Kontakt leverandør/eier" (blue, active)
   - Status: ⚪ pending or 🟢 completed

2. **Locked (12 items):**
   - Gray left border (2px, #D1D5DB)
   - 🔒 lock icon
   - Badge: "Kontraktfestet" (gray bg)
   - No buttons
   - Opacity: 0.7
   - Non-interactive

### AI Agents (4 Total)
**CRITICAL - Must show all 4 in relevant mockups:**

1. **Anne-Lise Berg** (Owner/Eier - Kommune)
   - Color: Yellow/Orange (#F59E0B)
   - Powers: Budget ↑, Scope ↓, **Time ✗**
   - Critical rule: "Tiden kan IKKE forlenges"

2. **Bjørn Eriksen** (Supplier 1 - Grunnarbeid)
   - Color: Blue (#3B82F6)
   - Powers: Price/quality negotiation

3. **Kari Andersen** (Supplier 2 - Fundamentering)
   - Color: Blue (#3B82F6)
   - Powers: Time/cost trade-offs

4. **Per Johansen** (Supplier 3 - Råbygg)
   - Color: Blue (#3B82F6)
   - Powers: Scope reduction

---

## Quality Checklist for Each Mockup

Before marking a mockup as complete, verify:

- [ ] All text is in **Norwegian (Bokmål)**
- [ ] All text is **within SVG bounds** (no overflow)
- [ ] All text is **within buttons/containers** (no orphaned text)
- [ ] Font family is **'Inter' or system fallback**
- [ ] Colors match the **specified palette**
- [ ] Budget model is **390/310/700 MNOK** (not 650/310)
- [ ] Shows **3 negotiable + 12 locked** WBS items
- [ ] Shows **4 AI agents** (Owner + 3 suppliers)
- [ ] Includes **explicit accept/reject** flow where applicable
- [ ] Owner agent shows **time_extension_allowed: false**
- [ ] High resolution and professional quality
- [ ] SVG viewBox is properly sized
- [ ] Accessible (sufficient color contrast)

---

## Mockup Implementation Priority

### Priority 1: CRITICAL (Already Complete) ✅
- Dashboard (v2-screen-02) - Central UI, budget display
- Chat (v2-screen-03) - Core negotiation feature
- Complete Journey Flow (v2-flow-01) - User understanding

### Priority 2: HIGH (Complete Next)
1. Supplier/Owner Selection Modal (v2-modal-01) - Core interaction
2. Commitment Confirm Modal (v2-modal-02) - Explicit accept/reject
3. Success Modal (v2-modal-03) - Completion feedback
4. Error Modal (v2-modal-04) - Validation feedback

### Priority 3: MEDIUM
1. Registration Screen (v2-screen-04) - Auth flow
2. Help Modal (v2-modal-05) - User guidance
3. WBS Card Component (v2-component-01) - Reusable UI

### Priority 4: LOW (Nice to Have)
1. Gantt Chart (v2-screen-05) - Visualization
2. Precedence Diagram (v2-screen-06) - Visualization
3. Navigation Component (v2-component-02) - Standard UI
4. Owner Negotiation Modal (v2-modal-06) - Special case

---

## Next Steps

To complete the remaining 11 mockups:

1. **Immediate:** Create the 4 high-priority modals (v2-modal-01 through v2-modal-04)
   - These are essential for core user flow
   - Estimated time: 2 hours

2. **Short-term:** Create registration and help screens
   - Complete the authentication flow
   - Estimated time: 1 hour

3. **Medium-term:** Create visualization screens (Gantt, Precedence)
   - These are supplementary but valuable
   - Estimated time: 2 hours

4. **Final polish:** Create remaining components
   - Ensure consistency across all mockups
   - Estimated time: 1 hour

**Total estimated time to complete:** 6 hours

---

## File Naming Convention

All mockups follow this pattern:
```
v2-{type}-{number}-{name}.svg
```

Where:
- `type` = flow | screen | component | modal
- `number` = sequential (01, 02, 03...)
- `name` = descriptive kebab-case name

Examples:
- `v2-flow-01-complete-journey.svg`
- `v2-screen-02-dashboard.svg`
- `v2-modal-03-success.svg`

---

## Version History

- **v2.0 (2025-12-12):** Initial creation, 6 of 17 mockups complete
  - All mockups reflect POC scope changes
  - Budget model: 390/310/700 MNOK
  - 4 AI agents (Owner + 3 suppliers)
  - Explicit accept/reject flow
  - Norwegian language throughout
