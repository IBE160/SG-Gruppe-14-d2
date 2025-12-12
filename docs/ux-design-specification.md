# UX Design Specification
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 2.0
**Date:** 2025-12-11
**Status:** Updated for POC Scope (3 Negotiable WBS + 4 AI Agents)
**UX Designer:** [To be assigned]
**Changelog:**
- v2.0: POC scope - 3 negotiable + 12 locked WBS, 4 AI agents (Owner + 3 suppliers), explicit accept/reject flow, budget display (310/650/700)
- v1.1: Added sections 3.7-3.9 for Gantt chart, precedence diagram, and history/timeline views

---

## Document Purpose

This UX Design Specification provides detailed visual and interaction design guidelines for implementing the Nye Hædda Barneskole Project Management Simulation. It serves as the bridge between the Product Requirements Document (PRD) and frontend implementation.

**Audience:**
- Frontend developers (primary)
- Product owner and stakeholders (review/approval)
- QA team (UI testing)

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Visual Design System](#2-visual-design-system)
3. [Page Wireframes](#3-page-wireframes)
4. [User Flows](#4-user-flows)
5. [Component Specifications](#5-component-specifications)
6. [Interaction Patterns](#6-interaction-patterns)
7. [Responsive Design](#7-responsive-design)
8. [Accessibility](#8-accessibility)
9. [Implementation Notes](#9-implementation-notes)

---

## 1. Design Principles

### 1.1 Core Design Philosophy

**DP-1: Professional Academic Context**
- This is an educational tool for university-level students and professionals
- Design should feel serious, credible, and academic (not gamified or playful)
- Use professional color palette, clean typography, structured layouts
- Avoid: Bright colors, cartoonish elements, excessive animations

**DP-2: Clarity Over Cleverness**
- Every UI element should have an obvious purpose
- No hidden features or "Easter eggs"
- Labels and buttons use clear, action-oriented language
- Users should never wonder "What does this button do?"

**DP-3: Immediate Feedback**
- All user actions trigger instant visual response
- Loading states for async operations (AI responses)
- Success/error states clearly communicated
- Real-time updates (budget, timeline) without page refresh

**DP-4: Progressive Disclosure**
- Don't overwhelm users with everything at once
- Start with essentials (constraints, WBS list)
- Reveal details on demand (expand WBS item, view chat history)
- Advanced features (export) appear after completion

**DP-5: Consistency & Predictability**
- Same actions always produce same results
- UI patterns repeat across pages (header, buttons, modals)
- Consistent terminology (never "Submit" in one place and "Confirm" in another)

---

## 2. Visual Design System

### 2.1 Color Palette

**Primary Colors:**
```
Primary Blue:   #3B82F6  (rgb(59, 130, 246))  - Primary CTAs, links
Primary Dark:   #2563EB  (rgb(37, 99, 235))   - Hover states
```

**Semantic Colors:**
```
Success Green:  #10B981  (rgb(16, 185, 129))  - Completed items, validation success
Warning Yellow: #F59E0B  (rgb(245, 158, 11))  - Warnings, approaching limits
Error Red:      #EF4444  (rgb(239, 68, 68))   - Errors, over budget/timeline
```

**Neutral Grays:**
```
Gray 900:       #111827  (rgb(17, 24, 39))    - Primary text
Gray 700:       #374151  (rgb(55, 65, 81))    - Secondary text
Gray 500:       #6B7280  (rgb(107, 114, 128)) - Placeholder text
Gray 300:       #D1D5DB  (rgb(209, 213, 219)) - Borders
Gray 100:       #F3F4F6  (rgb(243, 244, 246)) - Background accents
Gray 50:        #F9FAFB  (rgb(249, 250, 251)) - Page background
White:          #FFFFFF  (rgb(255, 255, 255)) - Cards, modals
```

**Usage Guidelines:**
- Primary Blue: CTAs, links, active states
- Gray 900: Body text (high contrast)
- Gray 700: Labels, secondary information
- Gray 50: Page backgrounds
- White: Cards, panels, modals (creates depth)

---

### 2.2 Typography

**Font Family:**
```
Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
Monospace: 'Fira Code', 'Courier New', monospace (for WBS codes, numbers)
```

**Font Sizes (Tailwind CSS scale):**
```
text-xs:    12px / 16px line-height  - Small labels, timestamps
text-sm:    14px / 20px              - Body text, form inputs
text-base:  16px / 24px              - Default body text
text-lg:    18px / 28px              - Section headings
text-xl:    20px / 28px              - Page headings
text-2xl:   24px / 32px              - Dashboard title
text-3xl:   30px / 36px              - Success/error modals
```

**Font Weights:**
```
font-normal:    400  - Body text
font-medium:    500  - Labels, emphasized text
font-semibold:  600  - Buttons, headings
font-bold:      700  - Modal titles, warnings
```

**Typography Hierarchy Example:**
```
Page Title (Dashboard): text-2xl font-bold text-gray-900
Section Heading (WBS List): text-lg font-semibold text-gray-900
Body Text (Chat messages): text-sm font-normal text-gray-700
Button Text: text-sm font-semibold text-white
```

---

### 2.3 Spacing System

**Tailwind Spacing Scale (4px base unit):**
```
space-1:  4px    - Tight spacing (icon + label)
space-2:  8px    - Small gaps (form elements)
space-3:  12px   - Medium gaps (buttons, cards)
space-4:  16px   - Standard gaps (sections)
space-6:  24px   - Large gaps (page sections)
space-8:  32px   - Extra large (modal padding)
space-12: 48px   - Section dividers
```

**Common Patterns:**
- Card padding: `p-6` (24px)
- Button padding: `px-4 py-2` (16px horizontal, 8px vertical)
- Section spacing: `mb-6` or `space-y-6` (24px between sections)
- Modal padding: `p-8` (32px)

---

### 2.4 Border & Shadows

**Borders:**
```
Border Radius:
  rounded-sm:  2px   - Subtle (progress bars)
  rounded:     4px   - Default (buttons, inputs)
  rounded-md:  6px   - Cards
  rounded-lg:  8px   - Modals
  rounded-xl:  12px  - Large cards

Border Widths:
  border:      1px   - Default (inputs, cards)
  border-2:    2px   - Emphasized (focused inputs)
```

**Shadows:**
```
shadow-sm:   Small shadow for inputs
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05)

shadow:      Default card shadow
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)

shadow-md:   Modal shadow
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)

shadow-lg:   Elevated elements (dropdown menus)
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)
```

---

### 2.5 Icons

**Icon Library:** Lucide React or Heroicons (consistent style)

**Icon Sizes:**
```
w-4 h-4:   16px  - Small (inline with text)
w-5 h-5:   20px  - Medium (buttons)
w-6 h-6:   24px  - Large (headers)
w-8 h-8:   32px  - Extra large (empty states)
```

**Common Icons:**
- User menu: `UserCircle` icon
- Logout: `LogOut` icon
- Help: `HelpCircle` icon
- Close modal: `X` icon
- Status completed: `CheckCircle` icon (green)
- Status pending: `Circle` icon (gray)
- Send message: `Send` icon
- Document: `FileText` icon
- Export: `Download` icon
- Warning: `AlertTriangle` icon (yellow)
- Error: `XCircle` icon (red)

---

## 3. Page Wireframes

### 3.1 Login Page

**Layout:**
```
┌────────────────────────────────────────────────────┐
│                                                    │
│              [Logo/Project Title]                  │
│     Nye Hædda Barneskole Simulation                │
│                                                    │
│                                                    │
│        ┌──────────────────────────┐                │
│        │  [Login Form]            │                │
│        │                          │                │
│        │  Email                   │                │
│        │  [___________________]   │                │
│        │                          │                │
│        │  Passord                 │                │
│        │  [___________________]   │                │
│        │                          │                │
│        │     [Logg Inn]           │                │
│        │                          │                │
│        │  Har du ikke konto?      │                │
│        │  [Registrer deg]         │                │
│        └──────────────────────────┘                │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Specifications:**
- **Container:** Max-width 400px, centered horizontally and vertically
- **Background:** Gray-50 (#F9FAFB)
- **Form Card:** White background, shadow-md, rounded-lg, p-8
- **Logo/Title:** text-2xl font-bold text-gray-900, mb-8
- **Input Fields:**
  - Label: text-sm font-medium text-gray-700, mb-1
  - Input: border border-gray-300, rounded, px-3 py-2, w-full
  - Focus state: border-blue-500, ring-2 ring-blue-200
- **Primary Button (Logg Inn):**
  - bg-blue-600, text-white, font-semibold
  - px-4 py-2, rounded, w-full
  - Hover: bg-blue-700
- **Secondary Link (Registrer deg):**
  - text-blue-600, text-sm, underline
  - Hover: text-blue-700

**States:**
- **Default:** Clean form
- **Error:** Red border on input, red text below: "Feil e-post eller passord"
- **Loading:** Button shows spinner, text changes to "Logger inn..."

---

### 3.2 Dashboard (Main Game View - v2.0 POC Scope)

**Layout (Desktop):**
```
┌────────────────────────────────────────────────────────────────────┐
│ Header                                              [User Menu ▼]  │
│ Nye Hædda Barneskole                                   [Hjelp]     │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Prosjektbegrensninger                                             │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │ Tilgjengelig: [=====>       ] 105 / 310 MNOK (34%)        │   │
│  │ Låst:         650 MNOK (12 kontraktfestede leverandører)   │   │
│  │ Totalt:       755 / 700 MNOK ❌ (overskredet med 55 MNOK)  │   │
│  │ Frist:        15. mai 2026                                 │   │
│  │ Forventet:    10. april 2026  ✓                            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  Fremdrift:  1 / 3 forhandlbare pakker fullført  |  5 forhandlinger│
│                                                                    │
│  ┌─WBS-liste──────────────────────┐  ┌──────────────────────┐     │
│  │ FORHANDLBARE (3)               │  │ [Send Inn Plan]      │     │
│  │                                │  │                      │     │
│  │ 🔵 ⚪ 1.3.1 Grunnarbeid        │  │ [Eksporter Økt]      │     │
│  │    💬 Kan forhandles           │  │                      │     │
│  │    [Kontakt Leverandør/Eier]  │  │ [Hjelp]              │     │
│  │                                │  └──────────────────────┘     │
│  │ 🔵 🟢 2.1 Fundamentering       │                               │
│  │    105 MNOK, 2.5 mnd           │                               │
│  │    Kari Andersen               │                               │
│  │    [Reforhandle]               │                               │
│  │                                │                               │
│  │ 🔵 ⚪ 3.2 Råbygg                │                               │
│  │    💬 Kan forhandles           │                               │
│  │    [Kontakt Leverandør/Eier]  │                               │
│  │                                │                               │
│  │ KONTRAKTFESTET (12)            │                               │
│  │ 🔒 1.1 Prosjektering           │                               │
│  │    50 MNOK, 2 mnd              │                               │
│  │    Arkitekt AS (forhåndsbestilt)│                              │
│  │ ... (10 more locked, scrollable)│                              │
│  └────────────────────────────────┘                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Specifications:**

**Header:**
- Height: 64px
- Background: White
- Border-bottom: 1px solid gray-300
- Title: text-xl font-bold text-gray-900
- User menu: Dropdown (UserCircle icon + name)
  - Dropdown items: "Min Profil", "Logg Ut"

**Constraint Panel (v2.0 - 3-Tier Budget Display):**
- Background: White, rounded-md, shadow, p-6, mb-6
- **Budget Display (3 rows):**
  1. **Tilgjengelig (Available)** - For 3 negotiable WBS:
     - Height: 20px, rounded-full progress bar
     - Background: gray-200
     - Fill: Green (0-300 MNOK), yellow (300-310), red (>310)
     - Label: "Tilgjengelig: 105 / 310 MNOK (34%)"
  2. **Låst (Locked)** - For 12 contracted WBS:
     - Text display only (no bar): "Låst: 650 MNOK (12 kontraktfestede leverandører)"
     - text-sm text-gray-600
  3. **Totalt (Total)** - Sum validation:
     - Text display: "Totalt: 755 / 700 MNOK ❌ (overskredet med 55 MNOK)"
     - Color: Red if >700, yellow if >680, green if ≤680
     - Checkmark (✓) or X (❌) icon
- Deadline & Projected:
  - Grid layout: 2 columns
  - Labels: text-sm font-medium text-gray-700
  - Values: text-base font-semibold
  - Green checkmark if projected ≤ May 15 2026, red X if late

**Quick Stats:**
- text-sm text-gray-600
- Separated by " | " (vertical divider)

**WBS List (v2.0 - 3 Negotiable + 12 Locked):**
- Background: White, rounded-md, shadow, p-6
- Max-height: 500px, overflow-y: auto (scrollable)
- **Section Headers:**
  - "FORHANDLBARE (3)" - text-sm font-bold text-blue-600, mb-2
  - "KONTRAKTFESTET (12)" - text-sm font-bold text-gray-500, mt-4, mb-2
- **Negotiable WBS Items (3):**
  - Padding: py-3, border-bottom: 1px gray-200
  - **Blue indicator:** Blue circle (🔵) or blue left border (4px solid blue-500)
  - Status icon: ⚪ (pending) or 🟢 (completed), w-5 h-5
  - Badge: "💬 Kan forhandles" - bg-blue-100, text-blue-700, text-xs, px-2 py-1, rounded
  - WBS code + name: text-sm font-medium text-gray-900
  - Button: "Kontakt Leverandør/Eier" (pending) or "Reforhandle" (completed)
  - Interactive: Hover bg-blue-50, cursor-pointer
- **Locked WBS Items (12):**
  - Padding: py-2, border-bottom: 1px gray-100
  - **Lock indicator:** 🔒 icon or gray left border (2px solid gray-300)
  - Badge: "Kontraktfestet" - bg-gray-100, text-gray-600, text-xs, px-2 py-1, rounded
  - WBS code + name: text-sm font-normal text-gray-600
  - Pre-committed details: "50 MNOK, 2 mnd | Arkitekt AS (forhåndsbestilt)"
  - Non-interactive: No hover state, no buttons, opacity-75

**Action Buttons Sidebar:**
- Sticky position (remains visible on scroll)
- Buttons: Full width, mb-3
- Primary button: "Send Inn Plan" - bg-blue-600
- Secondary: "Eksporter Økt", "Hjelp" - bg-white border

---

### 3.3 Chat/Negotiation Page (v2.0 - Explicit Accept/Reject + Owner Option)

**Layout (Desktop):**
```
┌────────────────────────────────────────────────────────────────────┐
│ [← Tilbake til Oversikt]    Kari Andersen - Fundamentering         │
│                             WBS 2.1 | 💬 Kan forhandles            │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ ┌─Chat Window──────────────────────┐  ┌─Dokumenter────────────┐  │
│ │ (scrollable)                     │  │                        │  │
│ │                                  │  │ 📄 WBS                 │  │
│ │          ┌───────────────────┐   │  │ 📄 Kravspesifikasjon   │  │
│ │          │ Bruker: Jeg trenger│  │  │ 📄 Prosjektbeskrivelse │  │
│ │          │ et pristilbud...  │   │  │                        │  │
│ │          └───────────────────┘   │  │ Forhandler med:        │  │
│ │                                  │  │ [X] Leverandør         │  │
│ │ ┌───────────────────┐            │  │ [ ] Eier (Kommune)     │  │
│ │ │ AI: Basert på...  │            │  └────────────────────────┘  │
│ │ │ 120 MNOK, 3 mnd   │            │                               │
│ │ └───────────────────┘            │                               │
│ │ [✓ Godta: 120 MNOK] [✗ Avslå]   │                               │
│ │                                  │                               │
│ │          ┌───────────────────┐   │                               │
│ │          │ Bruker: For høyt..│   │                               │
│ │          └───────────────────┘   │                               │
│ │                                  │                               │
│ │ ┌───────────────────┐            │                               │
│ │ │ AI: Jeg kan gjøre │            │                               │
│ │ │ 105 MNOK, 2.5 mnd │            │                               │
│ │ └───────────────────┘            │                               │
│ │ [✓ Godta: 105 MNOK] [✗ Avslå]   │                               │
│ │                                  │                               │
│ │ ... (more messages)              │                               │
│ └──────────────────────────────────┘                               │
│                                                                    │
│ ┌──Meldingsinput────────────────────────────────────┐              │
│ │ [____________________________________]  [Send →]  │              │
│ └───────────────────────────────────────────────────┘              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

**Specifications:**

**Header:**
- Same as Dashboard header
- Back button: "← Tilbake til Oversikt" - text-sm text-blue-600
- Context: Supplier name + role (text-lg font-semibold) | WBS item (text-sm text-gray-600)

**Chat Window:**
- Background: gray-50, rounded-md, p-4
- Height: calc(100vh - 300px), overflow-y: auto
- Auto-scroll to bottom on new message

**Message Bubbles:**
- **User Message:**
  - Align: Right (ml-auto, max-w-2/3)
  - Background: blue-600, text-white
  - Padding: px-4 py-2, rounded-lg (rounded-br-none for tail effect)
  - text-sm
- **AI Message:**
  - Align: Left (mr-auto, max-w-2/3)
  - Background: white, text-gray-900, shadow-sm
  - Padding: px-4 py-2, rounded-lg (rounded-bl-none)
  - text-sm
- **System Message:**
  - Align: Center (mx-auto)
  - Background: gray-200, text-gray-700
  - Padding: px-3 py-1, rounded, text-xs, italic

**Accept/Reject Offer Buttons (v2.0 - Explicit Action Required):**
- Appears below AI message when offer detected (cost + duration OR budget adjustment)
- **Two buttons side-by-side:**
  1. **✓ Godta Button:**
     - Background: green-600, text-white, text-xs, font-semibold
     - px-3 py-1, rounded, mt-2, mr-2
     - Hover: green-700
     - Label: "✓ Godta: 105 MNOK, 2.5 mnd" (shows offer details)
  2. **✗ Avslå Button:**
     - Background: gray-300, text-gray-700, text-xs, font-semibold
     - px-3 py-1, rounded, mt-2
     - Hover: gray-400
     - Label: "✗ Avslå"
- **Behavior:**
  - "Godta" triggers confirmation modal (Section 3.4)
  - "Avslå" dismisses offer, hides buttons, chat continues
  - NO automatic acceptance - user MUST click one of the buttons
- **Owner Offers (Budget Increase):**
  - Godta label: "✓ Godta: +15 MNOK budsjett" (for budget increase)
  - Same button styling as supplier offers

**Document Sidebar:**
- Background: white, rounded-md, shadow, p-4
- Width: 200px (fixed)
- Links: text-sm text-blue-600, flex items-center, py-2
- Icon: FileText, w-4 h-4, mr-2
- Hover: underline

**Message Input:**
- Background: white, border border-gray-300, rounded-md, p-3
- Textarea: resize-none, h-16, border-none, focus:outline-none
- Send button: bg-blue-600, text-white, px-4 py-2, rounded, ml-2
- Icon: Send (w-5 h-5)

**Loading State (AI Typing):**
- Gray bubble with animated dots: "Bjørn ser gjennom spesifikasjonene..."

---

### 3.3.1 Modal: Supplier/Owner Selection (v2.0 - NEW)

**Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│                                                             [X] │
│  Velg Forhandlingspartner                                       │
│  WBS 1.3.1 - Grunnarbeid                                        │
│                                                                 │
│  Hvem vil du forhandle med for denne pakken?                   │
│                                                                 │
│  ┌─LEVERANDØRER────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌──Bjørn Eriksen─────────────────────────────────┐     │   │
│  │  │ 🏗️ Grunnarbeid-specialist                      │     │   │
│  │  │ Strategi: Pris/kvalitet-avveining               │     │   │
│  │  │ "Kan redusere pris ved kvalitetsjustering"      │     │   │
│  │  │                            [Velg Leverandør →]  │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  │                                                          │   │
│  │  ┌──Kari Andersen─────────────────────────────────┐     │   │
│  │  │ 🏗️ Fundamentering-specialist                   │     │   │
│  │  │ Strategi: Tid/kostnad-avveining                 │     │   │
│  │  │ "Kan levere raskere mot høyere pris"            │     │   │
│  │  │                            [Velg Leverandør →]  │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  │                                                          │   │
│  │  ┌──Per Johansen──────────────────────────────────┐     │   │
│  │  │ 🏗️ Råbygg-specialist                           │     │   │
│  │  │ Strategi: Omfangsreduksjon                      │     │   │
│  │  │ "Kan foreslå funksjonsreduksjoner for besparelse"│   │   │
│  │  │                            [Velg Leverandør →]  │     │   │
│  │  └─────────────────────────────────────────────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─EIER (KOMMUNE)───────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌──Anne-Lise Berg─────────────────────────────────┐    │   │
│  │  │ 🏛️ Prosjekteier (Kommune)                       │    │   │
│  │  │ Makt: Budsjettøkning, omfangsreduksjon          │    │   │
│  │  │ ⚠️ ALDRI tidsfrist-forlengelse                  │    │   │
│  │  │ "Kan godkjenne budsjettøkning ved god begrunnelse" │  │
│  │  │                            [Velg Eier →]        │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│                                [Avbryt]                         │
└─────────────────────────────────────────────────────────────────┘
```

**Specifications:**
- Overlay: bg-black bg-opacity-50 (semi-transparent)
- Modal: bg-white, rounded-lg, shadow-lg, p-8, max-w-3xl
- Title: text-xl font-bold text-gray-900, mb-2
- WBS context: text-sm text-gray-600, mb-4
- Section headers:
  - "LEVERANDØRER" - text-sm font-bold text-blue-600, mb-3
  - "EIER (KOMMUNE)" - text-sm font-bold text-purple-600, mb-3
- **Agent Cards:**
  - Background: white, border border-gray-300, rounded-md, p-4, mb-3
  - Hover: border-blue-500, bg-blue-50
  - Name: text-base font-semibold text-gray-900
  - Icon: 🏗️ (suppliers) or 🏛️ (owner), w-6 h-6
  - Specialty: text-sm text-gray-700
  - Strategy: text-sm font-medium text-blue-600
  - Description: text-xs text-gray-600, italic
  - Button: "Velg Leverandør →" or "Velg Eier →" - bg-blue-600, text-white, px-4 py-2, rounded, float-right
- **Owner Card Distinction:**
  - Border: border-purple-300
  - Warning badge: "⚠️ ALDRI tidsfrist-forlengelse" - bg-red-100, text-red-700, text-xs, px-2 py-1, rounded, font-bold
- Cancel button: bg-white border, bottom center

**Behavior:**
- Triggered from Dashboard when user clicks "Kontakt Leverandør/Eier" on negotiable WBS item
- User selects one of 4 agents → navigate to Chat page with selected agent
- Modal dismisses on selection or cancel

---

### 3.4 Modal: Commitment Confirmation

**Layout:**
```
┌─────────────────────────────────────────────┐
│                                         [X] │
│  Bekreft Forpliktelse                       │
│                                             │
│  WBS-oppgave:   1.3.1 - Grunnarbeid         │
│  Leverandør:    Bjørn Eriksen               │
│  Kostnad:       105 MNOK                    │
│  Varighet:      2.5 måneder                 │
│                                             │
│  Dette vil oppdatere prosjektplanen din.    │
│  Fortsette?                                 │
│                                             │
│           [Avbryt]     [Bekreft]            │
└─────────────────────────────────────────────┘
```

**Specifications:**
- Overlay: bg-black bg-opacity-50 (semi-transparent)
- Modal: bg-white, rounded-lg, shadow-lg, p-8, max-w-md
- Title: text-xl font-bold text-gray-900, mb-4
- Details: Grid layout, text-sm
  - Labels: font-medium text-gray-700
  - Values: font-semibold text-gray-900
- Message: text-sm text-gray-600, my-4
- Buttons:
  - Avbryt: bg-white, border border-gray-300, text-gray-700, px-4 py-2, rounded
  - Bekreft: bg-blue-600, text-white, px-4 py-2, rounded, ml-3
  - Hover states: Darken background

---

### 3.5 Modal: Validation Error

**Layout:**
```
┌─────────────────────────────────────────────┐
│                                         [X] │
│  ❌ Planvalidering Mislyktes                │
│                                             │
│  Feil funnet:                               │
│                                             │
│  • Budsjett overskredet med 50 MNOK         │
│    Total: 750 MNOK (Grense: 700 MNOK)      │
│                                             │
│  • Prosjektet forsinket til 20. mai 2026    │
│    (Frist: 15. mai 2026)                    │
│                                             │
│  Forslag:                                   │
│  Vurder å reforhandle disse kostbare        │
│  oppgavene:                                 │
│  - 2.1 Råbygg (250 MNOK)                    │
│  - 3.4 VVS-installasjon (180 MNOK)          │
│                                             │
│             [Tilbake til Planlegging]       │
└─────────────────────────────────────────────┘
```

**Specifications:**
- Same overlay and modal structure as confirmation
- Title: Red error icon (XCircle) + text-xl font-bold text-red-600
- Error list:
  - Bullets: red dot (w-2 h-2 rounded-full bg-red-500)
  - Error text: text-sm font-medium text-gray-900
  - Details: text-xs text-gray-600, pl-6 (indented)
- Suggestions:
  - Section title: text-sm font-semibold text-gray-700
  - Suggestion list: text-sm text-gray-600
- Button: bg-blue-600, text-white, w-full

---

### 3.6 Modal: Success

**Layout:**
```
┌─────────────────────────────────────────────┐
│                                         [X] │
│  🎉 Plan Godkjent!                          │
│                                             │
│  Gratulerer! Du har lykkes med å           │
│  fullføre planleggingsfasen.                │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ Total Kostnad:     698 MNOK           │ │
│  │ Fullføringsdato:   10. mai 2026       │ │
│  │ Tid Brukt:         47 minutter        │ │
│  │ Forhandlinger:     23                 │ │
│  │ Reforhandlinger:   3                  │ │
│  └───────────────────────────────────────┘ │
│                                             │
│        [Eksporter Økt]                      │
│        [Start Nytt Spill]                   │
│                                             │
└─────────────────────────────────────────────┘
```

**Specifications:**
- Title: Green success icon (CheckCircle) + text-2xl font-bold text-green-600
- Message: text-base text-gray-700, mb-4
- Stats table:
  - Background: gray-50, rounded-md, p-4
  - Grid: 2 columns (label | value)
  - Labels: text-sm font-medium text-gray-700
  - Values: text-sm font-semibold text-gray-900
- Buttons: Full width, mb-2
  - Eksporter: bg-blue-600 (primary)
  - Start Nytt: bg-white border (secondary)

---

### 3.7 Gantt Chart View

**Layout (Desktop):**
```
┌────────────────────────────────────────────────────────────────────┐
│ [Nye Hædda]  📊 Dashbord | 📈 Gantt-diagram | 🔀 Presedensdiagram  │
│                                                    🕒 Historikk  [User] │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Gantt-diagram                                                      │
│                                                                    │
│ ┌──Controls────────────────────────────────────────────────────┐ │
│ │ Visning: [Måned ▼] | Zoom: [=====>    ] | ☑ Vis kritisk sti │ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌──Timeline─────────────────────────────────────────────────────┐│
│ │       Jan 2025  Feb  Mar  Apr  Mai  Jun ... Mai 2026          ││
│ │                           ↓ Idag                               ││
│ │ 1.1   [========]                                               ││
│ │ 1.3.1   [==========]                                           ││
│ │ 2.1       [█████████████░░░░] 45%                              ││
│ │ 2.2         └──→[──────]                                       ││
│ │ ...                                                            ││
│ │                                                                ││
│ └────────────────────────────────────────────────────────────────┘│
│                                                                    │
│ ┌──Info Panel──────────────────────────────────────────────────┐ │
│ │ Forventet ferdig: 10. april 2026 ✓                            │ │
│ │ Budsjett brukt:   450 / 700 MNOK (64%)                        │ │
│ │ Kritisk sti:      15 måneder                                  │ │
│ │                                                                │ │
│ │                           [Eksporter Gantt (PNG)]             │ │
│ └────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
```

**Specifications:**

**Navigation Tabs:**
- Height: 48px, background: white, border-bottom: 2px solid gray-200
- Active tab: border-bottom-color: blue-600, text-blue-600, font-semibold
- Inactive tabs: text-gray-600, hover: text-gray-900
- Icons: Lucide icons (BarChart3, GanttChart, Network)
- Historikk button: Positioned absolute right, blue-600 button with Clock icon

**Controls Panel:**
- Background: white, rounded-md, shadow-sm, p-4, mb-4
- View selector: Dropdown with options "Måned", "Uke", "Dag"
- Zoom slider: Input range 50-200%, default 100%
- Filter checkbox: Styled checkbox + label

**Timeline Canvas:**
- Background: white, rounded-md, shadow, p-6
- Min-height: 500px, overflow: auto (horizontal + vertical scroll)
- Timeline header:
  - Months displayed as text-sm font-medium text-gray-700
  - Grid lines: 1px dashed gray-300 for month boundaries
  - "Idag" marker: Blue vertical dashed line (border-left: 2px dashed blue-500)
- Task bars:
  - Height: 32px, margin-bottom: 8px
  - **Completed:** bg-green-500, 100% opacity
  - **In-progress:** bg-yellow-500, with percentage label (text-xs white)
  - **Planned:** border-2 border-gray-400, bg-transparent
  - **Critical path:** border: 3px solid red-500
- Dependency arrows:
  - Normal: stroke-gray-400, stroke-width: 2px
  - Critical: stroke-red-500, stroke-width: 3px, stroke-dasharray: "5,5"
- WBS labels (left): text-sm font-medium text-gray-900, width: 80px

**Info Panel:**
- Background: gray-50, rounded-md, p-4
- Stats: text-sm, font-medium
- Checkmark/X icons: Lucide Check/X icons with conditional colors
- Export button: bg-blue-600, text-white, px-4 py-2, rounded

**Real-time Updates:**
- When plan changes (commit/renegotiate), re-render chart with smooth transition (300ms)
- Critical path recalculation triggers red outline updates

**Reference:** mockup-08-gantt-chart-view.svg, PRD FR-9.1

---

### 3.8 Precedence Diagram View

**Layout (Desktop):**
```
┌────────────────────────────────────────────────────────────────────┐
│ [Nye Hædda]  📊 Dashbord | 📈 Gantt-diagram | 🔀 Presedensdiagram  │
│                                                    🕒 Historikk  [User] │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ Presedensdiagram                                                   │
│                                                                    │
│ ┌──Controls────────────────────────────────────────────────────┐ │
│ │ Layout: [Venstre→Høyre ▼] | Zoom: [=====>    ]              │ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│ ┌──Network Diagram──────────────────────┐ ┌──Info Panels─────┐  │
│ │                                        │ │ Kritisk Sti:     │  │
│ │  (START)                               │ │ • 1.1 → 1.3.1    │  │
│ │     ↓                                  │ │ • 2.1 → 3.2      │  │
│ │  ┌────────┐                            │ │ • ...            │  │
│ │  │  1.1   │──→┌────────┐               │ │ Total: 15 mnd   │  │
│ │  │Proj... │   │ 1.3.1  │               │ │                  │  │
│ │  │2m, 50M │   │Grunn..│                │ │ Parallelle Stier:│  │
│ │  └────────┘   │2.5m,105M│               │ │ Sti A: 12 mnd   │  │
│ │               └────────┘                │ │ Sti B: 10 mnd   │  │
│ │                   ↓                     │ │                  │  │
│ │               ┌────────┐                │ │ Fremdrift:       │  │
│ │               │  2.1   │ (CRITICAL)     │ │ Fullført: 4/15   │  │
│ │               │Råbygg  │                │ │ Gjenstår: 11     │  │
│ │               └────────┘                │ │                  │  │
│ │                   ↓                     │ │ Nettverksstat:   │  │
│ │                 (END)                   │ │ Oppgaver: 15     │  │
│ │                                        │ │ Avhengigheter:18 │  │
│ └────────────────────────────────────────┘ │ Dybde: 5 nivåer  │  │
│                                             └──────────────────┘  │
│                          [Eksporter Diagram (PNG)]                │
└────────────────────────────────────────────────────────────────────┘
```

**Specifications:**

**Network Canvas:**
- Background: white, rounded-md, shadow, p-6
- Min-height: 600px, width: 70% of viewport
- Pan/zoom enabled: Use react-flow or cytoscape.js
- Layout algorithm: Dagre (hierarchical left-to-right)

**Node Styling:**
- Size: 180px × 100px (desktop), 140px × 80px (tablet)
- Border-radius: 8px, shadow-sm
- Border: 2px solid
- **Colors:**
  - Completed: bg-green-50, border-green-500
  - In-progress: bg-yellow-50, border-yellow-500
  - Planned: bg-white, border-gray-300
  - Critical path: border-red-500, border-width: 3px
- **Content:**
  - WBS code: text-sm font-bold text-gray-900 (top)
  - Name: text-xs text-gray-700 (truncated if long)
  - Duration: text-xs text-gray-600
  - Cost: text-xs text-gray-600
  - Slack time: text-xs text-blue-600 (bottom right)
- **START/END nodes:** Circular (w-20 h-20), bg-gray-200, border-gray-400

**Arrows/Edges:**
- **Normal dependencies:** stroke-gray-400, stroke-width: 2px, arrow-head
- **Critical path:** stroke-red-500, stroke-width: 3px

**Interactive Features:**
- **Hover on node:** Highlight incoming/outgoing arrows with blue-400
- **Click on node:** Show popup modal with full WBS details
- **Drag to pan:** Canvas is draggable
- **Scroll to zoom:** Mouse wheel or pinch gesture

**Info Panels (Right Sidebar):**
- Width: 30% of viewport, background: gray-50, rounded-md, p-4
- 4 panels stacked vertically:
  - Critical Path Summary
  - Parallel Paths
  - Progress Stats
  - Network Statistics
- Each panel: bg-white, rounded, p-3, mb-3, shadow-sm
- Titles: text-sm font-semibold text-gray-900
- Content: text-xs text-gray-700, bullet lists

**Layout Mode Selector:**
- Dropdown: "Venstre→Høyre" (default), "Topp→Bunn", "Hierarkisk"
- Triggers re-layout animation (500ms transition)

**Reference:** mockup-09-precedence-diagram.svg, PRD FR-9.2

---

### 3.9 History/Timeline View (Overlay Panel)

**Layout (Full-screen Overlay):**
```
┌────────────────────────────────────────────────────────────────────┐
│ 🕒 Historikk                                    ✕ Lukk historikk  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│ ┌──Event Timeline──────┐  ┌──Comparison View──────────────────┐  │
│ │ [Filter: Alle ▼]     │  │ Før (Versjon 7) | Etter (Versjon 8)│  │
│ │                      │  │                                     │  │
│ │ Versjon 8 (Nå)       │  │ ┌─────────────┐  ┌─────────────┐   │  │
│ │ ⦿ Forpliktet         │  │ │ Råbygg      │  │ Råbygg      │   │  │
│ │   2.1 Råbygg         │  │ │ 200 MNOK    │  │ 185 MNOK    │   │  │
│ │   15. mar 13:24      │  │ │ [████████]  │  │ [████████]  │   │  │
│ │                      │  │ └─────────────┘  └─────────────┘   │  │
│ │ ○ Versjon 7          │  │     (rødt)          (grønt)        │  │
│ │   Fjernet 3.2        │  │                                     │  │
│ │   15. mar 13:20      │  │ Endringer:                          │  │
│ │                      │  │ • Budsjett: -15 MNOK (2.1% ↓)      │  │
│ │ ○ Versjon 6          │  │ • Tidslinje: -5 dager (1.5% raskere)│ │
│ │   Reforhandlet 1.3.1 │  │ • Kritisk sti: Uendret              │  │
│ │   15. mar 12:45      │  │                                     │  │
│ │                      │  │ Kaskadeeffekter:                    │  │
│ │ ○ Versjon 5          │  │ 1. WBS 2.2 start flyttet 5 d tid.. │  │
│ │   ...                │  │ 2. Kritisk sti opprettholdt         │  │
│ │ (scrollable)         │  │ 3. Ingen nye forsinkelser           │  │
│ │                      │  │                                     │  │
│ │                      │  │ [← Forrige] [Neste →]              │  │
│ │ (32 hendelser)       │  │ [Sammenlign med nåværende]         │  │
│ └──────────────────────┘  │ [Eksporter historikk (JSON)]       │  │
│                            └─────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

**Specifications:**

**Overlay Container:**
- Position: fixed, z-index: 50
- Background: rgba(0, 0, 0, 0.5) (semi-transparent backdrop)
- Click backdrop to close (or use ✕ button)
- Animation: Slide-in from right (300ms ease-in-out)

**Panel:**
- Background: white, full height, 90% width (max 1400px)
- Position: right: 0
- Border-left: 1px solid gray-300
- Padding: p-6

**Header:**
- Title: text-xl font-bold text-gray-900, with Clock icon
- Close button: Absolute top-right, red-600 text, hover: red-700
- Border-bottom: 1px solid gray-200, pb-4

**Left Sidebar - Event Timeline:**
- Width: 400px, border-right: 1px solid gray-200
- Filter dropdown: mb-4, options: "Alle", "Forhandlinger", "Planendringer"
- Event list:
  - Scrollable: max-height: calc(100vh - 200px), overflow-y: auto
  - Each event: py-3, border-bottom: 1px gray-100
  - **Current/selected event:** bg-blue-50, border-left: 3px blue-600
  - **Other events:** hover: bg-gray-50
  - Event icon: Circle (filled for current, outline for past)
  - Action type icons: CheckCircle (commit), XCircle (remove), RefreshCw (renegotiate)
  - Timestamp: text-xs text-gray-500
  - WBS description: text-sm font-medium text-gray-900
- Total count: text-xs text-gray-500, at bottom

**Right Panel - Comparison View:**
- Width: calc(100% - 400px - 48px)
- Headers: "Før (Versjon N)" | "Etter (Versjon N+1)"
  - text-lg font-semibold text-gray-900
  - Separated by vertical divider
- **Gantt Comparison:**
  - Side-by-side mini Gantt charts (simplified view)
  - Old state: Red bars, strikethrough for removed tasks
  - New state: Green bars, highlighted for added/changed tasks
  - Height: 300px
- **Change Summary Stats:**
  - Background: blue-50, rounded, p-3
  - Stats displayed with icons (TrendingDown for reductions, TrendingUp for increases)
  - Text: text-sm font-medium
- **Cascade Effects Panel:**
  - Background: gray-50, rounded, p-3
  - Numbered list (1, 2, 3...)
  - Each effect: text-xs text-gray-700
  - Shows up to 5 most significant impacts

**Action Buttons:**
- Row of buttons at bottom
- Navigation: "← Forrige versjon" | "Neste versjon →" (ghost buttons)
- Compare: "Sammenlign med nåværende" (secondary button)
- Export: "Eksporter historikk (JSON)" or "(PDF)" (primary button)

**Data Management:**
- Maximum 50 versions stored (auto-prune oldest)
- Each version ~5-10 KB (snapshot of current_plan)
- Storage warning if approaching localStorage limit

**Reference:** mockup-10-history-timeline-pane.svg, PRD FR-9.3

---

## 4. User Flows

### 4.1 First-Time User Complete Flow

**Flow Diagram:**
```
[Start] → [Registrer] → [Bekreft E-post] → [Logg Inn]
   ↓
[Oversikt: Se Budsjett/Frist/WBS]
   ↓
[Velg WBS-oppgave: 1.3.1 Grunnarbeid]
   ↓
[Velg Leverandør: Bjørn Eriksen] → [Chat Åpner]
   ↓
[Send Melding: "Trenger pristilbud"]
   ↓
[AI Svarer: "120 MNOK, 3 mnd"] ← [Venter 2-3 sek]
   ↓
[Forhandler: "For høyt, F-003..."] ← [Åpner Kravspec]
   ↓
[AI Innrømmer: "105 MNOK, 2.5 mnd"]
   ↓
[Godta Tilbud] → [Bekreft Modal] → [Bekreft]
   ↓
[Oversikt Oppdateres: 105/700 MNOK, 1.3.1 🟢]
   ↓
[Gjenta for 14 andre WBS-oppgaver...]
   ↓
[Krisepunkt: 500 MNOK brukt, 9 oppgaver igjen]
   ↓
[Reforhandle 1.3.1: "Trenger 100 MNOK"]
   ↓
[AI Aksepterer: "OK, 100 MNOK"]
   ↓
[Oversikt Oppdateres: 495/700 MNOK]
   ↓
[Fullfør alle 15 oppgaver]
   ↓
[Send Inn Plan] → [Validering Kjører...]
   ↓
  ┌─────────┴────────┐
  │                  │
[Feil]           [Suksess]
  │                  │
[Vis Feil]       [Vis Suksess Modal]
  │                  │
[Reforhandle]    [Eksporter → Last ned JSON]
  │
[Prøv Igjen]
```

**Key Decision Points:**
1. **After first AI response:** User decides to negotiate or accept
2. **After seeing high budget:** User realizes need to renegotiate earlier items
3. **Before submission:** User reviews final plan
4. **After validation failure:** User decides which items to renegotiate

---

### 4.2 Renegotiation Flow

**Flow Diagram:**
```
[Oversikt: Ser Fullført WBS 1.3.1 (105 MNOK)]
   ↓
[Klikk "Reforhandle"]
   ↓
[Bekreft Modal: "Dette vil fjerne fra plan"]
   ↓
[Bekreft] → [Plan Oppdateres: 1.3.1 → ⚪, Budsjett -105]
   ↓
[Chat Åpner med Historikk Bevart]
   ↓
[Send Melding: "Må reforhandle, budsjett strammere..."]
   ↓
[AI Svarer: "Forstår, kan godta 100 MNOK for 2.5 mnd"]
   ↓
[Godta Nytt Tilbud]
   ↓
[Oversikt: 1.3.1 → 🟢 igjen, Budsjett oppdatert]
```

---

### 4.3 Validation Failure Recovery Flow

**Flow Diagram:**
```
[Send Inn Plan (med 750 MNOK total)]
   ↓
[Validering Kjører... (spinner)]
   ↓
[Feil Modal: "Budsjett overskredet med 50 MNOK"]
[Forslag: "Reforhandle 2.1, 3.4"]
   ↓
[Klikk "Tilbake til Planlegging"]
   ↓
[Oversikt: Se hvilke oppgaver er dyrest]
   ↓
[Reforhandle 2.1: 250 MNOK → 230 MNOK]
   ↓
[Reforhandle 3.4: 180 MNOK → 165 MNOK]
   ↓
[Total nå: 695 MNOK]
   ↓
[Send Inn Plan igjen]
   ↓
[Suksess Modal: "Plan Godkjent!"]
```

---

## 5. Component Specifications

### 5.1 Button Component

**Variants:**

**Primary Button:**
```tsx
<button className="
  bg-blue-600 hover:bg-blue-700
  text-white font-semibold text-sm
  px-4 py-2 rounded
  transition-colors duration-200
  disabled:bg-gray-400 disabled:cursor-not-allowed
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
">
  Primary Action
</button>
```

**Secondary Button:**
```tsx
<button className="
  bg-white hover:bg-gray-50
  border border-gray-300
  text-gray-700 font-semibold text-sm
  px-4 py-2 rounded
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
">
  Secondary Action
</button>
```

**Danger Button:**
```tsx
<button className="
  bg-red-600 hover:bg-red-700
  text-white font-semibold text-sm
  px-4 py-2 rounded
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
">
  Destructive Action
</button>
```

**Loading State:**
```tsx
<button className="bg-blue-600 text-white px-4 py-2 rounded" disabled>
  <Loader className="animate-spin w-5 h-5 mr-2 inline" />
  Behandler...
</button>
```

---

### 5.2 Input Component

**Text Input:**
```tsx
<div className="mb-4">
  <label className="block text-sm font-medium text-gray-700 mb-1">
    E-post
  </label>
  <input
    type="email"
    className="
      w-full px-3 py-2
      border border-gray-300 rounded
      text-sm
      focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200
      placeholder:text-gray-400
    "
    placeholder="din.epost@eksempel.no"
  />
</div>
```

**Error State:**
```tsx
<div className="mb-4">
  <label className="block text-sm font-medium text-gray-700 mb-1">
    E-post
  </label>
  <input
    type="email"
    className="
      w-full px-3 py-2
      border-2 border-red-500 rounded
      text-sm
      focus:outline-none focus:ring-2 focus:ring-red-200
    "
  />
  <p className="text-red-600 text-xs mt-1">Ugyldig e-postadresse</p>
</div>
```

---

### 5.3 Progress Bar Component

**Budget Progress Bar:**
```tsx
<div className="mb-4">
  <div className="flex justify-between items-center mb-2">
    <span className="text-sm font-medium text-gray-700">Budsjett</span>
    <span className="text-sm font-semibold text-gray-900">
      450 / 700 MNOK (64%)
    </span>
  </div>

  <div className="w-full h-6 bg-gray-200 rounded-full overflow-hidden">
    <div
      className="h-full bg-green-500 transition-all duration-500"
      style={{ width: '64%' }}
    />
  </div>
</div>
```

**Color Logic:**
```tsx
const getProgressColor = (used: number, limit: number) => {
  const percentage = (used / limit) * 100;
  if (percentage > 100) return 'bg-red-500';
  if (percentage > 97) return 'bg-yellow-500';
  return 'bg-green-500';
};
```

---

### 5.4 WBS Item Component

**Pending State:**
```tsx
<div className="py-3 border-b border-gray-200">
  <div className="flex items-start">
    <Circle className="w-5 h-5 text-gray-400 mr-2 flex-shrink-0" />
    <div className="flex-1">
      <h4 className="text-sm font-medium text-gray-900">
        1.3.1 - Grunnarbeid
      </h4>
      <p className="text-xs text-gray-600 mt-1">
        Grunnlag: 100 MNOK, 2 måneder
      </p>
      <button className="mt-2 text-xs text-blue-600 hover:underline">
        Kontakt Leverandør
      </button>
    </div>
  </div>
</div>
```

**Completed State:**
```tsx
<div className="py-3 border-b border-gray-200">
  <div className="flex items-start">
    <CheckCircle className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
    <div className="flex-1">
      <h4 className="text-sm font-medium text-gray-900">
        1.3.1 - Grunnarbeid
      </h4>
      <div className="text-xs text-gray-600 mt-1 pl-0">
        <p>105 MNOK, 2.5 måneder</p>
        <p>Leverandør: Bjørn Eriksen</p>
        <p className="text-gray-500">Start: 15. jan 2025 | Slutt: 1. apr 2025</p>
      </div>
      <button className="mt-2 text-xs text-red-600 hover:underline">
        Reforhandle
      </button>
    </div>
  </div>
</div>
```

---

### 5.5 Chat Message Component

**User Message:**
```tsx
<div className="flex justify-end mb-3">
  <div className="
    max-w-2/3 bg-blue-600 text-white
    px-4 py-2 rounded-lg rounded-br-none
    text-sm
  ">
    Jeg trenger et pristilbud for Grunnarbeid. Kostnad og varighet?
  </div>
</div>
```

**AI Message with Offer:**
```tsx
<div className="flex justify-start mb-3">
  <div className="max-w-2/3">
    <div className="
      bg-white text-gray-900 shadow-sm
      px-4 py-2 rounded-lg rounded-bl-none
      text-sm
    ">
      Basert på nåværende markedspriser estimerer jeg 120 MNOK og 3 måneder
      for Grunnarbeid.
    </div>
    <button className="
      mt-2 bg-green-600 hover:bg-green-700 text-white
      text-xs px-3 py-1 rounded
    ">
      Godta: 120 MNOK, 3 måneder
    </button>
  </div>
</div>
```

**System Message:**
```tsx
<div className="flex justify-center mb-3">
  <div className="
    bg-gray-200 text-gray-700
    px-3 py-1 rounded text-xs italic
  ">
    ✅ Tilbud godtatt og forpliktet til plan
  </div>
</div>
```

---

## 6. Interaction Patterns

### 6.1 Real-Time Updates

**Budget Update on Commitment:**
```
User clicks "Godta" button
  → Button shows spinner ("Behandler...")
  → Modal appears (Bekreft Forpliktelse)
  → User clicks "Bekreft"
  → Modal closes with fade animation (200ms)
  → Dashboard budget bar updates with slide animation (500ms)
  → WBS item status changes ⚪ → 🟢 with fade (200ms)
  → Toast notification: "1.3.1 Grunnarbeid lagt til i plan"

Total time: ~1 second from click to visual confirmation
```

---

### 6.2 Loading States

**AI Response Loading:**
```
User sends message
  → Message appears immediately (optimistic UI)
  → Send button disabled, shows spinner
  → Chat shows typing indicator at bottom:
      [Gray bubble with animated dots: "Bjørn ser gjennom spesifikasjonene..."]
  → After 1-3 seconds, AI response appears
  → Typing indicator disappears
  → Chat auto-scrolls to new message
```

**Plan Submission Loading:**
```
User clicks "Send Inn Plan"
  → Button text changes to "Validerer..."
  → Button shows spinner icon
  → Semi-transparent overlay appears over dashboard (prevents interaction)
  → After <1 second, validation completes
  → Overlay fades out
  → Success or error modal appears with slide-up animation
```

---

### 6.3 Error Handling

**Network Error (AI API Timeout):**
```
User sends message
  → After 10 seconds with no response:
  → Error message appears in chat (system message):
      "❌ AI-tjenesten er midlertidig utilgjengelig. Prøv igjen."
  → "Prøv Igjen" button appears
  → User can click to retry
```

**Validation Error:**
```
User clicks "Send Inn Plan"
  → Validation fails
  → Error modal appears (slide up animation)
  → Modal lists specific errors with:
      - Red icon (XCircle)
      - Clear error message ("Budsjett overskredet med 50 MNOK")
      - Actionable suggestions ("Reforhandle 2.1, 3.4")
  → User clicks "Tilbake til Planlegging"
  → Modal closes
  → Dashboard highlights suggested items (subtle yellow background flash)
```

---

### 6.4 Toast Notifications

**Success Notifications:**
```
Trigger: Quote committed
Toast: Green background, white text, CheckCircle icon
Message: "1.3.1 Grunnarbeid lagt til i plan"
Position: Top-right corner
Duration: 3 seconds, auto-dismiss
```

**Warning Notifications:**
```
Trigger: Budget approaches limit (>680 MNOK)
Toast: Yellow background, dark text, AlertTriangle icon
Message: "⚠️ Budsjett på 97% - begrenset fleksibilitet"
Position: Top-right corner
Duration: 5 seconds, manual dismiss option
```

---

## 7. Responsive Design

### 7.1 Breakpoint Strategy

**Tailwind Breakpoints:**
```
sm:  640px   - Small tablets (portrait)
md:  768px   - Tablets (landscape)
lg:  1024px  - Desktop
xl:  1280px  - Large desktop
```

**Design Priorities:**
- **Primary:** Desktop (lg: 1024px+) - Most users will complete on laptop
- **Secondary:** Tablet landscape (md: 768px) - iPad horizontal
- **Tertiary:** Tablet portrait (sm: 640px) - iPad vertical
- **Not MVP:** Mobile (<640px) - Chat interface too complex for small screens

**Post-MVP Mobile Strategy:**
Full mobile support (<640px breakpoints) estimated 1-2 weeks effort. Requires chat UI redesign for small screens (vertical layout, collapsible supplier list, simplified WBS view).

---

### 7.2 Dashboard Responsive Layout

**Desktop (lg:):**
```
┌─Header─────────────────────────────────┐
├─Constraint Panel (full width)──────────┤
├─Quick Stats────────────────────────────┤
├─WBS List (2/3)───────┬─Actions (1/3)───┤
│                      │                 │
│                      │                 │
└──────────────────────┴─────────────────┘
```

**Tablet (md:):**
```
┌─Header─────────────────────────────────┐
├─Constraint Panel (full width)──────────┤
├─Quick Stats────────────────────────────┤
├─WBS List (full width)──────────────────┤
├─Actions (full width, sticky bottom)────┤
└────────────────────────────────────────┘
```

**Implementation:**
```tsx
<div className="grid lg:grid-cols-3 md:grid-cols-1 gap-6">
  <div className="lg:col-span-2">
    {/* WBS List */}
  </div>
  <div className="lg:col-span-1 md:sticky md:bottom-0 md:bg-white">
    {/* Action Buttons */}
  </div>
</div>
```

---

### 7.3 Chat Page Responsive Layout

**Desktop (lg:):**
```
┌─Header─────────────────────────────────┐
├─Chat Window (3/4)─────┬─Docs (1/4)─────┤
│                       │                │
│                       │                │
├─Message Input─────────┴────────────────┤
└────────────────────────────────────────┘
```

**Tablet (md:):**
```
┌─Header─────────────────────────────────┐
├─Chat Window (full width)───────────────┤
│                                        │
│ [Docs available via modal button]     │
├─Message Input──────────────────────────┤
└────────────────────────────────────────┘
```

**Implementation:**
```tsx
<div className="grid lg:grid-cols-4 md:grid-cols-1 gap-4">
  <div className="lg:col-span-3">
    {/* Chat Window */}
  </div>
  <div className="hidden lg:block">
    {/* Document Sidebar */}
  </div>
</div>

{/* Mobile: Floating button to open docs modal */}
<button className="lg:hidden fixed bottom-20 right-4 ...">
  📄 Dokumenter
</button>
```

---

## 8. Accessibility

### 8.1 Keyboard Navigation

**Tab Order:**
```
Login Page:
  Email input → Password input → Login button → Register link

Dashboard:
  Header links → WBS item 1 button → WBS item 2 button → ... → Send Inn Plan button

Chat Page:
  Back link → Message input → Send button → Accept Offer button (if visible)
```

**Keyboard Shortcuts:**
- `Tab`: Navigate forward
- `Shift + Tab`: Navigate backward
- `Enter`: Submit form / Activate button
- `Escape`: Close modal
- `Space`: Activate button (when focused)

**Focus Indicators:**
```css
.focus-visible:focus {
  outline: 2px solid #3B82F6; /* Blue outline */
  outline-offset: 2px;
}
```

---

### 8.2 Screen Reader Support

**ARIA Labels:**
```tsx
{/* Button without visible text */}
<button aria-label="Lukk modal">
  <X className="w-5 h-5" />
</button>

{/* Progress bar */}
<div
  role="progressbar"
  aria-valuenow={64}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Budsjettbruk: 450 av 700 MNOK"
>
  {/* Visual progress bar */}
</div>

{/* Form input */}
<label htmlFor="email" className="...">E-post</label>
<input
  id="email"
  type="email"
  aria-describedby="email-error"
  aria-invalid={hasError}
/>
{hasError && (
  <p id="email-error" role="alert">Ugyldig e-postadresse</p>
)}
```

**Live Regions:**
```tsx
{/* Budget updates announced */}
<div aria-live="polite" aria-atomic="true" className="sr-only">
  Budsjett oppdatert til 450 av 700 MNOK
</div>

{/* Errors announced */}
<div aria-live="assertive" aria-atomic="true" className="sr-only">
  Feil: Planvalidering mislyktes
</div>
```

---

### 8.3 Color Contrast

**WCAG 2.1 Level AA Compliance:**
- **Normal text (16px):** 4.5:1 contrast minimum
- **Large text (24px+):** 3:1 contrast minimum
- **UI components:** 3:1 contrast minimum

**Contrast Checks:**
```
Gray 900 (#111827) on White (#FFFFFF):
  Contrast: 16.9:1 ✅ (Exceeds AAA)

Blue 600 (#3B82F6) on White:
  Contrast: 4.6:1 ✅ (Meets AA)

White on Blue 600:
  Contrast: 4.6:1 ✅ (Meets AA for large text)

Gray 600 (#4B5563) on White:
  Contrast: 7.3:1 ✅ (Meets AAA)
```

---

## 9. Implementation Notes

### 9.1 Tech Stack Recommendations

**Framework:**
- Next.js 14+ (App Router)
- React 18+
- TypeScript

**Styling:**
- Tailwind CSS 3+
- Shadcn UI (for complex components: modals, dropdowns)

**State Management:**
- React Context for UI state (modal open/close)
- localStorage for session data (direct read/write)

**Utilities:**
- `clsx` or `classnames` for conditional classes
- `date-fns` for date formatting
- Lucide React for icons

---

### 9.2 Component Library (Shadcn)

**Recommended Shadcn Components:**
- `Dialog` - For modals (confirmation, error, success)
- `DropdownMenu` - For user menu
- `Textarea` - For chat input
- `Progress` - For budget progress bar
- `ScrollArea` - For chat window, WBS list
- `Toast` - For notifications

**Installation:**
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add dialog dropdown-menu textarea progress scroll-area toast
```

---

### 9.3 Animation Guidelines

**Transitions:**
```css
/* Button hover */
transition: background-color 200ms ease-in-out;

/* Budget bar update */
transition: width 500ms ease-in-out;

/* Modal appear/disappear */
transition: opacity 200ms, transform 200ms;
```

**Animations:**
- **Modal Enter:** Fade in + slide up (200ms)
- **Modal Exit:** Fade out + slide down (150ms)
- **Toast Enter:** Slide in from right (300ms)
- **Toast Exit:** Fade out (200ms)
- **Loading Spinner:** Continuous rotation (linear, 1s)

**Accessibility:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

### 9.4 Norwegian Language Strings

**Common UI Text:**
```typescript
const nb_NO = {
  // Authentication
  "auth.login": "Logg Inn",
  "auth.register": "Registrer deg",
  "auth.email": "E-post",
  "auth.password": "Passord",
  "auth.logout": "Logg Ut",

  // Dashboard
  "dashboard.budget": "Budsjett",
  "dashboard.deadline": "Frist",
  "dashboard.projected": "Forventet",
  "dashboard.submitPlan": "Send Inn Plan",
  "dashboard.export": "Eksporter Økt",
  "dashboard.help": "Hjelp",

  // WBS
  "wbs.contactSupplier": "Kontakt Leverandør",
  "wbs.renegotiate": "Reforhandle",
  "wbs.completed": "Fullført",
  "wbs.pending": "Venter",

  // Chat
  "chat.sendMessage": "Send",
  "chat.typing": "skriver...",
  "chat.acceptOffer": "Godta",

  // Validation
  "validation.budgetExceeded": "Budsjett overskredet",
  "validation.timelineExceeded": "Prosjektet forsinket",
  "validation.success": "Plan Godkjent!",

  // Errors
  "error.networkError": "Nettverksfeil. Prøv igjen.",
  "error.aiUnavailable": "AI-tjenesten er midlertidig utilgjengelig.",
};
```

---

### 9.5 Development Checklist

**Before Starting Implementation:**
- [ ] Review complete UX spec with team
- [ ] Set up Tailwind + Shadcn
- [ ] Create base components (Button, Input, Modal)
- [ ] Set up TypeScript interfaces matching localStorage schema
- [ ] Prepare static data files (wbs.json, suppliers.json)

**During Implementation:**
- [ ] Build pages in order: Login → Dashboard → Chat
- [ ] Test responsive layouts at each breakpoint
- [ ] Implement keyboard navigation
- [ ] Add ARIA labels and roles
- [ ] Test with screen reader (NVDA or VoiceOver)
- [ ] Verify color contrast with tool (WebAIM Contrast Checker)

**Before Launch:**
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Lighthouse audit (Performance, Accessibility, Best Practices)
- [ ] User acceptance testing with 5-10 students
- [ ] Fix critical issues identified in testing

---

## Appendices

### Appendix A: Color Palette Reference

**Full Palette (Tailwind CSS Variables):**
```css
:root {
  /* Primary */
  --blue-50: #EFF6FF;
  --blue-600: #3B82F6;
  --blue-700: #2563EB;

  /* Success */
  --green-50: #ECFDF5;
  --green-500: #10B981;
  --green-600: #059669;

  /* Warning */
  --yellow-50: #FFFBEB;
  --yellow-500: #F59E0B;
  --yellow-600: #D97706;

  /* Error */
  --red-50: #FEF2F2;
  --red-500: #EF4444;
  --red-600: #DC2626;

  /* Neutral */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-400: #9CA3AF;
  --gray-500: #6B7280;
  --gray-600: #4B5563;
  --gray-700: #374151;
  --gray-800: #1F2937;
  --gray-900: #111827;
}
```

---

### Appendix B: Component Export Checklist

**Reusable Components to Build:**
- [ ] Button (Primary, Secondary, Danger variants)
- [ ] Input (Text, Email, Password, Textarea)
- [ ] Modal (Confirmation, Error, Success)
- [ ] ProgressBar (Budget meter)
- [ ] WBSItem (Pending, Completed states)
- [ ] ChatMessage (User, AI, System)
- [ ] Toast (Success, Warning, Error)
- [ ] LoadingSpinner
- [ ] Header (with user menu)
- [ ] DocumentLink (with icon)

---

### Appendix C: Figma/Design Tool Integration (Optional)

**If using Figma:**
1. Export color palette as Figma styles
2. Export typography scale as text styles
3. Create component library matching this spec
4. Share Figma file with developers for exact measurements

**Figma Plugins:**
- **Tailwind CSS Color Generator:** Auto-generate Tailwind classes from Figma colors
- **Accessibility Checker:** Verify contrast ratios
- **Auto Layout:** Create responsive components

---

### Appendix D: Component Development Time Estimates

This appendix provides development time estimates for implementing the components specified in this document. Estimates assume a developer familiar with React, TypeScript, and Tailwind CSS.

#### D.1 Core Components (Section 5)

| Component | Complexity | Estimated Time | Notes |
|-----------|-----------|----------------|-------|
| **Button** | Low | 1-2 hours | Variants (primary, secondary, ghost), states (hover, disabled, loading) |
| **ProgressBar** | Low | 2-3 hours | Dynamic width calculation, color thresholds (green/yellow/red), percentage label |
| **SupplierCard** | Medium | 3-4 hours | Conditional styling (online/offline), modal trigger, responsive layout |
| **WBSListItem** | Medium | 4-5 hours | Expandable details, status icons, conditional rendering (empty/filled states) |
| **ChatInterface** | High | 6-8 hours | Message history, auto-scroll, typing indicator, supplier avatar, responsive height |

**Subtotal:** 16-22 hours

#### D.2 Page Layouts (Section 3)

| Page | Complexity | Estimated Time | Notes |
|------|-----------|----------------|-------|
| **Login Page** | Low | 2-3 hours | Form validation, error handling, Supabase Auth integration |
| **Dashboard** | High | 8-10 hours | Multi-section layout, real-time budget/deadline calculation, WBS list integration, action buttons |
| **Chat Page** | High | 6-8 hours | Supplier selection, chat interface integration, back navigation, responsive grid |
| **Success Modal** | Low | 1-2 hours | Centered modal, export button, visual feedback (confetti optional) |
| **Validation Error Modal** | Medium | 2-3 hours | Conditional content (budget/deadline violations), WBS item list, dynamic error messages |

**Subtotal:** 19-26 hours

#### D.3 Interaction Patterns (Section 6)

| Pattern | Estimated Time | Notes |
|---------|----------------|-------|
| **Modal System (Base)** | 3-4 hours | Reusable modal wrapper, overlay, close handlers, focus trap |
| **Form Validation** | 2-3 hours | Email validation, password strength, error display patterns |
| **Real-time Updates** | 4-5 hours | Budget/deadline recalculation on plan changes, localStorage sync |
| **Loading States** | 2-3 hours | Skeleton screens, spinner components, button loading states |

**Subtotal:** 11-15 hours

#### D.4 Responsive Design (Section 7)

| Task | Estimated Time | Notes |
|------|----------------|-------|
| **Desktop Layout (lg:)** | Included in page estimates | Primary target |
| **Tablet Landscape (md:)** | 3-4 hours | Grid adjustments, sticky action buttons |
| **Tablet Portrait (sm:)** | 2-3 hours | Single-column layouts, font size adjustments |
| **Responsive Testing** | 2-3 hours | Cross-device testing, breakpoint validation |

**Subtotal:** 7-10 hours

#### D.5 Accessibility (Section 8)

| Task | Estimated Time | Notes |
|------|----------------|-------|
| **ARIA Labels** | 3-4 hours | Add aria-label, aria-describedby to all interactive elements |
| **Keyboard Navigation** | 4-5 hours | Focus indicators, tab order, keyboard shortcuts (ESC for modals) |
| **Contrast Validation** | 1-2 hours | Verify all text/background combinations meet WCAG 2.1 Level A |
| **Screen Reader Testing** | 2-3 hours | Manual testing with NVDA/VoiceOver, adjust as needed |

**Subtotal:** 10-14 hours

#### D.6 Total Estimates

| Category | Time Range |
|----------|-----------|
| Core Components | 16-22 hours |
| Page Layouts | 19-26 hours |
| Interaction Patterns | 11-15 hours |
| Responsive Design | 7-10 hours |
| Accessibility | 10-14 hours |
| **Total** | **63-87 hours** |

**Recommended Sprint Allocation:**
- **Week 2 (UI Foundation):** 20-24 hours (Login, Dashboard shell, Core components)
- **Week 3 (AI Integration):** 24-30 hours (Chat interface, WBS interaction, Modal system)
- **Week 4 (Polish):** 19-33 hours (Responsive, Accessibility, Testing, Bug fixes)

**Note:** These estimates exclude backend integration time (API calls, authentication, localStorage logic), which is covered in the Epic story point estimates in `epics.md`. Estimates assume working in 4-hour focused blocks per day (half-day sprints).

---

**End of UX Design Specification**

*This document should be reviewed by frontend developers and product owner before implementation begins. Any deviations from this spec should be documented and approved.*

**Next Steps:**
1. UX Design Validation (stakeholder review)
2. Begin frontend implementation (Week 2)
3. Component library setup (Tailwind + Shadcn)
