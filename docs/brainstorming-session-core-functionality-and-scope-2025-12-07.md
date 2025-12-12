# Brainstorming Session Report - Core Functionality and Scope

> **⚠️ HISTORICAL DOCUMENT:** This brainstorming session reflects the original v1.0 scope (15 negotiable WBS, 5 suppliers). For current POC scope, see:
> - **PRD.md (v2.0):** 3 negotiable + 12 locked WBS, 4 AI agents (Owner + 3 suppliers)
> - **product-brief.md (v2.0):** 310/650/700 MNOK budget model, inflexible time constraint
> - **AI_AGENT_SYSTEM_PROMPTS.md:** Complete v2.0 AI agent specifications

- **Date:** 2025-12-07
- **Facilitator:** Solution Architect & Business Analyst
- **Topic:** Core Functionality Definition and MVP Scope
- **Session Goals:** Define MVP features with simplified architecture using localStorage, establish data flow, identify visualization needs, and create clear scope boundaries

---

## 1. Session Goals

**Stated Goals:**
- Define the Minimum Viable Product (MVP) feature set with clear prioritization
- Design a simplified architecture using Supabase Auth + localStorage (no database tables)
- Map the complete data flow through the system
- Identify all visualization and UI component requirements
- Establish scope boundaries: Must-Have (MVP), Should-Have (Post-MVP), Could-Have (Future), Won't-Have (Out of Scope)
- Define the core game loop mechanics in technical detail
- Maximize development speed while maintaining quality

**Approach:** MoSCoW Prioritization, Data Flow Mapping, Component Inventory, localStorage Schema Design, Simplified Backend Architecture

**Key Architectural Decision:**
- **Storage:** localStorage (browser-based, no database tables)
- **Auth:** Supabase Auth only (user_id + JWT)
- **Backend:** Minimal FastAPI (AI chat + validation)
- **Export:** Full session history as downloadable JSON
- **Rationale:** 45-60 min single-session use case doesn't require full database; saves 1-2 weeks development time

---

## 2. Brainstorming Techniques

**Technique 1: MoSCoW Prioritization**
- **Must Have:** Critical features without which the MVP cannot function
- **Should Have:** Important features that significantly enhance value
- **Could Have:** Nice-to-have features
- **Won't Have:** Explicitly out of scope

**Technique 2: localStorage Schema Design**
- Define complete data structure stored in browser
- Plan for history tracking and export

**Technique 3: Data Flow Mapping**
- Map user actions → localStorage → backend API → AI → frontend

**Technique 4: Component Inventory**
- Catalog all UI components needed

---

## 3. Generated Ideas

### 3.1 MoSCoW Feature Prioritization

#### MUST HAVE (MVP - Week 1-5)

**M1: User Registration & Authentication**
- **Description:** Email-based registration and login via Supabase Auth
- **Rationale:** Required to uniquely identify users and associate exported sessions with specific students
- **User Stories:**
  - As Sara, I want to register with my university email so my session is associated with my identity
  - As Magnus, I want to log in to access my saved session if I refresh the page
  - As the System, I want to authenticate users so exported sessions include verified user_id
- **Implementation:**
  - Supabase Auth SDK (frontend only)
  - JWT token stored in localStorage
  - No database tables (auth.users managed by Supabase)
- **Acceptance Criteria:**
  - User can register with email + password
  - User receives email verification
  - User can log in and JWT persists across page refreshes
  - User can log out (clears JWT and session data)
- **Effort Estimate:** 1 day (Supabase simplifies this)

**M2: Session Initialization & localStorage Setup**
- **Description:** Create new game session in localStorage when user starts
- **Rationale:** Foundation for all game data storage
- **User Stories:**
  - As Sara, I want to start a new simulation so I can begin practicing negotiation
  - As the System, I want to initialize session data with default values
- **Implementation:**
```javascript
// On "Start New Game" click:
const gameSession = {
  user_id: getUserIdFromJWT(),
  game_id: generateUUID(),
  created_at: new Date().toISOString(),
  status: 'in_progress',

  wbs_items: loadStaticWBSData(), // From JSON file
  suppliers: loadStaticSupplierData(), // From JSON file

  plan_history: [],
  chat_logs: [],
  current_plan: {},

  metrics: {
    total_budget_used: 0,
    projected_end_date: null,
    negotiation_count: 0,
    renegotiation_count: 0,
    time_spent_seconds: 0
  }
};

localStorage.setItem(
  `nye-haedda-session-${user_id}`,
  JSON.stringify(gameSession)
);
```
- **Acceptance Criteria:**
  - Clicking "Start New Game" creates session in localStorage
  - Session includes game_id, user_id, timestamps
  - Static data (WBS, suppliers) loaded from JSON files
  - Previous session is archived before starting new one
- **Effort Estimate:** 1 day

**M3: Project Dashboard (Constraint Overview)**
- **Description:** Main view showing project constraints and current status (read from localStorage)
- **Rationale:** Users need constant visibility of budget and timeline
- **UI Components:**
  - Budget meter: "X / 700 MNOK used" (progress bar, color-coded)
  - Timeline indicator: "Projected End Date: [Date]" (green if <May 15, red if >)
  - Project metadata: Start date, deadline
  - Quick stats: "X/15 WBS items completed", "X negotiations"
- **Data Source:**
```javascript
const session = JSON.parse(localStorage.getItem(`nye-haedda-session-${user_id}`));
const budgetUsed = session.metrics.total_budget_used;
const endDate = session.metrics.projected_end_date;
const completedItems = Object.keys(session.current_plan).length;
```
- **Acceptance Criteria:**
  - Dashboard displays real-time data from localStorage
  - Budget/timeline update immediately after plan commitment
  - Color-coded warnings when constraints exceeded
