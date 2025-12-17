# MVP Completion Roadmap (REVISED)
## Nye Hædda Barneskole - Implementation Plan with ALL Requirements

**Created:** December 16, 2025
**Revision:** v2.0 (Updated with Gantt, Precedence, Tests, Chat Fix)
**Deadline:** December 17, 2025 (End of Day)
**Total Estimated Time:** 32-42 hours
**Status:** 🚨 CRITICAL - 7 must-have features + visualizations + tests required

---

## 🎯 REVISED EXECUTIVE SUMMARY

**Current State:** 8/15 PRD Must-Have features complete (53%)

**MUST IMPLEMENT (blocking MVP):**
1. ❌ Session completion flow with validation (4-6 hours)
2. ❌ Session export (JSON download) (3-4 hours)
3. ❌ Renegotiation (uncommit) capability (3-4 hours)
4. ❌ Chat history loading from DB (2 hours) **[REQUIRED]**
5. ❌ Gantt chart visualization using gantt-task-react (6-8 hours) **[REQUIRED]**
6. ❌ Precedence diagram using ReactFlow (6-8 hours) **[REQUIRED]**
7. ❌ Automated tests (8-10 hours) **[REQUIRED]**

**NICE TO HAVE (if time):**
- ⏸️ Mobile optimization (8-12 hours)
- ⏸️ Help documentation modal (1-2 hours)

**Total Required Effort:** 32-42 hours
**Team Recommendation:** 2-3 developers working in parallel

---

## 📅 IMPLEMENTATION STRATEGY

### Option A: Parallel Development (Recommended)
**Team of 3 developers:**
- **Developer 1:** Core flow (items 1-3) - 10-14 hours
- **Developer 2:** Visualizations using gantt-task-react + ReactFlow (items 5-6) - 12-16 hours
- **Developer 3:** Chat fix + Tests (items 4, 7) - 10-12 hours
- **Timeline:** 14-16 hours with coordination
- **Result:** Full MVP compliance

### Option B: Sequential (Single Developer)
**Minimum viable path:**
- Tonight: Core flow (10-14 hours)
- Tomorrow AM: Chat fix (2 hours)
- Tomorrow PM: Basic Gantt (4 hours) + Basic tests (4 hours)
- **Result:** Partial compliance, request extension for full completion

---

## 📋 DETAILED IMPLEMENTATION PLAN

## PRIORITY 1: CORE FLOW (10-14 hours)

### Task 1.1: Session Completion Flow with Validation (4-6 hours)

#### Backend Implementation (2-3 hours)

**File:** `backend/services/critical_path.py` (NEW)

```python
from datetime import datetime, timedelta
from typing import List, Dict

def calculate_critical_path(
    wbs_items: List[Dict],
    commitments: List[Dict],
    start_date: str = "2025-01-15"
) -> Dict:
    """
    Calculate critical path using Forward/Backward pass algorithm.

    Returns:
        {
            "projected_completion_date": "2026-05-10",
            "total_duration_days": 480,
            "critical_path": ["1.3.1", "1.3.2", "1.4.1"],
            "meets_deadline": True,
            "days_before_deadline": 5
        }
    """
    deadline = datetime.fromisoformat("2026-05-15")
    project_start = datetime.fromisoformat(start_date)

    # Build WBS lookup
    wbs_map = {item["id"]: item for item in wbs_items}
    commitment_map = {c["wbs_item_id"]: c for c in commitments}

    # Forward pass: Calculate ES and EF
    earliest_start = {}
    earliest_finish = {}

    def calc_earliest_start(wbs_id: str) -> datetime:
        if wbs_id in earliest_start:
            return earliest_start[wbs_id]

        wbs = wbs_map[wbs_id]
        dependencies = wbs.get("dependencies", [])

        if not dependencies:
            earliest_start[wbs_id] = project_start
        else:
            dep_finishes = [calc_earliest_finish(dep) for dep in dependencies]
            earliest_start[wbs_id] = max(dep_finishes)

        return earliest_start[wbs_id]

    def calc_earliest_finish(wbs_id: str) -> datetime:
        if wbs_id in earliest_finish:
            return earliest_finish[wbs_id]

        es = calc_earliest_start(wbs_id)

        # Get duration from commitment or baseline
        if wbs_id in commitment_map:
            duration_days = int(commitment_map[wbs_id]["committed_duration_days"])
        else:
            duration_days = int(wbs_map[wbs_id]["baseline_duration"])

        earliest_finish[wbs_id] = es + timedelta(days=duration_days)
        return earliest_finish[wbs_id]

    # Calculate for all tasks
    for wbs_id in wbs_map.keys():
        calc_earliest_finish(wbs_id)

    # Project completion = maximum EF
    projected_completion = max(earliest_finish.values())

    # Backward pass: Calculate LS and LF
    latest_finish = {}
    latest_start = {}

    # Initialize: All tasks must finish by project completion
    for wbs_id in wbs_map.keys():
        latest_finish[wbs_id] = projected_completion

    def calc_latest_finish(wbs_id: str) -> datetime:
        if wbs_id in latest_finish:
            return latest_finish[wbs_id]

        # Find all tasks that depend on this task
        successors = [
            task_id for task_id, task in wbs_map.items()
            if wbs_id in task.get("dependencies", [])
        ]

        if not successors:
            latest_finish[wbs_id] = projected_completion
        else:
            successor_starts = [calc_latest_start(succ) for succ in successors]
            latest_finish[wbs_id] = min(successor_starts)

        return latest_finish[wbs_id]

    def calc_latest_start(wbs_id: str) -> datetime:
        if wbs_id in latest_start:
            return latest_start[wbs_id]

        lf = calc_latest_finish(wbs_id)

        if wbs_id in commitment_map:
            duration_days = int(commitment_map[wbs_id]["committed_duration_days"])
        else:
            duration_days = int(wbs_map[wbs_id]["baseline_duration"])

        latest_start[wbs_id] = lf - timedelta(days=duration_days)
        return latest_start[wbs_id]

    # Calculate for all tasks
    for wbs_id in wbs_map.keys():
        calc_latest_start(wbs_id)

    # Identify critical path (slack = 0)
    critical_path = []
    for wbs_id in wbs_map.keys():
        slack = (latest_start[wbs_id] - earliest_start[wbs_id]).days
        if slack == 0:
            critical_path.append(wbs_id)

    total_duration = (projected_completion - project_start).days
    meets_deadline = projected_completion <= deadline
    days_diff = (deadline - projected_completion).days

    return {
        "projected_completion_date": projected_completion.isoformat(),
        "total_duration_days": total_duration,
        "critical_path": critical_path,
        "meets_deadline": meets_deadline,
        "days_before_deadline": days_diff,
        "deadline": deadline.isoformat(),
        "earliest_start": {k: v.isoformat() for k, v in earliest_start.items()},
        "earliest_finish": {k: v.isoformat() for k, v in earliest_finish.items()},
        "latest_start": {k: v.isoformat() for k, v in latest_start.items()},
        "latest_finish": {k: v.isoformat() for k, v in latest_finish.items()}
    }
```

