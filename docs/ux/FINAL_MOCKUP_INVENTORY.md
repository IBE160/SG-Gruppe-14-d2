# FINAL Mockup Inventory - Nye Hædda Barneskole POC

**Date:** 2025-12-12
**Version:** FINAL - Corrected Budget Model
**Status:** Complete (6 of 6 core mockups)
**File Prefix:** `final-*` (all files from this session)
**Budget Model:** 390 MNOK locked + 310 MNOK available = 700 MNOK total
**Challenge:** 35 MNOK deficit from start (345 MNOK baseline - 310 MNOK available)

---

## 🎯 IMPORTANT: File Naming

**All corrected mockups from this session use the prefix `final-`:**

- `final-flow-##-*.svg` - Flow diagrams
- `final-screen-##-*.svg` - Screen mockups

**These are the ONLY files with the correct budget model (390/310/700 MNOK).**

---

## ✅ COMPLETED MOCKUPS (6/6)

### Flow Diagrams (3/3) ✅

#### 1. final-flow-01-complete-user-journey.svg ✅
**Type:** Process flow diagram
**Purpose:** Shows complete user journey from login to success

**Key Features:**
- All decision points with explicit yes/no paths
- 3 negotiable WBS packages
- 12 locked packages (390 MNOK)
- Budget display: 390 MNOK låst + 310 MNOK tilgjengelig
- 35 MNOK deficit highlighted
- 4 AI agents (Owner + 3 suppliers)
- Validation checkpoints (≤700 MNOK, ≤15 May 2026)
- Norwegian language throughout

**Budget Model Shown:**
- Locked: 390 MNOK (12 packages)
- Available: 310 MNOK (3 negotiable)
- Total: 700 MNOK
- Deficit: 35 MNOK (345 baseline - 310 available)

---

#### 2. final-flow-02-authentication-process.svg ✅
**Type:** Process flow diagram
**Purpose:** Shows authentication logic and user flow

**Key Features:**
- Login vs Register branching
- Email verification flow
- Supabase Auth integration
- Session creation
- Error handling
- Dashboard redirect with budget context
- Norwegian language

**Budget Context:**
- Dashboard shows: "390 MNOK låst, 310 MNOK tilgjengelig"

---

#### 3. final-flow-03-negotiation-strategies.svg ✅
**Type:** Strategy comparison diagram
**Purpose:** Shows 3 main negotiation approaches

**Key Features:**
- **Challenge Box:**
  - Total: 700 MNOK
  - Locked: 390 MNOK (12 packages)
  - Available: 310 MNOK
  - Baseline: 345 MNOK (105+60+180)
  - **UNDERSKUDD: 35 MNOK**

- **Strategy 1: Reduced Quality (Supplier)**
  - Partner: Bjørn Eriksen
  - Save 10-16 MNOK
  - Trade-off: Quality reduction

- **Strategy 2: Reduced Scope (Owner)**
  - Partner: Anne-Lise Berg
  - Save 15-25 MNOK
  - Trade-off: Functionality reduction
  - **Best for 35 MNOK deficit**

- **Strategy 3: Faster + Budget Increase**
  - Partners: Kari Andersen → Anne-Lise Berg
  - Requires +20-30 MNOK extra
  - Trade-off: Total budget increases

- **Critical Rule:** Owner can NEVER extend time (15 May 2026)
- Norwegian language

---

### Screen Mockups (3/3) ✅

#### 4. final-screen-01-login-page.svg ✅
**Type:** Visual screen mockup
**Purpose:** Shows login page UI design

**Key Features:**
- Clean, professional design
- Email + Password fields
- "Logg inn" button
- "Registrer deg her" link
- Supabase security badge
- Budget context in footer: "390 MNOK låst + 310 MNOK tilgjengelig"
- Norwegian language
- Proper Inter font styling

---

#### 5. final-screen-02-dashboard-main.svg ✅
**Type:** Visual screen mockup
**Purpose:** **CRITICAL SCREEN** - Main dashboard with complete budget model

**Scenario:** Initial state (0 MNOK spent, all 3 negotiable packages pending)

**Key Features:**

**3-Tier Budget Display:**
1. **Tilgjengelig (Available):**
   - 0 / 310 MNOK (0%)
   - Progress bar: empty (green)
   - For 3 negotiable packages