- **Effort Estimate:** 2 days

**M4: WBS View (Work Breakdown Structure Browser)**
- **Description:** Display WBS items from static JSON file with status from localStorage
- **Rationale:** Users browse and select items to negotiate
- **Data Structure (Static JSON file: `/data/wbs.json`):**
```json
[
  {
    "id": "1.3.1",
    "name": "Grunnarbeid",
    "description": "Site preparation and earthwork",
    "baseline_cost": 100,
    "baseline_duration": 2,
    "dependencies": ["1.2"],
    "suggested_suppliers": ["bjorn-eriksen", "kari-jensen"]
  },
  {
    "id": "2.1",
    "name": "Råbygg - Fundament",
    "description": "Foundation construction",
    "baseline_cost": 150,
    "baseline_duration": 3,
    "dependencies": ["1.3.1"],
    "suggested_suppliers": ["bjorn-eriksen"]
  }
  // ... all 15 WBS items
]
```
- **UI Display:**
  - List/tree view of WBS items
  - Status indicator: ⚪ Pending (not in current_plan), 🟢 Completed (in current_plan)
  - Show committed values if completed
  - "Contact Supplier" or "Renegotiate" button
- **Acceptance Criteria:**
  - All WBS items rendered from static JSON
  - Status reflects current_plan in localStorage
  - Dependencies clearly shown
- **Effort Estimate:** 2 days

**M5: Supplier Directory**
- **Description:** Display available suppliers from static JSON file
- **Data Structure (Static JSON file: `/data/suppliers.json`):**
```json
[
  {
    "id": "bjorn-eriksen",
    "name": "Bjørn Eriksen",
    "role": "Totalentreprenør",
    "specialty": ["1.3.1", "2.1", "2.2"],
    "persona_summary": "Profit-driven, shrewd negotiator. Starts high but flexible with good arguments.",
    "system_prompt": "You are Bjørn Eriksen, a general contractor with 20 years experience...",
    "hidden_params": {
      "min_cost_multiplier": 0.88,
      "min_duration_multiplier": 0.92
    }
  },
  {
    "id": "siri-hansen",
    "name": "Siri Hansen",
    "role": "Arkitekt",
    "specialty": ["1.1", "2.4"],
    "persona_summary": "Quality-focused architect. Resists compromises affecting design.",
    "system_prompt": "You are Siri Hansen, an award-winning architect...",
    "hidden_params": {
      "min_cost_multiplier": 0.95,
      "min_duration_multiplier": 0.95
    }
  }
  // ... 5-10 suppliers total
]
```
- **UI:**
  - Supplier cards showing name, role, specialty
  - "Start Chat" button
  - Filter by WBS item relevance
- **Note:** `system_prompt` and `hidden_params` sent to backend (not shown to user)
- **Effort Estimate:** 1 day

**M6: AI Chat Interface (Negotiation Window)**
- **Description:** Real-time chat with AI suppliers
- **UI Components:**
  - Chat window with message bubbles
  - Text input + send button
  - Supplier context header
  - "Accept Offer" button (when AI makes valid offer)
  - Document reference sidebar
- **Data Flow:**
```javascript
// User sends message
const message = {
  timestamp: new Date().toISOString(),
  wbs_item: "1.3.1",
  supplier: "bjorn-eriksen",
  sender: "user",
  message: userInput
};

// Add to localStorage
session.chat_logs.push(message);
session.metrics.negotiation_count++;
localStorage.setItem(`nye-haedda-session-${user_id}`, JSON.stringify(session));

// Send to backend
const response = await fetch('/api/chat/message', {
  method: 'POST',
  body: JSON.stringify({
    supplier_id: "bjorn-eriksen",
    wbs_item: session.wbs_items.find(w => w.id === "1.3.1"),
    chat_history: session.chat_logs.filter(c => c.wbs_item === "1.3.1" && c.supplier === "bjorn-eriksen"),
    user_message: userInput
  })
});

const aiMessage = await response.json();

// Add AI response to localStorage
session.chat_logs.push({
  timestamp: new Date().toISOString(),
  wbs_item: "1.3.1",
  supplier: "bjorn-eriksen",
  sender: "ai",
  message: aiMessage.response,
  extracted_offer: aiMessage.offer // {cost: 120, duration: 3}
});
localStorage.setItem(`nye-haedda-session-${user_id}`, JSON.stringify(session));
```
- **Acceptance Criteria:**
  - Messages appear in chat window
  - All messages logged to localStorage
  - AI responds within 3 seconds
  - Chat history persists on page refresh
- **Effort Estimate:** 3 days

**M7: AI Supplier Logic (Backend - Gemini Integration)**
- **Description:** Stateless backend endpoint that generates AI responses
- **Backend Endpoint:**
```python
# FastAPI endpoint
@app.post("/api/chat/message")
async def chat_message(request: ChatRequest):
    # Load supplier data from request (frontend sends it)
    supplier = request.supplier_data  # includes system_prompt, hidden_params
    wbs_item = request.wbs_item
    chat_history = request.chat_history  # full conversation
    user_message = request.user_message

    # Load requirements/WBS context (from static files on server)
    requirements = load_requirements_spec()

    # Construct AI prompt
    prompt = f"""
{supplier.system_prompt}

Context:
- WBS Item: {wbs_item.id} - {wbs_item.name}
- Baseline Estimate: {wbs_item.baseline_cost} MNOK, {wbs_item.baseline_duration} months
- Requirements: {get_relevant_requirements(wbs_item.id, requirements)}

Negotiation Rules:
- You cannot accept cost below {wbs_item.baseline_cost * supplier.hidden_params.min_cost_multiplier} MNOK
- You cannot accept duration below {wbs_item.baseline_duration * supplier.hidden_params.min_duration_multiplier} months
- You should start with inflated offers and negotiate down based on user arguments
- Reference specific requirements when justifying your position

Previous conversation:
{format_chat_history(chat_history)}

User: {user_message}
Assistant:
"""

    # Call Gemini API
    ai_response = await gemini_client.generate(prompt)

    # Extract structured offer if present (regex or LLM extraction)
    extracted_offer = extract_offer_from_text(ai_response)

    return {
        "response": ai_response,
        "offer": extracted_offer  # {cost: 120, duration: 3} or null
    }
```
- **Key Design:** Backend is stateless - frontend sends all context
- **Acceptance Criteria:**
  - AI responds with persona-appropriate messages
  - AI references WBS and requirements
  - AI respects hidden minimum thresholds
  - No hallucinations (factual about project docs)