**File:** `backend/main.py` (ADD ENDPOINT)

```python
from services.critical_path import calculate_critical_path

@app.post("/api/sessions/{session_id}/validate")
async def validate_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseClient = Depends(get_supabase_client)
):
    """Validate session against all constraints."""
    # Fetch session
    session_response = db.table("game_sessions").select("*").eq("id", session_id).eq("user_id", current_user["sub"]).execute()
    if not session_response.data:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_response.data[0]

    # Fetch commitments
    commitments_response = db.table("wbs_commitments").select("*").eq("session_id", session_id).execute()
    commitments = commitments_response.data

    # Load WBS data
    import json
    with open("../frontend/public/data/wbs.json") as f:
        wbs_data = json.load(f)

    errors = []
    warnings = []

    # Check 1: Completeness
    negotiable_wbs = [item for item in wbs_data["items"] if item.get("negotiable", False)]
    committed_wbs_ids = [c["wbs_item_id"] for c in commitments]
    missing_wbs = [item["id"] for item in negotiable_wbs if item["id"] not in committed_wbs_ids]

    if missing_wbs:
        errors.append({
            "type": "completeness",
            "message": f"Mangler WBS pakker: {', '.join(missing_wbs)}",
            "missing_count": len(missing_wbs),
            "missing_items": missing_wbs
        })

    # Check 2: Budget
    total_budget = float(session["current_budget_used"]) + float(session["locked_budget"])
    if total_budget > 700.0:
        errors.append({
            "type": "budget",
            "message": f"Budsjett overskredet med {total_budget - 700.0:.2f} MNOK",
            "current": total_budget,
            "limit": 700.0,
            "overage": total_budget - 700.0
        })
    elif total_budget > 680.0:
        warnings.append({
            "type": "budget",
            "message": f"Budsjett på {(total_budget/700.0)*100:.1f}% kapasitet"
        })

    # Check 3: Timeline
    timeline_result = calculate_critical_path(wbs_data["items"], commitments)

    if not timeline_result["meets_deadline"]:
        errors.append({
            "type": "timeline",
            "message": f"Prosjekt forsinket til {timeline_result['projected_completion_date'][:10]}",
            "projected": timeline_result["projected_completion_date"],
            "deadline": "2026-05-15",
            "days_late": abs(timeline_result["days_before_deadline"])
        })
    elif timeline_result["days_before_deadline"] < 5:
        warnings.append({
            "type": "timeline",
            "message": f"Tidsplan har liten buffer: bare {timeline_result['days_before_deadline']} dager før deadline"
        })

    is_valid = len(errors) == 0

    # Update session if valid
    if is_valid:
        db.table("game_sessions").update({
            "status": "completed",
            "completed_at": "now()",
            "projected_completion_date": timeline_result["projected_completion_date"]
        }).eq("id", session_id).execute()

    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "session_id": session_id,
        "total_budget": total_budget,
        "committed_items": len(commitments),
        "timeline": timeline_result,
        "timestamp": datetime.utcnow().isoformat()
    }
```