2. **Låst (Locked):**
   - 390 MNOK (12 kontraktfestede pakker)
   - Gray background
   - Not editable

3. **Totalt (Total):**
   - 390 / 700 MNOK (56%)
   - 310 MNOK gjenstår ✓

**Warning Banner:**
- **Budget Challenge Alert**
- 3 packages estimated at 345 MNOK
- Available: 310 MNOK
- **Deficit: 35 MNOK** ⚠

**WBS List:**
- **WBS 1.3.1 Grunnarbeid** (Negotiable)
  - Baseline: 105 MNOK
  - Status: ⚪ Venter
  - Leverandør: Bjørn Eriksen
  - "Kontakt" button

- **WBS 1.3.2 Fundamentering** (Negotiable)
  - Baseline: 60 MNOK
  - Status: ⚪ Venter
  - Leverandør: Kari Andersen
  - "Kontakt" button

- **WBS 1.4.1 Råbygg** (Negotiable)
  - Baseline: 180 MNOK
  - Status: ⚪ Venter
  - Leverandør: Per Johansen
  - "Kontakt" button

- **12 Locked Packages Preview**
  - Examples: Prosjektering (30 MNOK), RIB (25 MNOK), Elektrisk (35 MNOK)
  - Total: 390 MNOK across all 12
  - Grayed out, non-interactive

**Right Sidebar:**
- **Budget Challenge Panel (Red)**
  - Shows complete breakdown
  - Highlights 35 MNOK deficit

- **Solution Panel (Green)**
  - Two approaches:
    1. Negotiate with suppliers
    2. Negotiate with owner
  - Note: Time CANNOT be extended

- **AI Agents Panel**
  - Anne-Lise Berg (Owner) - Yellow
    - Budsjett ↑ | Scope ↓ | Tid ✗
  - Bjørn Eriksen (Supplier 1) - Blue
    - Pris/kvalitet-forhandling
  - Kari Andersen (Supplier 2) - Blue
    - Tid/kost-avveining
  - Per Johansen (Supplier 3) - Blue
    - Scope-reduksjon

**Budget Model Consistency:**
- Total: 700 MNOK ✓
- Locked: 390 MNOK ✓
- Available: 310 MNOK ✓
- Baseline: 345 MNOK ✓
- Deficit: 35 MNOK ✓

---

#### 6. final-screen-03-chat-interface.svg ✅
**Type:** Visual screen mockup
**Purpose:** Chat interface with AI agent and explicit accept/reject flow

**Scenario:** Negotiation with Kari Andersen (Supplier 2) for WBS 1.3.2

**Key Features:**

**Chat Header:**
- Agent: Kari Andersen (Fundamentering)
- Toggle: "Forhandler med: Leverandør / Eier"
- Back to Dashboard button

**Conversation:**
1. User asks for better price (baseline 60 MNOK)
2. AI offers 3 alternatives:
   - Standard: 55 MNOK, 2.5 mnd
   - Budget: 48 MNOK, 2.5 mnd (lower quality)
   - Express: 72 MNOK, 1.8 mnd (overtime)
3. User selects alternative 1
4. AI presents final offer

**Final Offer Display (Green Box):**
- Package: WBS 1.3.2 Fundamentering
- Cost: 55 MNOK (saved 5 MNOK)
- Duration: 2.5 months
- Quality: Standard

**EXPLICIT ACCEPT/REJECT BUTTONS:**
- ✓ Godta tilbud: 55 MNOK, 2.5 mnd (Green, large)
- ✗ Avslå og reforhandle (Gray, secondary)
- Note: Budget updates automatically upon acceptance

**Right Sidebar:**

**Current WBS Info:**
- Baseline: 60 MNOK | 2.5 mnd
- Status: Under forhandling
- Critical path: Yes ⚠

**Budget Impact Preview (Yellow):**
- If accepted (55 MNOK):
  - Tilgjengelig: 55/310 MNOK (18%)
  - Låst: 390 MNOK
  - Totalt: 445/700 MNOK (64%)
  - Remaining: 255 MNOK for 2 packages

**Negotiation Capabilities:**
- Kari CAN: Reduce price, change duration, adjust materials
- Kari CANNOT: Extend deadline, change scope, increase total budget

**Documents:**
- WBS Specification PDF
- Cost Estimate
- Project Timeline