- **Effort Estimate:** 4 days (includes prompt engineering)

**M8: Quote Acceptance & Plan Commitment**
- **Description:** Accept AI offer and update localStorage
- **Implementation:**
```javascript
function acceptOffer(wbsItemId, supplierId, cost, duration) {
  const session = getSession();

  // Calculate start date based on dependencies
  const wbsItem = session.wbs_items.find(w => w.id === wbsItemId);
  const startDate = calculateStartDate(wbsItem.dependencies, session.current_plan);
  const endDate = addMonths(startDate, duration);

  // Add to plan_history (tracks all changes)
  session.plan_history.push({
    timestamp: new Date().toISOString(),
    action: 'commit',
    wbs_item: wbsItemId,
    supplier: supplierId,
    cost: cost,
    duration: duration,
    start_date: startDate,
    end_date: endDate
  });

  // Update current_plan (current state)
  session.current_plan[wbsItemId] = {
    supplier: supplierId,
    cost: cost,
    duration: duration,
    start_date: startDate,
    end_date: endDate,
    committed_at: new Date().toISOString()
  };

  // Recalculate metrics
  session.metrics.total_budget_used = calculateTotalCost(session.current_plan);
  session.metrics.projected_end_date = calculateCriticalPath(session.current_plan, session.wbs_items);

  saveSession(session);

  // Trigger dashboard refresh
  refreshDashboard();
}
```
- **Acceptance Criteria:**
  - Plan updates immediately in localStorage
  - Dashboard shows updated budget/timeline
  - WBS item status changes to "Completed"
  - History preserved in plan_history array
- **Effort Estimate:** 2 days

**M9: Real-Time Plan Validation (Client-Side)**
- **Description:** Validate plan against constraints (can be client-side or backend)
- **Implementation (Client-Side):**
```javascript
function validatePlan(session) {
  const errors = [];
  const warnings = [];

  // 1. Completeness check
  const committedCount = Object.keys(session.current_plan).length;
  const totalWBSItems = session.wbs_items.length;
  if (committedCount < totalWBSItems) {
    errors.push({
      type: 'incomplete',
      message: `Only ${committedCount}/${totalWBSItems} WBS items committed`
    });
  }

  // 2. Budget check
  const totalCost = session.metrics.total_budget_used;
  if (totalCost > 700) {
    errors.push({
      type: 'budget',
      message: `Budget exceeded by ${totalCost - 700} MNOK`,
      current: totalCost,
      limit: 700,
      suggestions: getHighCostItems(session.current_plan)
    });
  } else if (totalCost > 680) {
    warnings.push({
      type: 'budget',
      message: `Budget at ${(totalCost/700*100).toFixed(1)}% - limited flexibility remaining`
    });
  }

  // 3. Timeline check
  const endDate = new Date(session.metrics.projected_end_date);
  const deadline = new Date('2026-05-15');
  if (endDate > deadline) {
    const daysLate = Math.ceil((endDate - deadline) / (1000*60*60*24));
    errors.push({
      type: 'timeline',
      message: `Project delayed by ${daysLate} days`,
      current: endDate.toISOString().split('T')[0],
      limit: '2026-05-15'
    });
  }

  // 4. Dependency check
  for (const [wbsId, entry] of Object.entries(session.current_plan)) {
    const wbsItem = session.wbs_items.find(w => w.id === wbsId);
    for (const depId of wbsItem.dependencies) {
      const depEntry = session.current_plan[depId];
      if (!depEntry) {
        errors.push({
          type: 'dependency',
          message: `${wbsId} requires ${depId} to be completed first`
        });
      } else if (new Date(entry.start_date) < new Date(depEntry.end_date)) {
        errors.push({
          type: 'dependency',
          message: `${wbsId} starts before ${depId} finishes`
        });
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors: errors,
    warnings: warnings
  };
}
```
- **Alternative:** Send to backend `/api/validate` if validation logic is complex
- **Acceptance Criteria:**
  - Validation runs after every commitment (for warnings)
  - Validation runs before submission (for errors)
  - Clear error messages with actionable suggestions
- **Effort Estimate:** 2 days

**M10: Plan Submission & Win/Loss State**
- **Description:** Submit plan and show success/failure
- **Implementation:**
```javascript
function submitPlan() {
  const session = getSession();
  const validation = validatePlan(session);

  if (!validation.valid) {
    // Show error modal
    showValidationErrorModal(validation.errors);
    return;
  }

  // Mark session as completed
  session.status = 'completed';
  session.completed_at = new Date().toISOString();
  session.metrics.time_spent_seconds = calculateTimeSpent(session.created_at, session.completed_at);
  saveSession(session);

  // Show success screen
  showSuccessModal({
    total_cost: session.metrics.total_budget_used,
    completion_date: session.metrics.projected_end_date,
    time_spent: formatDuration(session.metrics.time_spent_seconds),
    negotiation_count: session.metrics.negotiation_count,
    renegotiation_count: session.metrics.renegotiation_count
  });
}
```
- **Success Screen:**
  - Congratulations message
  - Final stats
  - "Export Session" button
  - "Start New Game" button