#### Frontend Implementation (2-3 hours)

**File:** `frontend/components/validation-result-modal.tsx` (NEW)

```typescript
'use client'

interface ValidationError {
  type: string
  message: string
  current?: number
  limit?: number
  overage?: number
  days_late?: number
  missing_items?: string[]
}

interface ValidationResultModalProps {
  errors: ValidationError[]
  warnings: ValidationError[]
  onClose: () => void
}

export function ValidationResultModal({
  errors,
  warnings,
  onClose
}: ValidationResultModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <h2 className="text-2xl font-bold text-red-600 mb-4">
          ❌ Validering Feilet
        </h2>

        <div className="space-y-4 mb-6">
          {errors.map((error, idx) => (
            <div key={idx} className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-4 rounded">
              <p className="font-semibold text-red-800 dark:text-red-200 mb-2">
                {error.type === 'budget' && '💰 Budsjett Overskredet'}
                {error.type === 'completeness' && '📋 Manglende Pakker'}
                {error.type === 'timeline' && '⏰ Tidsfrist Overskredet'}
              </p>
              <p className="text-red-700 dark:text-red-300">{error.message}</p>

              {error.type === 'budget' && error.overage && (
                <div className="mt-3 text-sm space-y-1">
                  <p className="font-medium">Du må redusere kostnadene med <strong>{error.overage.toFixed(2)} MNOK</strong></p>
                  <p className="text-gray-600 dark:text-gray-400">
                    💡 Forslag: Reforhandle de dyreste pakkene eller fjern scope med eier
                  </p>
                </div>
              )}

              {error.type === 'completeness' && error.missing_items && (
                <div className="mt-3 text-sm">
                  <p className="font-medium">Manglende pakker:</p>
                  <ul className="list-disc list-inside text-gray-700 dark:text-gray-300">
                    {error.missing_items.map(item => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}

              {error.type === 'timeline' && error.days_late && (
                <div className="mt-3 text-sm">
                  <p className="font-medium">{error.days_late} dager for sent</p>
                  <p className="text-gray-600 dark:text-gray-400">
                    💡 Forslag: Forhandel kortere leveringstid eller fjern avhengigheter
                  </p>
                </div>
              )}
            </div>
          ))}

          {warnings.length > 0 && (
            <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 p-4 rounded">
              <p className="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">⚠️ Advarsler</p>
              <ul className="space-y-1">
                {warnings.map((warning, idx) => (
                  <li key={idx} className="text-yellow-700 dark:text-yellow-300 text-sm">
                    {warning.message}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <button
          onClick={onClose}
          className="w-full bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-semibold transition"
        >
          Tilbake til Planlegging
        </button>
      </div>
    </div>
  )
}
```

**File:** `frontend/components/success-modal.tsx` (NEW)

```typescript
'use client'

interface SuccessModalProps {
  sessionId: string
  totalBudget: number
  committedItems: number
  projectedCompletion: string
  daysBeforeDeadline: number
  onExport: () => void
  onNewGame: () => void
}

export function SuccessModal({
  sessionId,
  totalBudget,
  committedItems,
  projectedCompletion,
  daysBeforeDeadline,
  onExport,
  onNewGame
}: SuccessModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-8 max-w-2xl w-full mx-4">
        <h2 className="text-3xl font-bold text-green-600 mb-4">
          🎉 Plan Godkjent!
        </h2>

        <div className="space-y-4 mb-6">
          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <p className="text-lg mb-2">
              <strong>Total Kostnad:</strong> {totalBudget.toFixed(2)} MNOK
              <span className="text-green-600 dark:text-green-400 ml-2 font-semibold">
                (innenfor 700 MNOK budsjett)
              </span>
            </p>
            <p className="text-lg">
              <strong>Ferdigstillelse:</strong> {new Date(projectedCompletion).toLocaleDateString('nb-NO')}
              <span className="text-green-600 dark:text-green-400 ml-2 font-semibold">
                ({daysBeforeDeadline} dager før deadline)
              </span>
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">WBS Pakker</p>
              <p className="text-3xl font-bold">{committedItems}/15</p>
            </div>

            <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg text-center">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Status</p>
              <p className="text-2xl font-bold text-green-600">✓ Godkjent</p>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onExport}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition"
          >
            📥 Eksporter Økt
          </button>

          <button
            onClick={onNewGame}
            className="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 px-6 py-3 rounded-lg font-semibold transition"
          >
            🆕 Start Ny Økt
          </button>
        </div>
      </div>
    </div>
  )
}
```