**Budget Model Shown:**
- After acceptance: 55/310 available, 390 locked, 445/700 total
- Remaining challenge: 255 MNOK for 2 packages (baseline 285 MNOK)

---

## Design Specifications

### Color Palette
- **Primary Blue:** #3B82F6 (negotiable items, CTAs)
- **Success Green:** #10B981 (completed, success states)
- **Warning Yellow:** #F59E0B (warnings, owner agent)
- **Error Red:** #EF4444 (errors, over budget, deficit)
- **Gray 900:** #111827 (primary text)
- **Gray 700:** #374151 (secondary text)
- **Gray 500:** #6B7280 (placeholders)
- **Gray 300:** #D1D5DB (borders)
- **Gray 100:** #F3F4F6 (backgrounds)
- **White:** #FFFFFF (cards, modals)

### Typography
- **Font Family:** 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
- **Title:** 20-28px, font-weight: 700
- **Heading:** 16-18px, font-weight: 600-700
- **Body:** 13-14px, font-weight: 400-500
- **Small:** 11-12px, font-weight: 400
- **Button:** 13-15px, font-weight: 600

### Key UI Patterns
- **Cards:** White bg, 1px gray border, 8px border-radius, drop-shadow
- **Buttons Primary:** Blue bg (#3B82F6), white text, 6px border-radius
- **Buttons Success:** Green bg (#10B981), white text, 6px border-radius
- **Buttons Secondary:** White bg, gray border, gray text
- **Warning Panels:** Yellow bg (#FEF3C7), orange border (#F59E0B)
- **Error Panels:** Red bg (#FEE2E2), red border (#EF4444)
- **Success Panels:** Green bg (#F0FDF4), green border (#10B981)

---

## Budget Model - CRITICAL REFERENCE

**This is the ONLY correct budget model for all mockups:**

```
Total Budget: 700 MNOK
├─ Locked (12 packages): 390 MNOK ← ALREADY COMMITTED
└─ Available (3 negotiable): 310 MNOK ← FOR NEGOTIATION

Baseline Estimates (3 negotiable):
├─ WBS 1.3.1 Grunnarbeid: 105 MNOK
├─ WBS 1.3.2 Fundamentering: 60 MNOK
└─ WBS 1.4.1 Råbygg: 180 MNOK
   TOTAL: 345 MNOK

CHALLENGE: 345 MNOK - 310 MNOK = 35 MNOK DEFICIT ⚠
```

**User must negotiate down by minimum 35 MNOK to stay within budget.**

---

## File Naming Convention

All mockups follow this pattern:
```
{type}-{number}-{name}.svg
```

Where:
- `type` = flow | screen
- `number` = 01, 02, 03...
- `name` = descriptive-kebab-case-name

Examples:
- `flow-01-complete-user-journey.svg`
- `screen-02-dashboard-main.svg`

---

## Quality Checklist

Before marking a mockup as complete, verify:

- [x] All text is in **Norwegian (Bokmål)**
- [x] Budget model is **390/310/700 MNOK** (NOT 650/310)
- [x] Shows **35 MNOK deficit** from start
- [x] Shows **3 negotiable + 12 locked** WBS items
- [x] Shows **4 AI agents** (Owner + 3 suppliers)
- [x] Includes **explicit accept/reject** flow where applicable
- [x] Owner agent shows **time_extension_allowed: false**
- [x] Font family is **'Inter' or system fallback**
- [x] Colors match the **specified palette**
- [x] All text is **within SVG bounds** (no overflow)
- [x] SVG viewBox is properly sized
- [x] High resolution and professional quality
- [x] Valid SVG syntax (no invalid attributes)

---

## Version History

- **Final Revision (2025-12-12):** Complete rebuild of all mockups
  - New file naming: `{type}-{number}-{name}.svg`
  - Correct budget model throughout: 390/310/700 MNOK
  - 35 MNOK deficit prominently displayed
  - All 6 core mockups completed
  - Norwegian language
  - Consistent Inter font styling
  - Professional design quality

---

## Summary

**6 of 6 core mockups complete** ✅

All mockups now correctly show:
- **390 MNOK locked** (12 packages)
- **310 MNOK available** (3 negotiable packages)
- **700 MNOK total budget**
- **345 MNOK baseline estimates**
- **35 MNOK deficit challenge** ⚠

The mockup set provides complete visual design guidance for the POC implementation.