- **Effort Estimate:** 1 day

**M11: Session Export (JSON Download)**
- **Description:** Download complete session history as JSON file
- **Implementation:**
```javascript
function exportSession() {
  const session = getSession();

  // Create comprehensive export object
  const exportData = {
    // Metadata
    export_version: "1.0",
    exported_at: new Date().toISOString(),

    // User & game info
    user_id: session.user_id,
    game_id: session.game_id,
    created_at: session.created_at,
    completed_at: session.completed_at,
    status: session.status,

    // Complete chat history (every message)
    chat_logs: session.chat_logs,

    // Complete plan history (every change)
    plan_history: session.plan_history,

    // Final plan state
    final_plan: session.current_plan,

    // Metrics
    metrics: session.metrics,

    // WBS reference (for context)
    wbs_items: session.wbs_items,

    // Validation result
    validation: validatePlan(session)
  };

  // Download as JSON file
  const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `nye-haedda-session-${session.user_id}-${session.game_id}.json`;
  a.click();
}
```
- **Export includes:**
  - Full chat history (every message with timestamps)
  - Complete plan_history (every commit/uncommit action)
  - Final plan state
  - All metrics
  - Validation results
- **Acceptance Criteria:**
  - Export button downloads complete JSON
  - File includes all session data
  - JSON is valid and readable
  - User can submit this file for coursework
- **Effort Estimate:** 1 day

**M12: Renegotiation Capability**
- **Description:** Uncommit plan entry and renegotiate
- **Implementation:**
```javascript
function renegotiate(wbsItemId) {
  const session = getSession();

  // Confirm with user
  if (!confirm('This will uncommit this item and recalculate your plan. Continue?')) {
    return;
  }

  // Add to plan_history
  session.plan_history.push({
    timestamp: new Date().toISOString(),
    action: 'uncommit',
    wbs_item: wbsItemId
  });

  // Remove from current_plan
  delete session.current_plan[wbsItemId];

  // Increment renegotiation count
  session.metrics.renegotiation_count++;

  // Recalculate metrics
  session.metrics.total_budget_used = calculateTotalCost(session.current_plan);
  session.metrics.projected_end_date = calculateCriticalPath(session.current_plan, session.wbs_items);

  saveSession(session);

  // Navigate back to chat (history preserved)
  openChatForWBS(wbsItemId);
}
```
- **Acceptance Criteria:**
  - User can uncommit any item
  - Dashboard recalculates immediately
  - Chat history preserved (can reference earlier conversation)
  - plan_history tracks the uncommit action
- **Effort Estimate:** 1 day

**M13: Resource Library (Document Access)**
- **Description:** Access project documents while negotiating
- **Implementation:**
  - Static PDF files in `/public/docs/` folder
  - Sidebar with links or embedded viewer
  - Documents: wbs.pdf, krav-spec.pdf, project-description.pdf
- **Acceptance Criteria:**
  - Documents accessible from any page
  - Can open while chat is active (split screen or new tab)
- **Effort Estimate:** 0.5 days

**M14: Session Persistence (localStorage Management)**
- **Description:** Save/load session from localStorage, handle page refresh
- **Implementation:**
```javascript
// Auto-save after every action
function saveSession(session) {
  localStorage.setItem(
    `nye-haedda-session-${session.user_id}`,
    JSON.stringify(session)
  );
}

// Load on page load
function getSession() {
  const userId = getUserIdFromJWT();
  const sessionData = localStorage.getItem(`nye-haedda-session-${userId}`);
  if (!sessionData) {
    return null; // No active session
  }
  return JSON.parse(sessionData);
}

// Resume or start new
function initializeApp() {
  const session = getSession();
  if (session && session.status === 'in_progress') {
    // Resume existing session
    showDashboard(session);
  } else {
    // Show "Start New Game" screen
    showWelcomeScreen();
  }
}
```
- **Acceptance Criteria:**
  - Session persists across page refreshes
  - User can resume if they close/reopen browser (same day)
  - Session cleared on logout
- **Effort Estimate:** 1 day

**M15: Basic Error Handling & Loading States**
- **Description:** User-friendly errors and loading indicators
- **Implementation:**
  - Loading spinner for AI responses
  - Error messages for network failures
  - Retry buttons
  - Offline detection
- **Effort Estimate:** 1 day (ongoing)

---

#### SHOULD HAVE (Post-MVP - Week 6-8)

**S1: Cloud Backup (Optional Save to Supabase Storage)**
- **Description:** Upload session JSON to Supabase Storage for cross-device access
- **Implementation:**
```javascript
async function saveToCloud() {
  const session = getSession();
  const fileName = `sessions/${session.user_id}/${session.game_id}.json`;

  await supabase.storage
    .from('game-sessions')
    .upload(fileName, JSON.stringify(session));

  alert('Session saved to cloud! You can resume on any device.');
}

async function loadFromCloud() {
  const userId = getUserIdFromJWT();
  const { data, error } = await supabase.storage
    .from('game-sessions')
    .list(`sessions/${userId}/`);

  // Show list of saved sessions, let user select
  // Download and load into localStorage
}
```
- **Why Should-Have:** Enables cross-device resume; optional for MVP
- **Effort Estimate:** 2 days

**S2: Visual Gantt Chart**
- **Description:** Timeline visualization of plan
- **Why Should-Have:** Table view is sufficient; Gantt is polish
- **Effort Estimate:** 3 days

**S3: Plan Export as PDF Report**
- **Description:** Formatted PDF with plan summary, chat excerpts, metrics
- **Why Should-Have:** JSON export is sufficient for MVP
- **Effort Estimate:** 3 days