**File:** `frontend/app/dashboard/page.tsx` (MODIFY)

Add submit button and validation logic:

```typescript
const [showSuccessModal, setShowSuccessModal] = useState(false)
const [showErrorModal, setShowErrorModal] = useState(false)
const [validationResult, setValidationResult] = useState<any>(null)

const handleSubmitPlan = async () => {
  const token = ... // get JWT token

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/validate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const result = await response.json()
  setValidationResult(result)

  if (result.valid) {
    setShowSuccessModal(true)
  } else {
    setShowErrorModal(true)
  }
}

// In JSX:
<button
  onClick={handleSubmitPlan}
  disabled={committedCount < 3}
  className={`px-6 py-3 rounded-lg font-semibold transition ${
    committedCount < 3
      ? 'bg-gray-300 cursor-not-allowed'
      : 'bg-green-600 hover:bg-green-700 text-white'
  }`}
>
  {committedCount < 3 ? '⏳ Fullfør alle 3 pakker først' : '✅ Send Inn Plan'}
</button>

{showSuccessModal && validationResult && (
  <SuccessModal
    sessionId={sessionId}
    totalBudget={validationResult.total_budget}
    committedItems={validationResult.committed_items}
    projectedCompletion={validationResult.timeline.projected_completion_date}
    daysBeforeDeadline={validationResult.timeline.days_before_deadline}
    onExport={handleExport}
    onNewGame={handleNewGame}
  />
)}

{showErrorModal && validationResult && (
  <ValidationResultModal
    errors={validationResult.errors}
    warnings={validationResult.warnings}
    onClose={() => setShowErrorModal(false)}
  />
)}
```

---

### Task 1.2: Session Export (3-4 hours)

**File:** `backend/main.py` (ADD ENDPOINT)

```python
@app.get("/api/sessions/{session_id}/export")
async def export_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseClient = Depends(get_supabase_client)
):
    """Export complete session as JSON for coursework submission."""
    # Fetch session
    session_response = db.table("game_sessions").select("*").eq("id", session_id).eq("user_id", current_user["sub"]).execute()
    if not session_response.data:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_response.data[0]

    # Fetch commitments
    commitments_response = db.table("wbs_commitments").select("*").eq("session_id", session_id).order("created_at").execute()
    commitments = commitments_response.data

    # Fetch negotiation history
    history_response = db.table("negotiation_history").select("*").eq("session_id", session_id).order("created_at").execute()
    chat_logs = history_response.data

    # Load reference data
    import json
    with open("../frontend/public/data/wbs.json") as f:
        wbs_data = json.load(f)
    with open("../frontend/public/data/agents.json") as f:
        agents_data = json.load(f)

    # Calculate timeline
    timeline_result = calculate_critical_path(wbs_data["items"], commitments)

    # Build export
    export_data = {
        # Metadata
        "export_version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "simulation_name": "Nye Hædda Barneskole PM Simulation",

        # Session info
        "session": {
            "id": session_id,
            "user_id": session["user_id"],
            "created_at": session["created_at"],
            "completed_at": session.get("completed_at"),
            "status": session["status"]
        },

        # Budget metrics
        "budget": {
            "total_limit": 700.0,
            "locked_budget": float(session["locked_budget"]),
            "available_budget": float(session["available_budget"]),
            "used_budget": float(session["current_budget_used"]),
            "final_total": float(session["current_budget_used"]) + float(session["locked_budget"]),
            "budget_percentage": ((float(session["current_budget_used"]) + float(session["locked_budget"])) / 700.0) * 100
        },

        # Timeline
        "timeline": {
            "deadline": "2026-05-15",
            "projected_completion": timeline_result["projected_completion_date"],
            "meets_deadline": timeline_result["meets_deadline"],
            "days_before_deadline": timeline_result["days_before_deadline"],
            "total_duration_days": timeline_result["total_duration_days"],
            "critical_path": timeline_result["critical_path"]
        },

        # Commitments
        "commitments": [
            {
                "wbs_item_id": c["wbs_item_id"],
                "agent_id": c["agent_id"],
                "baseline_cost": float(c["baseline_cost"]),
                "committed_cost": float(c["committed_cost"]),
                "baseline_duration": float(c["baseline_duration_days"]),
                "committed_duration": float(c["committed_duration_days"]),
                "cost_savings": float(c.get("cost_savings", 0)),
                "quality_level": c.get("quality_level"),
                "committed_at": c["created_at"]
            }
            for c in commitments
        ],

        # Negotiation history
        "negotiation_history": [
            {
                "id": msg["id"],
                "agent_id": msg["agent_id"],
                "wbs_item_id": msg.get("wbs_item_id"),
                "user_message": msg["user_message"],
                "agent_response": msg["agent_response"],
                "disagreement": msg.get("disagreement", False),
                "timestamp": msg["created_at"]
            }
            for msg in chat_logs
        ],

        # Statistics
        "statistics": {
            "total_negotiations": len(chat_logs),
            "total_commitments": len(commitments),
            "negotiable_items_completed": len([c for c in commitments if c.get("negotiable", True)]),
            "disagreement_count": sum(1 for msg in chat_logs if msg.get("disagreement")),
            "total_cost_savings": sum(float(c.get("cost_savings", 0)) for c in commitments)
        },

        # Reference data (for instructor review)
        "reference": {
            "wbs_items": wbs_data["items"],
            "agents": agents_data
        }
    }

    return JSONResponse(content=export_data)
```

