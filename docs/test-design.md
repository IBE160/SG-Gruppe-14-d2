# Test Design and Strategy
## Nye Hædda Barneskole - Project Management Simulation

**Document Version:** 1.1
**Date:** 2025-12-08
**Status:** Updated with Visualization Test Cases
**Test Analyst:** QA Team
**Changelog:** Added section 3.9 with 28 test cases for Epic 10 (Visualization & Analysis)

---

## Document Purpose

This test design defines the comprehensive testing strategy, test cases, and quality assurance processes for the Nye Hædda Barneskole simulation. It ensures all functional requirements, non-functional requirements, and user acceptance criteria are validated before launch.

**Audience:**
- QA Engineers (test execution)
- Developers (test-driven development)
- Product Owner (acceptance criteria validation)

---

## Table of Contents

1. [Test Strategy](#1-test-strategy)
2. [Test Levels](#2-test-levels)
3. [Functional Test Cases](#3-functional-test-cases)
4. [Non-Functional Test Cases](#4-non-functional-test-cases)
5. [AI Quality Testing](#5-ai-quality-testing)
6. [User Acceptance Testing](#6-user-acceptance-testing)
7. [Test Automation](#7-test-automation)
8. [Test Environment](#8-test-environment)
9. [Test Data](#9-test-data)
10. [Defect Management](#10-defect-management)
11. [Test Schedule](#11-test-schedule)

---

## 1. Test Strategy

### 1.1 Testing Objectives

**Primary Objectives:**
1. Verify all 15 Must-Have features work as specified in PRD
2. Validate AI negotiation realism (80% user satisfaction target)
3. Ensure performance meets NFRs (<2 sec response time)
4. Confirm Norwegian language accuracy and cultural appropriateness
5. Validate learning objectives (budget awareness, negotiation skills)

**Success Criteria:**
- 100% of Must-Have features pass acceptance tests
- 0 critical bugs in production
- <5 minor bugs in production
- 80%+ user satisfaction in pilot testing
- 85%+ session completion rate

---

### 1.2 Test Approach

**Test Pyramid:**
```
           /\
          /  \    E2E Tests (10%)
         /____\   - Critical user flows
        /      \  - AI negotiation scenarios
       /________\
      /          \ Integration Tests (30%)
     /            \ - API endpoints
    /______________\ - localStorage operations
   /                \
  /                  \ Unit Tests (60%)
 /                    \ - React components
/______________________\ - Business logic
                        - Validation functions
```

**Testing Types:**
- **Unit Testing:** 60% coverage—React components, utility functions
- **Integration Testing:** 30%—API calls, localStorage, Supabase auth
- **End-to-End Testing:** 10%—Critical user flows (login → negotiate → submit)
- **Manual Testing:** AI quality, UX/UI, Norwegian language
- **User Acceptance Testing (UAT):** 5-10 students, real-world usage

---

### 1.3 Test Tools

| Test Type | Tool | Justification |
|-----------|------|---------------|
| **Unit Tests** | Vitest + React Testing Library | Fast, TypeScript support, Vite integration |
| **E2E Tests** | Playwright | Cross-browser, reliable, video recording |
| **API Tests** | Pytest (FastAPI) | Native FastAPI test client |
| **Performance** | Lighthouse | Web vitals, accessibility, performance |
| **AI Testing** | Manual + Gemini API logs | Realistic user scenarios |
| **Bug Tracking** | GitHub Issues | Integrated with repo, free |

---

## 2. Test Levels

### 2.1 Unit Testing

**Scope:** Individual React components, utility functions, validation logic

**Coverage Target:** 60% code coverage minimum

**Components to Test:**
- Button (all variants, disabled state, loading state)
- Input (validation, error state)
- ProgressBar (color logic based on percentage)
- WBSItem (pending/completed states)
- ChatMessage (user/AI/system variants)

**Utility Functions to Test:**
- `calculateTotalCost(current_plan)` → returns sum of all costs
- `calculateProjectedEndDate(current_plan, wbs_items)` → critical path
- `validatePlan(current_plan, constraints)` → budget/timeline checks
- `parseAIOffer(message)` → extract cost and duration from text
- `resolveDependencies(wbs_code, current_plan, wbs_items)` → start_date calculation

**Example Unit Test (Vitest):**
```typescript
import { describe, it, expect } from 'vitest';
import { calculateTotalCost } from './planUtils';

describe('calculateTotalCost', () => {
  it('should return 0 for empty plan', () => {
    expect(calculateTotalCost({})).toBe(0);
  });

  it('should sum all costs correctly', () => {
    const plan = {
      '1.3.1': { cost: 105, duration: 2.5 },
      '2.1': { cost: 230, duration: 4 }
    };
    expect(calculateTotalCost(plan)).toBe(335);
  });

  it('should handle decimal costs', () => {
    const plan = {
      '1.3.1': { cost: 105.5, duration: 2.5 }
    };
    expect(calculateTotalCost(plan)).toBe(105.5);
  });
});
```

---

### 2.2 Integration Testing

**Scope:** Component interactions, API calls, localStorage operations

**Coverage Target:** 30% (focus on critical paths)

**Scenarios to Test:**
- Auth flow: Register → JWT stored → Dashboard loads session
- Chat flow: Send message → API call → AI response → localStorage updated
- Commit flow: Accept offer → localStorage updated → Dashboard refreshed
- Renegotiation flow: Remove item → plan updated → dependencies recalculated

**Example Integration Test (React Testing Library):**
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Dashboard from './Dashboard';

describe('Dashboard Integration', () => {
  it('should update budget when quote committed', async () => {
    // Mock localStorage
    const mockSession = {
      current_plan: {},
      metrics: { budget_used: 0 }
    };
    vi.spyOn(Storage.prototype, 'getItem').mockReturnValue(JSON.stringify(mockSession));

    render(<Dashboard />);

    // Initial budget should be 0 / 700
    expect(screen.getByText(/0 \/ 700 MNOK/)).toBeInTheDocument();

    // Simulate quote commitment (trigger via event or component method)
    // ... (test implementation)

    // Budget should update to 105 / 700
    await waitFor(() => {
      expect(screen.getByText(/105 \/ 700 MNOK/)).toBeInTheDocument();
    });
  });
});
```

---

### 2.3 End-to-End Testing

**Scope:** Complete user flows from login to export

**Coverage Target:** 10% (critical happy paths + edge cases)

**Critical Flows:**
1. **Happy Path:** Register → Login → Negotiate 15 WBS items → Submit plan → Pass validation → Export
2. **Renegotiation Path:** Commit item → Realize budget tight → Renegotiate → Lower cost → Submit → Pass
3. **Failure Path:** Commit all items → Over budget → Validation fails → See error → Renegotiate → Pass

**Example E2E Test (Playwright):**
```typescript
import { test, expect } from '@playwright/test';

test('complete game flow - happy path', async ({ page }) => {
  // 1. Register
  await page.goto('/');
  await page.click('text=Registrer deg');
  await page.fill('input[type="email"]', 'test@example.com');
  await page.fill('input[type="password"]', 'testpassword123');
  await page.click('button:has-text("Registrer")');

  // 2. Dashboard loads
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('text=Budsjett: 0 / 700 MNOK')).toBeVisible();

  // 3. Negotiate first WBS item
  await page.click('text=1.3.1 - Grunnarbeid');
  await page.click('text=Bjørn Eriksen');
  await page.fill('textarea', 'Jeg trenger et pristilbud for Grunnarbeid');
  await page.click('button:has-text("Send")');

  // 4. AI responds (wait for response)
  await expect(page.locator('text=estimerer jeg')).toBeVisible({ timeout: 5000 });

  // 5. Accept offer
  await page.click('button:has-text("Godta")');
  await page.click('button:has-text("Bekreft")');

  // 6. Dashboard updated
  await expect(page.locator('text=105 / 700 MNOK')).toBeVisible();

  // ... (repeat for all 15 WBS items)

  // 15. Submit plan
  await page.click('button:has-text("Send Inn Plan")');

  // 16. Success modal
  await expect(page.locator('text=🎉 Plan Godkjent!')).toBeVisible();

  // 17. Export
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.click('button:has-text("Eksporter Økt")')
  ]);
  expect(download.suggestedFilename()).toContain('nye_haedda_session');
});
```

---

## 3. Functional Test Cases

### 3.1 Epic 1: User Authentication

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E1-001** | User registration with valid email | 1. Go to Login page<br>2. Click "Registrer deg"<br>3. Enter email: test@example.com<br>4. Enter password: password123<br>5. Click "Registrer" | User account created, JWT stored in localStorage, redirected to Dashboard | High |
| **TC-E1-002** | User registration with existing email | 1-4. Same as TC-E1-001<br>5. Use email that already exists | Error message: "E-postadressen er allerede registrert" | High |
| **TC-E1-003** | User login with valid credentials | 1. Go to Login page<br>2. Enter email: test@example.com<br>3. Enter password: password123<br>4. Click "Logg Inn" | JWT stored, redirected to Dashboard | High |
| **TC-E1-004** | User login with invalid credentials | 1-3. Same as TC-E1-003<br>4. Use wrong password | Error message: "Feil e-post eller passord" | High |
| **TC-E1-005** | Session initialization on login | 1. Login with valid credentials<br>2. Dashboard loads | If no session → new session created with 15 WBS items, 0 budget. If session exists → loaded from localStorage | High |

---

### 3.2 Epic 2: Project Dashboard & Constraints

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E2-001** | Display initial budget | 1. Login<br>2. View Dashboard | Budget shows: "0 / 700 MNOK (0%)", Progress bar empty (gray background) | High |
| **TC-E2-002** | Budget updates after commitment | 1. Commit WBS item with 105 MNOK cost | Budget shows: "105 / 700 MNOK (15%)", Progress bar green, animated slide to 15% | High |
| **TC-E2-003** | Budget warning at 97% | 1. Commit items totaling 680 MNOK | Progress bar turns yellow, Warning toast: "⚠️ Budsjett på 97%..." | Medium |
| **TC-E2-004** | Budget error at >100% | 1. Commit items totaling 720 MNOK | Progress bar turns red, shows "720 / 700 MNOK (103%)" | High |
| **TC-E2-005** | Projected end date calculation | 1. Commit 3 WBS items with dependencies | Projected end date = latest end_date from committed items. Show green ✓ if < May 15, red ✗ if > May 15 | High |
| **TC-E2-006** | Quick stats update | 1. Commit 5 WBS items | Stats show: "5 / 15 WBS-oppgaver fullført \| [X] forhandlinger" | Low |

---

### 3.3 Epic 3: WBS Management

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E3-001** | Load WBS list | 1. Login<br>2. View Dashboard | 15 WBS items displayed, all with ⚪ pending icon | High |
| **TC-E3-002** | WBS item selection | 1. Click "Kontakt Leverandør" on 1.3.1 | Navigate to supplier selection page, WBS details shown | High |
| **TC-E3-003** | View WBS requirements | 1. Select WBS item<br>2. View requirements section | Requirements (F-codes, K-codes) displayed, dependencies listed | Medium |
| **TC-E3-004** | WBS status update after commitment | 1. Commit quote for WBS 1.3.1 | Icon changes ⚪ → 🟢, Shows "105 MNOK, 2.5 måneder \| Bjørn Eriksen" | High |
| **TC-E3-005** | Dependency prevention | 1. Try to commit WBS 2.1 (depends on 1.3.1)<br>2. 1.3.1 not yet committed | Error modal: "Kan ikke forplikte 2.1 Råbygg før 1.3.1 Grunnarbeid er fullført" | High |

---

### 3.4 Epic 4: AI Supplier Negotiation

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E4-001** | Send message to AI | 1. Open chat with Bjørn Eriksen<br>2. Type: "Trenger pristilbud"<br>3. Click "Send" | Message appears in chat (blue bubble, right-aligned), Sent to backend, Loading indicator shows | High |
| **TC-E4-002** | AI response received | 1. After sending message<br>2. Wait for AI | AI response appears (white bubble, left-aligned) within 1-3 seconds, Contains cost and duration estimate | Critical |
| **TC-E4-003** | AI offer detection | 1. AI responds: "120 MNOK og 3 måneder" | "Godta" button appears below message: "Godta: 120 MNOK, 3 måneder" | High |
| **TC-E4-004** | AI negotiation (multiple rounds) | 1. AI offers 120 MNOK<br>2. User: "For høyt, kan du gå ned?"<br>3. AI offers 110 MNOK | AI reduces price (concession_rate applied), New "Godta" button with 110 MNOK | Critical |
| **TC-E4-005** | AI walks away after patience exhausted | 1. AI offers 120 MNOK<br>2. User demands 50 MNOK (unreasonable)<br>3. Repeat 3 times | AI refuses: "Jeg kan dessverre ikke gå lavere enn 100 MNOK. Dette er mitt siste tilbud." | High |
| **TC-E4-006** | Chat history persistence | 1. Negotiate with Bjørn<br>2. Close chat<br>3. Reopen chat | All previous messages visible, AI has context of negotiation | Medium |
| **TC-E4-007** | Document sidebar access | 1. In chat, click "📄 WBS" | WBS modal opens with item details (or new tab) | Low |

---

### 3.5 Epic 5: Plan Management & Commitment

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E5-001** | Commit quote to plan | 1. Click "Godta: 105 MNOK, 2.5 mnd" | Confirmation modal appears with WBS, supplier, cost, duration | High |
| **TC-E5-002** | Confirm commitment | 1. In modal, click "Bekreft" | Modal closes, System message in chat: "✅ Tilbud godtatt...", Dashboard updated, Toast notification | High |
| **TC-E5-003** | Renegotiation (remove item) | 1. Click "Reforhandle" on completed WBS 1.3.1 | Confirmation modal: "Dette vil fjerne..." | High |
| **TC-E5-004** | Confirm renegotiation | 1. In modal, click "Bekreft" | Item removed from plan, Status ⚪, Budget reduced by 105 MNOK, Chat reopens with history | High |
| **TC-E5-005** | Plan history tracking | 1. Commit 3 items<br>2. Renegotiate 1 item | plan_history has 4 entries: 3 commits, 1 remove | Low |
| **TC-E5-006** | Visual feedback on commitment | 1. Click "Bekreft" in commitment modal | Button shows spinner (200ms), Modal fades out (200ms), Budget bar animates (500ms), WBS icon changes, Toast appears | Medium |

---

### 3.6 Epic 6: Plan Validation & Submission

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E6-001** | Submit incomplete plan | 1. Commit only 10/15 WBS items<br>2. Click "Send Inn Plan" | Button disabled (gray, not clickable) | High |
| **TC-E6-002** | Submit complete plan (within budget) | 1. Commit all 15 items, total 680 MNOK<br>2. Click "Send Inn Plan" | Loading overlay: "Validerer...", Success modal appears after <1 sec | Critical |
| **TC-E6-003** | Validation success modal | 1. After validation passes | Modal shows: "🎉 Plan Godkjent!", Stats (cost, date, time, negotiations), Buttons: "Eksporter Økt", "Start Nytt Spill" | High |
| **TC-E6-004** | Submit plan over budget | 1. Commit all 15 items, total 750 MNOK<br>2. Submit | Error modal: "❌ Planvalidering Mislyktes", Shows "Budsjett overskredet med 50 MNOK", Suggests 3 expensive items to renegotiate | Critical |
| **TC-E6-005** | Submit plan over timeline | 1. Commit items totaling 698 MNOK but projected date May 20, 2026<br>2. Submit | Error modal: "Prosjektet forsinket til 20. mai 2026 (Frist: 15. mai)" | High |
| **TC-E6-006** | Validation with 3% budget tolerance | 1. Commit items totaling 715 MNOK (102% of 700)<br>2. Submit | ⚠️ Depending on PRD decision: Pass with warning OR Fail. (Clarify in PRD FR-7.4) | Medium |

---

### 3.7 Epic 7: Session Export & Data Management

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E7-001** | Export session after success | 1. Pass validation<br>2. Click "Eksporter Økt" in success modal | JSON file downloads: `nye_haedda_session_[timestamp].json`, Contains full GameSession object | High |
| **TC-E7-002** | Export session mid-game | 1. Commit 5/15 items<br>2. Click "Eksporter Økt" in sidebar | JSON file downloads with current state (5 items in current_plan) | Medium |
| **TC-E7-003** | Start new game | 1. In success modal, click "Start Nytt Spill" | Confirmation: "Dette vil slette nåværende økt. Er du sikker?" | High |
| **TC-E7-004** | Confirm new game | 1. Click "Ja" in confirmation | localStorage cleared, Dashboard reloads with new session (0/15 items, 0 budget) | High |
| **TC-E7-005** | Storage quota warning | 1. Manually fill localStorage to 85% capacity<br>2. Reload app | Warning toast: "⚠️ Lagring 80% full..." | Low |

---

### 3.8 Epic 8: Help & Documentation

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E8-001** | Open help documentation | 1. Click "Hjelp" button in Dashboard | Help modal opens with Norwegian instructions (how to play, tips, FAQ) | Medium |
| **TC-E8-002** | Close help modal | 1. Open help<br>2. Click X or outside modal | Modal closes, Dashboard still visible | Low |

---

### 3.9 Epic 10: Visualization & Analysis

| Test ID | Test Case | Steps | Expected Result | Priority |
|---------|-----------|-------|-----------------|----------|
| **TC-E10-001** | Navigate to Gantt chart | 1. Login<br>2. Click "📈 Gantt-diagram" tab | Navigate to Gantt view, timeline header shows Jan 2025 - Mai 2026, "Idag" marker visible | High |
| **TC-E10-002** | Display task bars in Gantt | 1. Commit 3 WBS items (2 completed, 1 in-progress 45%)<br>2. View Gantt | Completed: Green bars, In-progress: Yellow bar with "45%" label, Planned: Gray outline bars | Critical |
| **TC-E10-003** | Critical path visualization Gantt | 1. Commit items forming critical path<br>2. View Gantt | Critical path tasks have red 3px border, Dependency arrows red dashed | High |
| **TC-E10-004** | Gantt zoom controls | 1. In Gantt view, adjust zoom slider to 150% | Timeline scales to 150%, task bars proportionally larger, scroll enabled | Medium |
| **TC-E10-005** | Gantt view mode switcher | 1. In Gantt view, select "Uke" from dropdown | Timeline header changes to weekly view (Uke 1, 2, 3...) | Medium |
| **TC-E10-006** | Gantt filter (critical path) | 1. Check "Vis kritisk sti" checkbox<br>2. Uncheck "Vis fullførte" | Only critical path tasks shown, completed tasks hidden | Low |
| **TC-E10-007** | Gantt real-time update | 1. Open Gantt view<br>2. Navigate to Dashboard<br>3. Commit new WBS item<br>4. Return to Gantt | New task bar appears with smooth animation (300ms), Critical path recalculated | Critical |
| **TC-E10-008** | Export Gantt as PNG | 1. In Gantt view, click "Eksporter Gantt (PNG)" | PNG image downloads showing current timeline state | Medium |
| **TC-E10-009** | Navigate to Precedence diagram | 1. Click "🔀 Presedensdiagram" tab | Navigate to Precedence view, network diagram visible with START/END nodes | High |
| **TC-E10-010** | Display nodes in Precedence | 1. Commit 5 WBS items<br>2. View Precedence | Nodes show: WBS code, name, duration, cost, status color, Arrows connect dependencies | Critical |
| **TC-E10-011** | Critical path in Precedence | 1. View Precedence with critical path<br>2. Check info panel | Critical path nodes have red 3px border, Info panel shows: "Kritisk Sti: 1.1 → 1.3.1 → 2.1...", Total duration | High |
| **TC-E10-012** | Precedence node interaction | 1. Hover on node 1.3.1 | Incoming/outgoing arrows highlighted blue-400 | Medium |
| **TC-E10-013** | Precedence node click details | 1. Click on node 2.1 | Popup modal shows full WBS details: requirements, supplier, dates | Medium |
| **TC-E10-014** | Precedence layout modes | 1. Select "Topp→Bunn" from layout dropdown | Network re-renders with top-to-bottom layout (500ms animation) | Low |
| **TC-E10-015** | Precedence pan/zoom | 1. Drag canvas<br>2. Scroll to zoom | Canvas pans, Zoom in/out (50%-200%) | Medium |
| **TC-E10-016** | Export Precedence as PNG | 1. Click "Eksporter Diagram (PNG)" | PNG downloads showing current network state | Medium |
| **TC-E10-017** | Open History/Timeline panel | 1. Click "🕒 Historikk" button (top-right) | Full-screen overlay panel slides in from right (300ms), Event timeline visible on left | High |
| **TC-E10-018** | Display event timeline | 1. After 10 commits/renegotiations<br>2. Open History | Left sidebar shows 10 events (newest first), Each with icon, description, timestamp | High |
| **TC-E10-019** | Filter history events | 1. In History, select "Forhandlinger" from filter dropdown | Only negotiation events shown, Commit/remove events hidden | Low |
| **TC-E10-020** | Compare versions (before/after) | 1. Select event "Versjon 7 - Forpliktet 2.1"<br>2. View comparison panel | Right panel shows: "Før (Versjon 6)" vs "Etter (Versjon 7)", Side-by-side Gantt comparison, Change summary stats | Critical |
| **TC-E10-021** | Cascade effects display | 1. View comparison after committing WBS 2.1 | Cascade effects panel lists up to 5 impacts: "WBS 2.2 start flyttet 5 dager tidligere", "Kritisk sti opprettholdt" | Medium |
| **TC-E10-022** | Navigate history versions | 1. Click "← Forrige versjon" | Comparison updates to show Versjon 5 vs Versjon 6 | Medium |
| **TC-E10-023** | Compare with current | 1. Select old version 3<br>2. Click "Sammenlign med nåværende" | Comparison shows: "Før (Versjon 3)" vs "Etter (Versjon 10 - Nåværende)" | Medium |
| **TC-E10-024** | Export history as JSON | 1. Click "Eksporter historikk (JSON)" | JSON file downloads: `nye_haedda_history_[timestamp].json`, Contains version_history array | Low |
| **TC-E10-025** | Close History panel | 1. Click "✕ Lukk historikk" or click backdrop | Panel slides out to right (300ms), Dashboard/current view visible | Medium |
| **TC-E10-026** | History storage limit (50 versions) | 1. Manually create 55 versions<br>2. Check version_history in localStorage | Only last 50 versions stored, Oldest 5 versions pruned | Low |
| **TC-E10-027** | Navigation state persistence | 1. Navigate to Gantt<br>2. Refresh page | Returns to Gantt view (not Dashboard), Active tab highlighted | Medium |
| **TC-E10-028** | Real-time sync across views | 1. Open Gantt view<br>2. In another tab, commit WBS item on Dashboard<br>3. Return to Gantt tab | Gantt automatically updates (localStorage listener), New task bar appears | High |

---

## 4. Non-Functional Test Cases

### 4.1 Performance Testing

| Test ID | Test Case | Target | Measurement Method | Priority |
|---------|-----------|--------|-------------------|----------|
| **TC-NFR-001** | Page load time (Dashboard) | <2 seconds | Lighthouse, Chrome DevTools | High |
| **TC-NFR-002** | AI response time | 1-3 seconds | Backend logs, Gemini API latency | Critical |
| **TC-NFR-003** | Budget update animation | 500ms | Browser performance timeline | Medium |
| **TC-NFR-004** | localStorage read/write | <100ms | Console.time() benchmarks | Low |
| **TC-NFR-005** | Chat message rendering (100 messages) | <1 second | React Profiler | Medium |

**Performance Test Script (Lighthouse CI):**
```bash
# Run Lighthouse on deployed app
npx lighthouse https://nye-haedda.vercel.app --output=json --output-path=./lighthouse-report.json

# Check thresholds
# Performance: >90
# Accessibility: >95
# Best Practices: >90
```

---

### 4.2 Accessibility Testing

| Test ID | Test Case | WCAG Level | Testing Method | Priority |
|---------|-----------|-----------|----------------|----------|
| **TC-ACC-001** | Keyboard navigation (Tab order) | A (2.1.1) | Manual keyboard-only navigation | High |
| **TC-ACC-002** | Screen reader support | A (4.1.2) | NVDA/VoiceOver testing | High |
| **TC-ACC-003** | Color contrast (text) | AA (1.4.3) | WebAIM Contrast Checker | High |
| **TC-ACC-004** | Focus visible | A (2.4.7) | Manual keyboard focus testing | Medium |
| **TC-ACC-005** | Form labels | A (1.3.1) | Axe DevTools | High |

**Accessibility Test Checklist:**
- [ ] All interactive elements accessible via keyboard (Tab, Enter, Escape)
- [ ] Screen reader announces: Budget updates, toast notifications, modal titles
- [ ] Color contrast ≥4.5:1 for normal text, ≥3:1 for large text
- [ ] Focus indicators visible on all focusable elements
- [ ] All form inputs have associated labels (htmlFor)

---

### 4.3 Security Testing

| Test ID | Test Case | Security Concern | Testing Method | Priority |
|---------|-----------|-----------------|----------------|----------|
| **TC-SEC-001** | JWT token expiration | Unauthorized access | Manually expire token, attempt API call | High |
| **TC-SEC-002** | CORS configuration | Cross-origin attacks | Test API from different origin | Medium |
| **TC-SEC-003** | Input sanitization (chat) | XSS attacks | Send `<script>alert('XSS')</script>` in chat | High |
| **TC-SEC-004** | localStorage data exposure | Sensitive data leak | Check if passwords/secrets stored in localStorage | High |
| **TC-SEC-005** | API rate limiting (Gemini) | DoS prevention | Send 100 chat requests in 1 second | Low |

**Security Best Practices Validation:**
- [ ] No passwords stored in localStorage (only JWT)
- [ ] Gemini API key not exposed in frontend (backend proxy)
- [ ] HTTPS enforced in production (Vercel default)
- [ ] Content Security Policy (CSP) headers set

---

### 4.4 Localization Testing (Norwegian)

| Test ID | Test Case | Expected Result | Priority |
|---------|-----------|-----------------|----------|
| **TC-LOC-001** | All UI text in Norwegian | No English text visible (except code/technical terms) | High |
| **TC-LOC-002** | Date formatting | Dates shown as "15. mai 2026" (Norwegian format) | Medium |
| **TC-LOC-003** | Number formatting | Costs shown as "105 MNOK" (space separator, not comma) | Medium |
| **TC-LOC-004** | AI supplier language | AI responses in Norwegian, culturally appropriate | Critical |
| **TC-LOC-005** | Error messages in Norwegian | All validation errors in Norwegian | High |

**Norwegian Language Checklist:**
- [ ] All buttons, labels, headings in Norwegian
- [ ] Error messages: "Feil e-post eller passord" (not "Invalid credentials")
- [ ] Toast notifications: "Lagt til i plan" (not "Added to plan")
- [ ] AI personas use Norwegian construction terminology
- [ ] Help documentation in Norwegian

---

## 5. AI Quality Testing

### 5.1 AI Negotiation Realism

**Objective:** Ensure AI suppliers feel realistic, challenging, and fair

**Test Scenarios (Manual Testing Required):**

| Scenario ID | Scenario Description | Expected AI Behavior | Pass Criteria |
|-------------|---------------------|---------------------|---------------|
| **AI-001** | User asks for quote without context | AI asks clarifying questions OR makes reasonable assumption | AI doesn't hallucinate details not in WBS |
| **AI-002** | User lowballs (offers 50% of baseline) | AI politely refuses, explains why too low | AI doesn't accept unreasonable offers |
| **AI-003** | User negotiates with reference to kravspec (F-codes) | AI acknowledges technical requirements, adjusts if valid | AI demonstrates understanding of requirements |
| **AI-004** | User pushes back twice (within reason) | AI concedes gradually (concession_rate), doesn't cave immediately | AI follows hidden parameters (1.15 → 1.10 → 1.05) |
| **AI-005** | User negotiates beyond patience limit | AI walks away politely: "Dette er mitt siste tilbud" | AI enforces patience parameter (3 rounds) |
| **AI-006** | User switches suppliers mid-negotiation | New supplier starts fresh (no memory of previous chat) | No context bleed between suppliers |
| **AI-007** | User renegotiates same item after commitment | AI remembers previous negotiation, may be less flexible | AI references past agreement: "Vi snakket om dette..." |

**Testing Process:**
1. Week 3: Create 5 system prompts (Bjørn, Kari, Per, Silje, Tor)
2. Test each prompt with 10 sample negotiations (50 total tests)
3. Log results: Pass/Fail for each scenario
4. Tune prompts based on failures (adjust concession_rate, patience, tone)
5. Re-test failed scenarios
6. Goal: 80%+ pass rate across all 50 tests

---

### 5.2 AI Consistency Testing

**Objective:** Ensure same supplier produces consistent behavior across sessions

| Test ID | Test Case | Expected Result |
|---------|-----------|-----------------|
| **AI-CON-001** | Same request to same supplier (3 times) | Offers should be within ±5% (e.g., 115-125 MNOK for 120 baseline) |
| **AI-CON-002** | Personality consistency (Bjørn = skeptical) | Bjørn always cautious, references quality, quotes slightly higher |
| **AI-CON-003** | Concession pattern | Each supplier follows their concession_rate (Bjørn: 5%, Kari: 3%, etc.) |

**Testing Method:**
- Use same prompt 3 times: "Trenger pristilbud for Grunnarbeid"
- Record initial offers from each supplier
- Calculate variance: Should be <10% (allows for LLM stochasticity)

---

### 5.3 AI Edge Cases

| Edge Case | Expected Behavior |
|-----------|------------------|
| User sends empty message | AI: "Jeg forstår ikke. Kan du utdype?" |
| User sends gibberish ("asdfgh") | AI: "Kan du omformulere spørsmålet?" |
| User asks unrelated question ("What's the weather?") | AI redirects: "Jeg er her for å diskutere [WBS item]. Hva trenger du å vite?" |
| API timeout (>10 sec) | Chat shows error message: "AI-tjenesten er midlertidig utilgjengelig. Prøv igjen." |
| Gemini API rate limit hit | Backend returns 429, Frontend shows: "For mange forespørsler. Vent 1 minutt." |

---

## 6. User Acceptance Testing (UAT)

### 6.1 UAT Objectives

**Goal:** Validate learning objectives and user satisfaction with 5-10 real students

**Participants:**
- 5-10 students from Norwegian university (NTNU, UiO, etc.)
- Mix of 3rd-year engineering students and PM course enrollees
- Recruited via professor or student organization

**Duration:** 1 week (Week 4)

**Method:**
1. Pre-test survey: Background, PM knowledge level
2. Guided session: Student completes full game (45-60 min)
3. Post-test survey: Satisfaction, learning outcomes, feedback
4. Semi-structured interview: 5-10 min feedback session

---

### 6.2 UAT Test Scenarios

| Scenario | Learning Objective | Success Criteria |
|----------|-------------------|------------------|
| **UAT-001: First-time user completes game** | Can navigate UI without help | Student completes all 15 WBS items without needing assistance |
| **UAT-002: Budget awareness** | Understands budget constraint | Student stays within 700 MNOK ±3% OR recognizes when over budget |
| **UAT-003: Negotiation skills** | Demonstrates negotiation attempt | Student negotiates at least 10/15 items (doesn't accept first offer) |
| **UAT-004: Strategic renegotiation** | Realizes need to adjust plan | Student renegotiates at least 1 item to reduce budget/timeline |
| **UAT-005: AI realism** | Finds AI believable | Student rates AI realism ≥4/5 in post-survey |

---

### 6.3 UAT Survey Questions

**Pre-Test Survey:**
1. Alder: ___
2. Studieprogram: ___
3. Har du tatt kurs i prosjektledelse før? (Ja / Nei)
4. Har du erfaring med forhandling? (1-5 skala)

**Post-Test Survey (1-5 Likert Scale):**
1. **Enkelhet:** Hvor enkelt var det å navigere i simuleringen? (1=Vanskelig, 5=Veldig enkelt)
2. **Realisme:** Hvor realistiske var AI-leverandørene? (1=Urealistisk, 5=Veldig realistisk)
3. **Læring:** Føler du at du lærte noe om prosjektplanlegging? (1=Nei, 5=Ja, mye)
4. **Engasjement:** Hvor engasjerende var simuleringen? (1=Kjedelig, 5=Veldig engasjerende)
5. **Vil du anbefale dette til andre studenter?** (Ja / Nei / Kanskje)

**Open-Ended Questions:**
- Hva likte du best med simuleringen?
- Hva var mest utfordrende?
- Hva ville du endret eller forbedret?
- Følte du at AI-leverandørene var realistiske? Hvorfor/hvorfor ikke?

**Success Criteria:**
- ≥80% rate Enkelhet ≥4/5
- ≥80% rate Realisme ≥4/5
- ≥70% rate Læring ≥4/5
- ≥85% would recommend to others

---

## 7. Test Automation

### 7.1 Unit Test Automation (Vitest)

**Coverage Target:** 60%

**Automated Tests:**
- All utility functions (calculateTotalCost, validatePlan, etc.)
- React components (Button, Input, ProgressBar, WBSItem, ChatMessage)
- Validation logic (budget, timeline, dependencies)

**Run Command:**
```bash
npm run test              # Run all unit tests
npm run test:coverage     # Generate coverage report
```

**CI Integration:**
- GitHub Actions workflow runs tests on every PR
- Fail PR if coverage drops below 60%

---

### 7.2 E2E Test Automation (Playwright)

**Coverage Target:** 10% (3-5 critical flows)

**Automated E2E Tests:**
1. Happy path: Register → Negotiate → Submit → Pass → Export
2. Renegotiation path: Commit → Renegotiate → Lower cost → Submit → Pass
3. Validation failure path: Over budget → Error → Renegotiate → Pass

**Run Command:**
```bash
npx playwright test                    # Run all E2E tests
npx playwright test --headed           # Run with browser visible
npx playwright test --debug            # Run with Playwright Inspector
```

**CI Integration:**
- Run E2E tests nightly (not on every PR—too slow)
- Run E2E tests before production deployment

---

### 7.3 API Test Automation (Pytest)

**Coverage Target:** 100% of 3 backend endpoints

**Automated API Tests:**
- `POST /api/chat`: Send message → receive AI response
- `GET /api/health`: Health check returns 200 OK
- `POST /api/validate` (if implemented server-side): Validate plan → return pass/fail

**Run Command:**
```bash
cd backend
pytest tests/                 # Run all API tests
pytest tests/ --cov=app       # With coverage report
```

---

## 8. Test Environment

### 8.1 Development Environment

**Setup:**
- **Frontend:** `npm run dev` (localhost:5173)
- **Backend:** `uvicorn main:app --reload` (localhost:8000)
- **Database:** None (localStorage only)
- **Auth:** Supabase (shared dev project)
- **AI:** Gemini API (dev API key, rate-limited)

**Test Data:**
- wbs.json with 15 items (static)
- suppliers.json with 5 suppliers (static)
- Mock localStorage sessions for testing

---

### 8.2 Staging Environment

**Setup:**
- **Frontend:** Deployed to Vercel preview (PR-based)
- **Backend:** Vercel serverless functions (preview environment)
- **Auth:** Supabase (dev project)
- **AI:** Gemini API (dev API key)

**Purpose:**
- Manual QA testing
- UAT with real users
- Performance testing (Lighthouse)

---

### 8.3 Production Environment

**Setup:**
- **Frontend:** Vercel production (nye-haedda.vercel.app)
- **Backend:** Vercel serverless functions (production)
- **Auth:** Supabase (production project)
- **AI:** Gemini API (production API key, higher rate limits)

**Promotion Criteria:**
- All critical bugs fixed
- UAT success criteria met (80%+ satisfaction)
- Performance targets met (Lighthouse >90)
- Security checklist passed

---

## 9. Test Data

### 9.1 Static Test Data

**wbs.json (15 items):**
- WBS codes: 1.1, 1.3.1, 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2
- Baseline costs: Range from 20-250 MNOK (total ~650 MNOK)
- Baseline durations: Range from 1-6 months
- Dependencies: 2-3 items have dependencies (e.g., 2.1 depends on 1.3.1)

**suppliers.json (5 suppliers):**
- Bjørn Eriksen (Totalentreprenør): initial_margin 1.20, concession_rate 0.05, patience 3
- Kari Andersen (Rørlegger): initial_margin 1.18, concession_rate 0.03, patience 4
- Per Johansen (Elektriker): initial_margin 1.25, concession_rate 0.07, patience 2
- Silje Henriksen (Arkitekt): initial_margin 1.15, concession_rate 0.04, patience 5
- Tor Kristoffersen (Maler): initial_margin 1.22, concession_rate 0.06, patience 3

---

### 9.2 Dynamic Test Data

**Mock GameSession (for unit tests):**
```json
{
  "game_id": "test-session-001",
  "user_id": "user-123",
  "created_at": "2025-12-07T10:00:00Z",
  "status": "in_progress",
  "current_plan": {
    "1.3.1": {
      "supplier_id": "bjorn",
      "cost": 105,
      "duration": 2.5,
      "start_date": "2025-01-15",
      "end_date": "2025-04-01"
    }
  },
  "plan_history": [
    {
      "timestamp": "2025-12-07T10:30:00Z",
      "action": "commit",
      "wbs_code": "1.3.1",
      "supplier_id": "bjorn",
      "cost": 105,
      "duration": 2.5
    }
  ],
  "chat_logs": [],
  "metrics": {
    "total_budget_used": 105,
    "projected_end_date": "2025-04-01",
    "negotiation_count": 2,
    "renegotiation_count": 0
  }
}
```

---

## 10. Defect Management

### 10.1 Bug Severity Levels

| Severity | Definition | Example | Response Time |
|----------|-----------|---------|---------------|
| **Critical** | App unusable, data loss, security breach | Login broken, AI not responding, XSS vulnerability | Fix immediately (<4 hours) |
| **High** | Core feature broken, workaround available | Commitment not updating plan, validation logic wrong | Fix within 1 day |
| **Medium** | Minor feature broken, UX degraded | Toast notification not showing, animation glitch | Fix within 1 week |
| **Low** | Cosmetic issue, typo, minor inconvenience | Button text misaligned, Norwegian typo | Fix when convenient |

---

### 10.2 Bug Report Template (GitHub Issues)

```markdown
## Bug Report

**Title:** [Concise description of bug]

**Severity:** Critical / High / Medium / Low

**Environment:**
- OS: Windows 10 / macOS / Linux
- Browser: Chrome 120 / Firefox 121 / Safari 17
- URL: https://nye-haedda.vercel.app/dashboard

**Steps to Reproduce:**
1. Login with user@example.com
2. Navigate to Dashboard
3. Click "Kontakt Leverandør" on WBS 1.3.1
4. Send message to Bjørn

**Expected Result:**
AI response appears within 1-3 seconds

**Actual Result:**
Chat shows "Loading..." indefinitely, no AI response

**Screenshots:**
[Attach screenshot if applicable]

**Console Errors:**
[Copy/paste any browser console errors]

**Additional Context:**
[Any other relevant information]
```

---

### 10.3 Bug Triage Process

1. **Report:** Developer or QA creates GitHub issue with bug template
2. **Triage:** Product Owner assigns severity within 24 hours
3. **Assignment:** Scrum Master assigns to developer based on severity
4. **Fix:** Developer creates PR with fix + test case
5. **Verify:** QA verifies fix in staging environment
6. **Close:** Issue closed after deployment to production

---

## 11. Test Schedule

### 11.1 Testing Timeline (4 Weeks)

| Week | Testing Activities | Deliverables |
|------|-------------------|--------------|
| **Week 1** | - Unit tests for utility functions<br>- API tests for FastAPI endpoints | 30% code coverage |
| **Week 2** | - Unit tests for React components<br>- Integration tests (Dashboard, WBS) | 50% code coverage |
| **Week 3** | - AI quality testing (50 scenarios)<br>- E2E tests (happy path)<br>- Performance testing | AI prompts tuned, E2E passing |
| **Week 4** | - UAT with 5-10 students<br>- Accessibility testing<br>- Security testing<br>- Final bug fixes | UAT report, 60% coverage, 0 critical bugs |

---

### 11.2 Test Milestones

| Milestone | Date | Exit Criteria |
|-----------|------|---------------|
| **Unit Tests Complete** | End of Week 2 | 50% code coverage, all utility functions tested |
| **AI Prompts Validated** | Mid Week 3 | 80% pass rate on AI quality scenarios |
| **E2E Tests Passing** | End of Week 3 | 3 critical flows automated and passing |
| **UAT Complete** | Mid Week 4 | 5+ students tested, 80% satisfaction |
| **Production Ready** | End of Week 4 | 60% coverage, 0 critical bugs, UAT success |

---

## Appendix A: Test Coverage Summary

| Test Level | Target Coverage | Measurement |
|-----------|----------------|-------------|
| Unit Tests | 60% code coverage | Vitest coverage report |
| Integration Tests | 30% (critical paths) | Manual tracking + Playwright |
| E2E Tests | 10% (3-5 flows) | Playwright test count |
| Manual Tests | 100% of Must-Have features | Test case execution log |
| UAT | 5-10 real users | UAT survey results |

---

## Appendix B: Test Execution Checklist

**Before Each Release:**
- [ ] All unit tests passing (`npm run test`)
- [ ] E2E tests passing (`npx playwright test`)
- [ ] API tests passing (`pytest`)
- [ ] Lighthouse score >90 (Performance, Accessibility, Best Practices)
- [ ] Manual smoke test (login → negotiate → submit → export)
- [ ] Norwegian language review (no English text visible)
- [ ] 0 critical bugs open
- [ ] <5 high severity bugs open
- [ ] UAT survey results ≥80% satisfaction (if UAT conducted)

---

**End of Test Design Document**

**Next Steps:**
1. Review with QA team and developers
2. Set up test infrastructure (Vitest, Playwright, GitHub Actions)
3. Begin writing unit tests in Week 1
4. Execute test plan according to schedule

**Document Status:** Complete and ready for implementation.