**S4: Negotiation Hints System**
- **Description:** Contextual tips when user seems stuck
- **Effort Estimate:** 2 days

**S5: Auto-Save to Cloud (Background Upload)**
- **Description:** Auto-upload session to Supabase Storage every 5 minutes
- **Why Should-Have:** Protects against cache clearing; nice safety net
- **Effort Estimate:** 1 day

**S6: Session Import (Upload JSON)**
- **Description:** Upload previously exported JSON to resume on different device
- **Effort Estimate:** 1 day

**S7: Multiple Save Slots**
- **Description:** Allow user to have multiple concurrent sessions
- **Effort Estimate:** 2 days

---

#### COULD HAVE (Future)

**C1: Difficulty Settings**
- Easy/Medium/Hard modes with different AI stubbornness

**C2: Random Risk Events**
- "Steel prices rose 10%" mid-game

**C3: Instructor Dashboard**
- View all student sessions (requires database)

**C4: Alternative Scenarios**
- Different construction projects

**C5: Achievements/Badges**
- Gamification elements

**C6: Supplier Reputation System**
- Track relationship with each supplier

---

#### WON'T HAVE (Out of Scope)

Same as previous version (Execution Phase, 3D Visualization, VR, etc.)

---

### 3.2 localStorage Schema (Complete)

```javascript
// Key: nye-haedda-session-{user_id}
{
  // ===== METADATA =====
  "user_id": "abc123-def456",
  "game_id": "uuid-game-xxx",
  "created_at": "2025-12-07T10:00:00Z",
  "completed_at": null,  // Set when status becomes 'completed'
  "status": "in_progress",  // 'in_progress' | 'completed' | 'abandoned'

  // ===== STATIC DATA (Loaded from JSON files) =====
  "wbs_items": [
    {
      "id": "1.3.1",
      "name": "Grunnarbeid",
      "description": "Site preparation...",
      "baseline_cost": 100,
      "baseline_duration": 2,
      "dependencies": ["1.2"],
      "suggested_suppliers": ["bjorn-eriksen"]
    }
    // ... all WBS items
  ],

  "suppliers": [
    {
      "id": "bjorn-eriksen",
      "name": "Bjørn Eriksen",
      "role": "Totalentreprenør",
      "specialty": ["1.3.1", "2.1"],
      "persona_summary": "Profit-driven...",
      // system_prompt stored but not displayed to user
      "system_prompt": "You are Bjørn...",
      "hidden_params": {"min_cost_multiplier": 0.88}
    }
    // ... all suppliers
  ],

  // ===== CHAT HISTORY (Every message) =====
  "chat_logs": [
    {
      "timestamp": "2025-12-07T10:05:00Z",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "sender": "user",
      "message": "I need a quote for Grunnarbeid. Cost and duration?"
    },
    {
      "timestamp": "2025-12-07T10:05:03Z",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "sender": "ai",
      "message": "Based on current market rates, I estimate 120 MNOK and 3 months for Grunnarbeid...",
      "extracted_offer": {
        "cost": 120,
        "duration": 3
      }
    },
    {
      "timestamp": "2025-12-07T10:08:00Z",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "sender": "user",
      "message": "That's too high. According to Requirement F-003, only 30% rocky terrain..."
    },
    {
      "timestamp": "2025-12-07T10:08:05Z",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "sender": "ai",
      "message": "Good catch. I can revise to 105 MNOK, 2.5 months.",
      "extracted_offer": {
        "cost": 105,
        "duration": 2.5
      }
    }
    // ... every message from all negotiations
  ],

  // ===== PLAN HISTORY (Every change) =====
  "plan_history": [
    {
      "timestamp": "2025-12-07T10:15:00Z",
      "action": "commit",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "cost": 105,
      "duration": 2.5,
      "start_date": "2025-01-15",
      "end_date": "2025-04-01"
    },
    {
      "timestamp": "2025-12-07T10:45:00Z",
      "action": "uncommit",
      "wbs_item": "1.3.1",
      "reason": "Total budget exceeded, need to renegotiate"
    },
    {
      "timestamp": "2025-12-07T10:52:00Z",
      "action": "commit",
      "wbs_item": "1.3.1",
      "supplier": "bjorn-eriksen",
      "cost": 100,
      "duration": 2.5,
      "start_date": "2025-01-15",
      "end_date": "2025-04-01"
    },
    {
      "timestamp": "2025-12-07T11:00:00Z",
      "action": "commit",
      "wbs_item": "2.1",
      "supplier": "bjorn-eriksen",
      "cost": 145,
      "duration": 3,
      "start_date": "2025-04-01",
      "end_date": "2025-07-01"
    }
    // ... every commit/uncommit action
  ],

  // ===== CURRENT PLAN STATE =====
  "current_plan": {
    "1.3.1": {
      "supplier": "bjorn-eriksen",
      "cost": 100,
      "duration": 2.5,
      "start_date": "2025-01-15",
      "end_date": "2025-04-01",
      "committed_at": "2025-12-07T10:52:00Z"
    },
    "2.1": {
      "supplier": "bjorn-eriksen",
      "cost": 145,
      "duration": 3,
      "start_date": "2025-04-01",
      "end_date": "2025-07-01",
      "committed_at": "2025-12-07T11:00:00Z"
    }
    // ... only currently committed items (uncommitted items removed)
  },

  // ===== REAL-TIME METRICS =====
  "metrics": {
    "total_budget_used": 245,  // Sum of current_plan costs
    "projected_end_date": "2026-04-15",  // Critical path calculation
    "negotiation_count": 47,  // Total messages sent by user
    "renegotiation_count": 1,  // Number of uncommit actions
    "time_spent_seconds": 3120  // Calculated from created_at to now
  }
}
```