**Frontend Export Handler:**

```typescript
const handleExport = async () => {
  const token = ... // get JWT token

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/export`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  const exportData = await response.json()

  // Create blob and download
  const blob = new Blob([JSON.stringify(exportData, null, 2)], {
    type: 'application/json'
  })

  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `nye-haedda-session-${sessionId}-${new Date().toISOString().split('T')[0]}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
```

---

### Task 1.3: Renegotiation (Uncommit) (3-4 hours)

**File:** `backend/main.py` (ADD ENDPOINT)

```python
@app.delete("/api/sessions/{session_id}/commitments/{wbs_item_id}")
async def uncommit_wbs_item(
    session_id: str,
    wbs_item_id: str,
    current_user: dict = Depends(get_current_user),
    db: SupabaseClient = Depends(get_supabase_client)
):
    """Remove commitment and recalculate budget. Preserves chat history."""
    # Verify session ownership
    session_response = db.table("game_sessions").select("*").eq("id", session_id).eq("user_id", current_user["sub"]).execute()
    if not session_response.data:
        raise HTTPException(status_code=404, detail="Session not found")

    session = session_response.data[0]

    # Find commitment
    commitment_response = db.table("wbs_commitments").select("*").eq("session_id", session_id).eq("wbs_item_id", wbs_item_id).execute()
    if not commitment_response.data:
        raise HTTPException(status_code=404, detail="Commitment not found")

    commitment = commitment_response.data[0]
    committed_cost = float(commitment["committed_cost"])

    # Delete commitment
    db.table("wbs_commitments").delete().eq("session_id", session_id).eq("wbs_item_id", wbs_item_id).execute()

    # Update session budget
    new_budget_used = float(session["current_budget_used"]) - committed_cost
    db.table("game_sessions").update({
        "current_budget_used": new_budget_used,
        "status": "in_progress"  # Reset to in_progress if was completed
    }).eq("id", session_id).execute()

    # Chat history is NOT deleted - preserved for continued negotiation

    return {
        "message": "Commitment removed successfully",
        "wbs_item_id": wbs_item_id,
        "uncommitted_cost": committed_cost,
        "new_budget_used": new_budget_used
    }
```

**File:** `frontend/components/uncommit-modal.tsx` (NEW)