---

### 3.3 Data Flow Architecture (Simplified)

**Flow 1: User Registration & Authentication**
```
User (Browser)
  → POST /auth/register {email, password}
    → Supabase Auth API
      → Creates user in auth.users
      → Sends verification email
    ← Returns user_id + JWT
  ← Frontend stores JWT in localStorage['auth-token']
```

**Flow 2: Session Initialization**
```
User clicks "Start New Game"
  → Frontend generates new session object
  → Loads static WBS data from /data/wbs.json
  → Loads static supplier data from /data/suppliers.json
  → Saves to localStorage['nye-haedda-session-{user_id}']
  ← Redirects to Dashboard
```

**Flow 3: Dashboard Load**
```
Dashboard component mounts
  → Read session from localStorage
  → Calculate current metrics:
      - total_budget_used = sum(current_plan.*.cost)
      - projected_end_date = calculateCriticalPath(current_plan, wbs_items)
      - completed_count = Object.keys(current_plan).length
  ← Render dashboard with real-time values
```

**Flow 4: AI Negotiation**
```
User sends chat message
  → Add message to session.chat_logs (localStorage)
  → Increment session.metrics.negotiation_count
  → POST /api/chat/message
      {
        supplier: {id, system_prompt, hidden_params},
        wbs_item: {id, name, baseline_cost, baseline_duration},
        chat_history: [all previous messages for this wbs+supplier],
        user_message: "Can you do 100 MNOK?"
      }
    → Backend constructs prompt:
        - Supplier persona (system_prompt)
        - WBS context
        - Requirements (from static file on server)
        - Conversation history
        - Negotiation rules (hidden_params)
    → Backend calls Gemini API
    ← Gemini returns AI response
    → Backend extracts structured offer (if present)
    ← Returns {response: "I can do 105 MNOK for 2.5 months", offer: {cost: 105, duration: 2.5}}
  ← Frontend adds AI message to session.chat_logs (localStorage)
  ← Display in chat window
```

**Flow 5: Quote Acceptance & Commitment**
```
User clicks "Accept Offer"
  → Calculate start_date based on dependencies
  → Add to session.plan_history (localStorage)
  → Update session.current_plan[wbs_item_id] (localStorage)
  → Recalculate metrics:
      session.metrics.total_budget_used = sum(current_plan.*.cost)
      session.metrics.projected_end_date = calculateCriticalPath()
  → Save session to localStorage
  ← Dashboard auto-refreshes (reads from localStorage)
  ← WBS item status changes to "Completed"
```

**Flow 6: Plan Validation & Submission**
```
User clicks "Submit Plan"
  → Read session from localStorage
  → Run validation (client-side or backend):
      - Completeness: all WBS items committed?
      - Budget: total_cost <= 700 MNOK?
      - Timeline: projected_end_date <= 2026-05-15?
      - Dependencies: all dependencies satisfied?
  → IF validation fails:
      ← Show error modal with detailed breakdown
  → IF validation succeeds:
      → Update session.status = 'completed'
      → Update session.completed_at = now()
      → Save to localStorage
      ← Show success modal with final stats
```

**Flow 7: Session Export**
```
User clicks "Export Session"
  → Read complete session from localStorage
  → Create export object:
      - Metadata (user_id, game_id, timestamps)
      - Full chat_logs
      - Full plan_history
      - Final current_plan
      - Metrics
      - Validation result
  → Generate JSON blob
  → Trigger browser download: nye-haedda-session-{user_id}-{game_id}.json
  ← User receives file (can submit for coursework)
```

**Flow 8: Renegotiation**
```
User clicks "Renegotiate" on WBS item 1.3.1
  → Add uncommit action to session.plan_history (localStorage)
  → Delete session.current_plan["1.3.1"] (localStorage)
  → Increment session.metrics.renegotiation_count
  → Recalculate metrics
  → Save session to localStorage
  ← Reopen chat (chat_logs preserved, can reference earlier conversation)
```

---

### 3.4 Backend API (Minimal - 3 Endpoints)

**Endpoint 1: AI Chat**
```python
@app.post("/api/chat/message")
async def chat_message(request: ChatRequest):
    """
    Stateless endpoint: Frontend sends all context
    Returns AI response based on supplier persona
    """
    # Input validation
    if not request.supplier or not request.wbs_item:
        raise HTTPException(400, "Missing required fields")

    # Load requirements/project docs (static files on server)
    requirements = load_requirements_spec()
    wbs_context = load_wbs_context()

    # Construct prompt with supplier persona
    prompt = build_negotiation_prompt(
        supplier=request.supplier,
        wbs_item=request.wbs_item,
        chat_history=request.chat_history,
        user_message=request.user_message,
        requirements=requirements,
        wbs_context=wbs_context
    )

    # Call Gemini API
    ai_response = await gemini_client.generate(prompt)

    # Extract structured offer (regex or LLM)
    offer = extract_offer(ai_response)

    return {
        "response": ai_response,
        "offer": offer,  # {cost: 105, duration: 2.5} or null
        "timestamp": datetime.now().isoformat()
    }
```

**Endpoint 2: Plan Validation (Optional - Can Be Client-Side)**
```python
@app.post("/api/validate")
async def validate_plan(request: ValidationRequest):
    """
    Validates plan against constraints
    Optional: Can be done client-side for MVP
    """
    current_plan = request.current_plan
    wbs_items = request.wbs_items

    errors = []
    warnings = []

    # Budget validation
    total_cost = sum(entry['cost'] for entry in current_plan.values())
    if total_cost > 700:
        errors.append({
            "type": "budget",
            "message": f"Budget exceeded by {total_cost - 700} MNOK"
        })

    # Timeline validation (critical path)
    end_date = calculate_critical_path(current_plan, wbs_items)
    if end_date > datetime(2026, 5, 15):
        errors.append({
            "type": "timeline",
            "message": f"Project delayed until {end_date.date()}"
        })

    # Dependency validation
    # ... check all dependencies

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

**Endpoint 3: Health Check**
```python
@app.get("/api/health")
async def health_check():
    """Simple health check"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
```

**That's it! Only 2-3 endpoints needed.**

---

### 3.5 Static Data Files

**File 1: `/public/data/wbs.json`**
- Contains all 15 WBS items from wbs.pdf
- Loaded by frontend on session initialization
- ~5-10 KB file size

**File 2: `/public/data/suppliers.json`**
- Contains 5-10 supplier personas
- Includes system_prompt and hidden_params
- ~20-30 KB file size

**File 3: `/public/data/requirements.json`** (Optional)
- Extracted requirements from krav-spec.pdf
- Used by backend to inject context into AI prompts
- Can also just include in suppliers.json

**File 4: `/public/docs/wbs.pdf`**
- Original WBS document

**File 5: `/public/docs/krav-spec.pdf`**
- Requirements specification

**File 6: `/public/docs/project-description.pdf`**
- Project description

---

### 3.6 UI Component Inventory

**Pages (3):**
1. `/login` - Authentication
2. `/dashboard` - Main game view (WBS, metrics, actions)
3. `/negotiate` - Chat interface

**Components (~15 total):**

**Dashboard Page:**
- Header (logo, user menu, logout)
- ConstraintPanel (budget meter, timeline, deadline)
- QuickStats (WBS completion, negotiations count)
- WBSList (tree/list of all WBS items)
  - WBSItem (individual item with status, details)
- ActionButtons (Submit Plan, Export, Help)

**Negotiate Page:**
- ChatHeader (supplier info, WBS context)
- ChatWindow (message list)
  - UserMessage (right-aligned bubble)
  - AIMessage (left-aligned bubble)
  - SystemMessage (center, small)
- ChatInput (text area, send button)
- OfferCard (highlights AI offers with Accept button)
- DocumentSidebar (links to PDFs)

**Modals:**
- SupplierSelectionModal (choose supplier for WBS item)
- CommitConfirmationModal (confirm quote acceptance)
- SubmissionResultModal (success/failure after validation)
- ExportModal (export options)

---

### 3.7 Technology Stack (Final)

**Frontend:**
- Framework: React (with Next.js App Router)
- Language: TypeScript
- Styling: Tailwind CSS + Shadcn UI
- State: localStorage + React Context (for UI state)
- Routing: Next.js router

**Backend:**
- Framework: FastAPI (Python)
- AI: Gemini 2.5 Pro/Flash via PydanticAI
- Hosting: Vercel (serverless functions)

**Authentication:**
- Supabase Auth (JWT tokens)

**Storage:**
- Active session: localStorage (browser)
- Static data: JSON files in `/public/data/`
- Documents: PDFs in `/public/docs/`
- Optional cloud backup: Supabase Storage (Should-Have)

**Deployment:**
- Frontend + Backend: Vercel
- Static assets: Vercel CDN

---

## 4. Key Themes & Insights

### Key Themes:

1. **Radical Simplification Enables Speed:**
   - Removing database reduces MVP timeline by 1-2 weeks
   - localStorage is sufficient for 45-60 minute single-session use case
   - Stateless backend (just AI orchestration) is much simpler

2. **Export-First Design:**
   - Full session export provides portfolio artifacts
   - Students can submit exported JSON for coursework
   - Instructors can analyze exported sessions manually (no dashboard needed for MVP)

3. **Client-Side Ownership:**
   - Frontend owns all data management (localStorage CRUD)
   - Backend is a thin AI proxy layer
   - Validation can be client-side (faster feedback)

4. **Static Data is Powerful:**
   - WBS and supplier personas don't change during gameplay
   - JSON files are easy to edit and version control
   - No database migrations needed when tweaking supplier prompts

5. **History Tracking is Key:**
   - plan_history array captures every change
   - Full chat_logs preserve all negotiation context
   - This enables rich export and future analytics

### Insights & Learnings:

1. **localStorage is Underrated:**
   - 5-10 MB storage limit is more than enough (session is ~500 KB)
   - Persists across page refreshes and browser restarts (same session)
   - Only risk: User clearing cache (rare during 1-hour session)

2. **Stateless Backend is Liberating:**
   - No session management on server
   - No database connection pooling/management
   - Easy to scale (each request is independent)
   - Cheaper hosting (no persistent connections)

3. **Export Solves Cross-Device Problem:**
   - Instead of syncing via database, user downloads JSON
   - Can email themselves, import on different device
   - "Should-Have" cloud sync adds convenience but isn't critical

4. **MVP Effort Estimate: 3-4 Weeks (Down from 5)**
   - Removing database saves: Schema design, migrations, CRUD endpoints, testing
   - Backend is just 2 endpoints (chat, optional validation)
   - Frontend complexity unchanged (same UI components)

5. **The Architecture is "Good Enough" and Upgradeable:**
   - If later we need cross-device sync: Add Supabase Storage upload
   - If later we need instructor dashboard: Add database tables, import JSON sessions
   - If later we need analytics: Parse exported JSON files
   - The localStorage foundation doesn't block future enhancements

---

## 5. Action Plan

### Priority 1: Static Data Preparation (Week 1)
- **Tasks:**
  1. Extract all WBS items from wbs.pdf into `/public/data/wbs.json`
  2. Define 5-10 supplier personas in `/public/data/suppliers.json`
  3. Write initial system_prompt for each supplier (prompt engineering)
  4. Add project documents to `/public/docs/` folder
- **Effort:** 2-3 days

### Priority 2: Backend Development (Week 1-2)
- **Tasks:**
  1. Set up FastAPI project
  2. Integrate PydanticAI + Gemini API
  3. Implement `/api/chat/message` endpoint
  4. Test prompt engineering (quality, response time)
  5. Deploy to Vercel
- **Effort:** 3-4 days

### Priority 3: Frontend Foundation (Week 2)
- **Tasks:**
  1. Set up Next.js + React + Tailwind + Shadcn
  2. Implement Supabase Auth (login, register)
  3. Create localStorage utilities (save/load session)
  4. Build Dashboard layout
  5. Build WBS list component
- **Effort:** 4-5 days

### Priority 4: Chat Interface (Week 3)
- **Tasks:**
  1. Build chat UI components
  2. Integrate with backend `/api/chat/message`
  3. Implement message logging to localStorage
  4. Add offer extraction and "Accept" button
  5. Document sidebar
- **Effort:** 4-5 days

### Priority 5: Plan Management & Validation (Week 3-4)
- **Tasks:**
  1. Implement commitment logic (update localStorage)
  2. Build critical path calculation (timeline)
  3. Implement validation function
  4. Build submission flow (success/error modals)
  5. Build renegotiation flow
- **Effort:** 4-5 days

### Priority 6: Export & Polish (Week 4)
- **Tasks:**
  1. Implement session export (JSON download)
  2. Add loading states and error handling
  3. Test full user flow end-to-end
  4. Bug fixes
  5. User acceptance testing
- **Effort:** 3-4 days

### Priority 7: Deployment & Testing (Week 4)
- **Tasks:**
  1. Deploy to Vercel production
  2. Test with 5-10 real LOG565 students
  3. Gather feedback
  4. Iterate on AI prompts based on feedback
- **Effort:** 2-3 days

**Total: 3-4 weeks for MVP**

---

## 6. Session Reflection

### What Worked Well:

1. **Questioning Database Necessity:**
   - User's question "Do we really need a database?" forced critical thinking
   - Led to much simpler, faster architecture
   - localStorage is perfect fit for this use case

2. **localStorage Schema Design:**
   - Comprehensive schema captures all necessary data
   - Separation of chat_logs, plan_history, current_plan is clean
   - Easy to serialize/deserialize (JSON)

3. **Export-First Mindset:**
   - Solves portfolio requirement
   - Solves instructor review requirement (manually)
   - Solves analytics requirement (parse JSON files)
   - Defers need for database/dashboards

4. **Stateless Backend:**
   - Extremely simple to implement and test
   - No session management complexity
   - Easy to scale and deploy

### Areas for Further Exploration:

1. **localStorage Size Limits:**
   - Need to test: What if user has very long chat (100+ messages)?
   - Typical session: ~500 KB (well under 5 MB limit)
   - Mitigation: Truncate very old messages if needed

2. **Critical Path Algorithm:**
   - Need robust implementation for timeline calculation
   - Library: Use existing algorithm (topological sort + longest path)
   - Fallback: If too complex, simplify to sequential sum

3. **AI Offer Extraction:**
   - How to reliably extract structured offers from AI text?
   - Option A: Regex (fast but brittle)
   - Option B: Ask Gemini to return structured JSON
   - Option C: Second LLM call to extract (slow but accurate)
   - Recommendation: Option B (Gemini supports structured output)

4. **Cloud Backup Strategy (Should-Have):**
   - When to implement? After MVP if users request it
   - Simple: Upload JSON to Supabase Storage
   - Complex: Real-time sync (probably overkill)

### New Questions That Arose:

1. **What if user wants to review previous sessions?**
   - Solution: Archive completed sessions in localStorage
   - Key pattern: `nye-haedda-archive-{user_id}-{game_id}`
   - Show list of archived sessions, allow reload

2. **How to handle localStorage quota exceeded?**
   - Error handling: Catch QuotaExceededError
   - Mitigation: Prompt user to export and clear old sessions
   - Unlikely in practice (sessions are small)

3. **Should we validate on every commitment or only on submission?**
   - Recommendation: Both
   - Soft validation (warnings) after each commitment
   - Hard validation (errors) on submission

4. **How to prevent cheating (editing localStorage manually)?**
   - Not a concern for MVP (honor system)
   - Mitigation: Exported JSON includes timestamps (instructors can spot anomalies)
   - Future: Add cryptographic signature to export

---

## 7. Summary

### MVP Scope (3-4 Weeks)

**Must Have (15 features):**
1. User Auth (Supabase)
2. Session Initialization (localStorage)
3. Dashboard (metrics, WBS list)
4. WBS View
5. Supplier Directory
6. Chat Interface
7. AI Integration (Gemini via FastAPI)
8. Quote Acceptance
9. Plan Validation
10. Submission & Win/Loss
11. Session Export (JSON)
12. Renegotiation
13. Document Access
14. Session Persistence
15. Error Handling

**Storage:**
- localStorage for active session
- No database tables
- JSON export for persistence

**Backend:**
- 2-3 endpoints (chat, optional validation, health)
- Stateless (no session management)
- Minimal complexity

**Tech Stack:**
- Frontend: React + Next.js + Tailwind + Shadcn
- Backend: FastAPI + PydanticAI + Gemini
- Auth: Supabase Auth only
- Hosting: Vercel

**Development Time:**
- Week 1: Static data + backend
- Week 2: Frontend foundation
- Week 3: Chat + plan management
- Week 4: Polish + testing + deployment

**Total: 3-4 weeks vs. 5 weeks with database**

---

*Report generated by the BMAD system.*
*Next step: Update project-plan.md and proceed to Phase 1 (PRD creation).*