```typescript
'use client'

interface UncommitModalProps {
  wbsItem: any
  commitment: any
  onConfirm: () => void
  onCancel: () => void
}

export function UncommitModal({
  wbsItem,
  commitment,
  onConfirm,
  onCancel
}: UncommitModalProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md">
        <h3 className="text-xl font-bold mb-4">🔄 Fjern Forpliktelse?</h3>

        <p className="text-gray-700 dark:text-gray-300 mb-4">
          Dette vil fjerne <strong>{wbsItem.name}</strong> fra planen din og
          redusere budsjettet med <strong>{commitment.committed_cost} MNOK</strong>.
        </p>

        <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
          💬 Samtalehistorikken blir bevart, så du kan fortsette forhandlingene.
        </p>

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 px-4 py-2 rounded-lg transition"
          >
            Avbryt
          </button>
          <button
            onClick={onConfirm}
            className="flex-1 bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg font-semibold transition"
          >
            Fjern Forpliktelse
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Add to WBS Card:**

```typescript
{commitment && (
  <>
    <button
      onClick={() => setShowUncommitModal(true)}
      className="text-orange-600 hover:text-orange-700 text-sm font-medium"
    >
      🔄 Reforhandle
    </button>

    {showUncommitModal && (
      <UncommitModal
        wbsItem={wbsItem}
        commitment={commitment}
        onConfirm={async () => {
          await fetch(`/api/sessions/${sessionId}/commitments/${wbsItem.id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
          })
          setShowUncommitModal(false)
          // Refresh data
          router.refresh()
        }}
        onCancel={() => setShowUncommitModal(false)}
      />
    )}
  </>
)}
```

---

## PRIORITY 2: CHAT HISTORY FIX (2 hours)

### Task 2.1: Load Chat History from Database

**File:** `frontend/components/chat-interface.tsx` (MODIFY)

```typescript
useEffect(() => {
  const loadChatHistory = async () => {
    const token = ... // get JWT token

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/history?agent_id=${agentId}&wbs_item_id=${wbsId}`,
      {
        headers: { 'Authorization': `Bearer ${token}` }
      }
    )

    if (response.ok) {
      const history = await response.json()

      // Convert to message format
      const messages = history.flatMap((entry: any) => [
        {
          id: `${entry.id}-user`,
          role: 'user',
          content: entry.user_message,
          timestamp: entry.created_at
        },
        {
          id: `${entry.id}-agent`,
          role: 'agent',
          content: entry.agent_response,
          timestamp: entry.created_at,
          disagreement: entry.disagreement
        }
      ])

      setMessages(messages)
    }
  }

  loadChatHistory()
}, [sessionId, agentId, wbsId])
```

**Backend:** Endpoint already exists (`GET /api/sessions/{id}/history`)

---

## PRIORITY 3: VISUALIZATIONS (12-16 hours)

### Task 3.1: Gantt Chart (6-8 hours)

**Implementation Approach:** Using `gantt-task-react` library (30K+ weekly downloads) for pre-built Gantt chart functionality.

**File:** `frontend/components/gantt-chart.tsx` (NEW)

**Step 1: Install library**
```bash
npm install gantt-task-react
npm install --save-dev @types/gantt-task-react
```

**Step 2: Create Gantt component**

```typescript
'use client'

import { useMemo } from 'react'
import { Gantt, Task, ViewMode } from 'gantt-task-react'
import 'gantt-task-react/dist/index.css'

interface GanttChartProps {
  wbsItems: any[]
  commitments: any[]
  timeline: any // from validation endpoint
}

export function GanttChart({ wbsItems, commitments, timeline }: GanttChartProps) {
  const tasks: Task[] = useMemo(() => {
    const commitmentMap = Object.fromEntries(
      commitments.map(c => [c.wbs_item_id, c])
    )

    const earliestStart = timeline.earliest_start || {}
    const earliestFinish = timeline.earliest_finish || {}
    const criticalPath = timeline.critical_path || []

    return wbsItems
      .map(item => {
        const commitment = commitmentMap[item.id]
        const start = earliestStart[item.id] ? new Date(earliestStart[item.id]) : null
        const end = earliestFinish[item.id] ? new Date(earliestFinish[item.id]) : null

        if (!start || !end) return null

        const isCritical = criticalPath.includes(item.id)
        const isCommitted = !!commitment
        const isNegotiable = item.negotiable

        return {
          id: item.id,
          name: `${item.id} - ${item.name}`,
          start,
          end,
          progress: isCommitted ? 100 : 0,
          type: 'task' as const,
          styles: {
            backgroundColor: isCritical
              ? '#ef4444' // Red for critical path
              : isNegotiable
              ? '#22c55e' // Green for negotiable
              : '#9ca3af', // Gray for locked
            backgroundSelectedColor: isCritical ? '#dc2626' : isNegotiable ? '#16a34a' : '#6b7280',
            progressColor: isCritical ? '#991b1b' : isNegotiable ? '#15803d' : '#4b5563',
            progressSelectedColor: isCritical ? '#7f1d1d' : isNegotiable ? '#14532d' : '#374151'
          },
          dependencies: item.dependencies || []
        }
      })
      .filter((task): task is Task => task !== null)
  }, [wbsItems, commitments, timeline])

  // Set Norwegian locale and Month view by default
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold mb-4">Gantt Chart</h3>

      <div className="gantt-wrapper">
        <Gantt
          tasks={tasks}
          viewMode={ViewMode.Month}
          locale="nb-NO"
          listCellWidth="200px"
          columnWidth={60}
          barProgressColor="#3b82f6"
          barBackgroundColor="#e5e7eb"
          todayColor="rgba(59, 130, 246, 0.3)"
        />
      </div>

      {/* Legend */}
      <div className="mt-6 flex gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span>Kritisk sti</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span>Forhandlet</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-400 rounded"></div>
          <span>Låst</span>
        </div>
      </div>
    </div>
  )
}
```

**Step 3: Add custom CSS for styling** (optional, in `globals.css`)

```css
.gantt-wrapper {
  width: 100%;
  overflow-x: auto;
}

.gantt-wrapper .gantt {
  font-family: inherit;
}
```

**Benefits of gantt-task-react:**
- ✅ Pre-built timeline rendering (months, weeks, days)
- ✅ Auto-positioning of task bars
- ✅ Dependency arrows built-in
- ✅ Zoom and scroll interactions
- ✅ Today marker automatically displayed
- ✅ Saves 3-5 hours vs custom implementation

---

### Task 3.2: Precedence Diagram (6-8 hours)

**Implementation Approach:** Using `ReactFlow` library (500K+ weekly downloads) for AON network diagram with built-in graph layout.

**File:** `frontend/components/precedence-diagram.tsx` (NEW)

**Step 1: Install library**
```bash
npm install reactflow
```

**Step 2: Create Precedence Diagram component**

```typescript
'use client'

import { useMemo, useCallback } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from 'reactflow'
import 'reactflow/dist/style.css'

interface PrecedenceDiagramProps {
  wbsItems: any[]
  timeline: any
}

export function PrecedenceDiagram({ wbsItems, timeline }: PrecedenceDiagramProps) {
  const criticalPath = timeline.critical_path || []
  const earliestStart = timeline.earliest_start || {}
  const earliestFinish = timeline.earliest_finish || {}
  const latestStart = timeline.latest_start || {}
  const latestFinish = timeline.latest_finish || {}

  const initialNodes: Node[] = useMemo(() => {
    return wbsItems.map((item, idx) => {
      const es = earliestStart[item.id]
        ? Math.ceil((new Date(earliestStart[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0
      const ef = earliestFinish[item.id]
        ? Math.ceil((new Date(earliestFinish[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0
      const ls = latestStart[item.id]
        ? Math.ceil((new Date(latestStart[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0
      const lf = latestFinish[item.id]
        ? Math.ceil((new Date(latestFinish[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0
      const slack = ls - es
      const isCritical = criticalPath.includes(item.id)

      return {
        id: item.id,
        type: 'default',
        position: { x: (idx % 5) * 220 + 50, y: Math.floor(idx / 5) * 180 + 50 },
        data: {
          label: (
            <div className="text-center p-2">
              <div className="font-bold text-sm mb-1">{item.id}</div>
              <div className="text-xs mb-1 text-gray-700">
                {item.name.length > 20 ? item.name.substring(0, 20) + '...' : item.name}
              </div>
              <div className="text-xs text-gray-600 mt-2">
                <div>ES: {es} | EF: {ef}</div>
                <div>LS: {ls} | LF: {lf}</div>
              </div>
              <div className={`text-xs font-semibold mt-1 ${slack === 0 ? 'text-red-600' : 'text-green-600'}`}>
                {slack === 0 ? 'KRITISK' : `Slack: ${slack}d`}
              </div>
            </div>
          )
        },
        style: {
          background: isCritical ? '#fee2e2' : '#f3f4f6',
          border: `${isCritical ? '3' : '2'}px solid ${isCritical ? '#ef4444' : '#9ca3af'}`,
          borderRadius: '8px',
          width: 180,
          fontSize: '12px'
        }
      }
    })
  }, [wbsItems, timeline])

  const initialEdges: Edge[] = useMemo(() => {
    const edges: Edge[] = []
    wbsItems.forEach(item => {
      const dependencies = item.dependencies || []
      dependencies.forEach((depId: string) => {
        const isCritical =
          criticalPath.includes(item.id) && criticalPath.includes(depId)

        edges.push({
          id: `${depId}-${item.id}`,
          source: depId,
          target: item.id,
          type: 'smoothstep',
          animated: isCritical,
          style: {
            stroke: isCritical ? '#ef4444' : '#9ca3af',
            strokeWidth: isCritical ? 3 : 2
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: isCritical ? '#ef4444' : '#9ca3af'
          }
        })
      })
    })
    return edges
  }, [wbsItems, timeline])

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold mb-4">Precedence Diagram (AON)</h3>

      <div style={{ width: '100%', height: '600px' }} className="border border-gray-200 dark:border-gray-700 rounded">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-left"
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>

      {/* Legend */}
      <div className="mt-4 flex gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-12 h-8 bg-red-100 border-2 border-red-500 rounded"></div>
          <span>Kritisk sti</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-12 h-8 bg-gray-100 border-2 border-gray-400 rounded"></div>
          <span>Ikke-kritisk</span>
        </div>
        <div>
          <strong>ES</strong>=Tidligst start, <strong>EF</strong>=Tidligst slutt,
          <strong>LS</strong>=Senest start, <strong>LF</strong>=Senest slutt
        </div>
      </div>
    </div>
  )
}
```

**Benefits of ReactFlow:**
- ✅ Purpose-built for node-based diagrams (Activity-on-Node format)
- ✅ Auto-layout with drag-and-drop repositioning
- ✅ Built-in zoom, pan, fit-to-view controls
- ✅ Animated edges for critical path
- ✅ Smooth edge routing (no collision calculations needed)
- ✅ Saves 7-15 hours vs custom graph layout algorithms

**Add tabs to Dashboard:**

```typescript
const [activeTab, setActiveTab] = useState<'overview' | 'gantt' | 'precedence'>('overview')

// In JSX:
<div className="flex gap-2 mb-4">
  <button
    onClick={() => setActiveTab('overview')}
    className={activeTab === 'overview' ? 'tab-active' : 'tab'}
  >
    Oversikt
  </button>
  <button
    onClick={() => setActiveTab('gantt')}
    className={activeTab === 'gantt' ? 'tab-active' : 'tab'}
  >
    Gantt Chart
  </button>
  <button
    onClick={() => setActiveTab('precedence')}
    className={activeTab === 'precedence' ? 'tab-active' : 'tab'}
  >
    Precedensdiagram
  </button>
</div>

{activeTab === 'overview' && <DashboardOverview />}
{activeTab === 'gantt' && <GanttChart wbsItems={wbsItems} commitments={commitments} timeline={timeline} />}
{activeTab === 'precedence' && <PrecedenceDiagram wbsItems={wbsItems} timeline={timeline} />}
```

---

## PRIORITY 4: AUTOMATED TESTS (8-10 hours)

### Task 4.1: Backend Tests (4 hours)

**File:** `backend/tests/test_validation.py` (NEW)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validate_session_success():
    """Test successful validation."""
    # Create test session with valid data
    session_id = "test-session-123"

    response = client.post(
        f"/api/sessions/{session_id}/validate",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == True
    assert len(data["errors"]) == 0

def test_validate_session_over_budget():
    """Test validation fails when budget exceeded."""
    session_id = "test-session-over-budget"

    response = client.post(
        f"/api/sessions/{session_id}/validate",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == False
    assert any(e["type"] == "budget" for e in data["errors"])

def test_export_session():
    """Test session export."""
    session_id = "test-session-123"

    response = client.get(
        f"/api/sessions/{session_id}/export",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "export_version" in data
    assert "session" in data
    assert "budget" in data
    assert "commitments" in data
    assert "negotiation_history" in data

def test_uncommit_wbs_item():
    """Test uncommitting a WBS item."""
    session_id = "test-session-123"
    wbs_id = "1.3.1"

    response = client.delete(
        f"/api/sessions/{session_id}/commitments/{wbs_id}",
        headers={"Authorization": "Bearer test-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["wbs_item_id"] == wbs_id
    assert "uncommitted_cost" in data
    assert "new_budget_used" in data
```

### Task 4.2: Frontend Tests (4 hours)

**File:** `frontend/__tests__/dashboard.test.tsx` (NEW)

```typescript
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Dashboard from '@/app/dashboard/page'

describe('Dashboard', () => {
  it('displays budget correctly', () => {
    render(<Dashboard />)

    expect(screen.getByText(/310.*MNOK/i)).toBeInTheDocument()
    expect(screen.getByText(/700.*MNOK/i)).toBeInTheDocument()
  })

  it('shows submit button when 3 items committed', async () => {
    render(<Dashboard />)

    // Simulate 3 commitments
    // ...

    const submitButton = screen.getByText(/Send Inn Plan/i)
    expect(submitButton).toBeEnabled()
  })

  it('validates plan on submit', async () => {
    const user = userEvent.setup()
    render(<Dashboard />)

    const submitButton = screen.getByText(/Send Inn Plan/i)
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Plan Godkjent/i)).toBeInTheDocument()
    })
  })
})
```

---

## ✅ COMPLETION CHECKLIST

### Tonight (10-14 hours)
- [ ] Backend: critical_path.py service
- [ ] Backend: POST /api/sessions/{id}/validate
- [ ] Backend: GET /api/sessions/{id}/export
- [ ] Backend: DELETE /api/sessions/{id}/commitments/{wbs_id}
- [ ] Frontend: validation-result-modal.tsx
- [ ] Frontend: success-modal.tsx
- [ ] Frontend: uncommit-modal.tsx
- [ ] Frontend: Submit button + handlers
- [ ] Frontend: Export handler
- [ ] Testing: Core flow works end-to-end

### Tomorrow (14-18 hours)
- [ ] Frontend: Load chat history on mount
- [ ] Frontend: Install gantt-task-react and reactflow libraries
- [ ] Frontend: gantt-chart.tsx component (using gantt-task-react)
- [ ] Frontend: precedence-diagram.tsx component (using ReactFlow)
- [ ] Frontend: Dashboard tabs (overview/gantt/precedence)
- [ ] Backend: Test suite (validation, export, uncommit)
- [ ] Frontend: Test suite (dashboard, chat, modals)
- [ ] Integration testing: Full user journey
- [ ] Final testing: All features work

---

## 🚀 RECOMMENDED TEAM SPLIT

**Developer 1 (Backend Focus):**
- Critical path algorithm
- All 3 backend endpoints
- Backend tests
- ~12-14 hours

**Developer 2 (Frontend Core):**
- All modals (validation, success, uncommit)
- Submit button + logic
- Export handler
- Chat history loading
- ~8-10 hours

**Developer 3 (Frontend Visualizations):**
- Install gantt-task-react and reactflow libraries
- Gantt chart component (using gantt-task-react)
- Precedence diagram component (using ReactFlow)
- Dashboard tabs
- Frontend tests
- ~12-14 hours

**Total Team Time:** ~32-38 hours (parallelized to ~14-16 hours)

---

**Status:** Ready for implementation
**Next Step:** Assign tasks and begin development
**Goal:** MVP-ready by December 17 EOD
