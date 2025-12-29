from __future__ import annotations

# ---- Standard library ----
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---- Third-party ----
import requests
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from supabase import Client, create_client

# NOTE: These are currently not used in your file, but kept to avoid changing behavior
from jose import JWTError, jwk, jwt  # noqa: F401

# ---- Local imports ----
from config import settings
from prompts.agent_prompts import get_agent_name, get_agent_prompt, get_agent_type
from services.critical_path_service import calculate_critical_path
from services.gemini_service import get_gemini_service


# =============================================================================
# Fail-fast config check (so we don't crash later in a weird place)
# =============================================================================

def _require_env() -> None:
    missing = []
    if not getattr(settings, "SUPABASE_URL", None):
        missing.append("SUPABASE_URL")
    if not getattr(settings, "SUPABASE_ANON_KEY", None):
        missing.append("SUPABASE_ANON_KEY")

    if missing:
        raise RuntimeError(
            "Missing required Supabase config: "
            + ", ".join(missing)
            + ".\nFix config.py so it loads env vars (e.g. from backend/.env.local) before creating settings."
        )


_require_env()


# =============================================================================
# Supabase & Authentication
# =============================================================================

# Initialize Supabase client (service-level client)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Bearer token scheme
auth_scheme = HTTPBearer()

# In-memory cache for JWKS with a simple expiry
jwks_cache: Dict[str, Any] = {"keys": None, "expiry": 0}
JWKS_CACHE_TTL = 600  # 10 minutes


def get_jwks() -> Dict[str, Any]:
    """Fetch and cache the JSON Web Key Set (JWKS) from Supabase."""
    now = time.time()
    if jwks_cache["keys"] and jwks_cache["expiry"] > now:
        return jwks_cache["keys"]

    jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

    try:
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()

        jwks = response.json()
        jwks_cache["keys"] = jwks
        jwks_cache["expiry"] = now + JWKS_CACHE_TTL
        return jwks

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch JWKS: {e}")


# =============================================================================
# Dependencies
# =============================================================================

def get_db_client(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Client:
    """
    Create a new Supabase client authenticated with the user's JWT.
    Ensures RLS policies apply correctly on DB operations.
    """
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    client.postgrest.auth(token.credentials)
    return client


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Dict[str, Any]:
    """
    Validate the JWT token using Supabase Auth API via supabase-py.

    NOTE: This makes a network call to Supabase Auth.
    """
    try:
        user_response = supabase.auth.get_user(token.credentials)

        if not user_response or not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid token: User not found")

        user = user_response.user
        return {"id": user.id, "email": user.email, "role": user.role}

    except HTTPException:
        raise
    except Exception as e:
        # keep behavior close to your existing code
        print(f"Auth Error (Supabase Client): {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# =============================================================================
# Pydantic Models
# =============================================================================

class ConversationMessage(BaseModel):
    role: str  # "user" or "agent"
    content: str


class ChatRequest(BaseModel):
    session_id: str
    agent_id: str
    message: str
    conversation_history: List[ConversationMessage] = []
    game_context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    agent_id: str
    agent_name: str
    response: str
    timestamp: str
    is_disagreement: bool = False


class CreateSessionRequest(BaseModel):
    total_budget: float = 700_000_000.00
    locked_budget: float = 390_000_000.00
    available_budget: float = 310_000_000.00


class SessionResponse(BaseModel):
    id: str
    user_id: str
    total_budget: float
    locked_budget: float
    available_budget: float
    current_budget_used: float
    budget_tier1_percentage: Optional[float]
    budget_tier3_total: Optional[float]
    budget_remaining: Optional[float]
    deadline_date: str
    status: str
    created_at: str
    updated_at: str


class CreateCommitmentRequest(BaseModel):
    wbs_id: str
    wbs_name: str
    agent_id: str
    baseline_cost: float
    negotiated_cost: float
    committed_cost: float
    baseline_duration: float
    negotiated_duration: float
    committed_duration: float
    quality_level: Optional[str] = None


class CommitmentResponse(BaseModel):
    id: str
    session_id: str
    wbs_id: str

    committed_cost: float
    committed_duration: float
    baseline_cost: float
    baseline_duration: float
    quality_level: Optional[str] = None

    savings: Optional[float]
    savings_percentage: Optional[float]
    created_at: str
    updated_session: Optional[SessionResponse] = None

    # optional fields present in DB sometimes
    wbs_name: Optional[str] = None
    wbs_category: Optional[str] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    negotiated_cost: Optional[float] = None
    negotiated_duration: Optional[float] = None
    status: Optional[str] = None
    user_reasoning: Optional[str] = None
    scope_changes: Optional[str] = None
    committed_at: Optional[str] = None
    updated_at: Optional[str] = None


class NegotiationHistoryRecord(BaseModel):
    id: str
    session_id: str
    agent_id: str
    agent_name: str
    agent_type: str
    user_message: str
    agent_response: str
    is_disagreement: bool
    contains_offer: bool
    offer_data: Optional[Dict[str, Any]] = None
    context_snapshot: Dict[str, Any]
    timestamp: str
    response_time_ms: Optional[int] = None
    sentiment: Optional[str] = None


class ValidationResponse(BaseModel):
    valid: bool
    earliest_start: Dict[str, str]
    earliest_finish: Dict[str, str]
    latest_start: Dict[str, str]
    latest_finish: Dict[str, str]
    slack: Dict[str, int]
    critical_path: List[str]
    projected_completion_date: str
    deadline: str
    meets_deadline: bool
    total_duration_days: int
    budget_valid: bool
    budget_used: float
    budget_remaining: float


class SnapshotResponse(BaseModel):
    id: str
    session_id: str
    version: int
    label: str
    snapshot_type: str
    budget_committed: int
    budget_available: int
    budget_total: int
    contract_wbs_id: Optional[str]
    contract_cost: Optional[int]
    contract_duration: Optional[int]
    contract_supplier: Optional[str]
    project_end_date: str
    days_before_deadline: int
    gantt_state: Dict[str, Any]
    precedence_state: Dict[str, Any]
    timestamp: str
    created_at: str


class SnapshotListResponse(BaseModel):
    snapshots: List[SnapshotResponse]
    total_count: int
    limit: int
    offset: int
    has_more: bool


# =============================================================================
# FastAPI App Initialization
# =============================================================================

app = FastAPI(
    title="My FastAPI Backend",
    description="A backend service with Supabase integration using JWKS.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Helpers
# =============================================================================

def detect_disagreement(ai_response: str) -> bool:
    disagreement_keywords = [
        "dessverre",
        "det går ikke",
        "for lavt",
        "urealistisk",
        "kan ikke godta",
        "må avslå",
        "det er for",
        "vi kan ikke",
        "ikke mulig",
    ]
    response_lower = ai_response.lower()
    return any(keyword in response_lower for keyword in disagreement_keywords)


def _wbs_json_path() -> Path:
    # Always resolve relative to this file (backend/main.py)
    return Path(__file__).parent / "data" / "wbs.json"


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI backend with Supabase!"}


@app.get("/me", tags=["Users"])
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_agent(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        valid_agents = ["anne-lise-berg", "bjorn-eriksen", "kari-andersen", "per-johansen"]
        if request.agent_id not in valid_agents:
            raise HTTPException(
                status_code=400,
                detail=f"Ugyldig agent_id. Må være en av: {', '.join(valid_agents)}",
            )

        try:
            system_prompt = get_agent_prompt(request.agent_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        gemini_service = get_gemini_service()

        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

        ai_response = await gemini_service.chat_with_agent(
            agent_id=request.agent_id,
            system_prompt=system_prompt,
            user_message=request.message,
            conversation_history=conversation_history,
            game_context=request.game_context,
        )

        is_disagreement = detect_disagreement(ai_response)
        timestamp = datetime.utcnow().isoformat()

        try:
            db.table("negotiation_history").insert(
                {
                    "session_id": request.session_id,
                    "agent_id": request.agent_id,
                    "agent_name": get_agent_name(request.agent_id),
                    "agent_type": get_agent_type(request.agent_id),
                    "user_message": request.message,
                    "agent_response": ai_response,
                    "is_disagreement": is_disagreement,
                    "context_snapshot": request.game_context or {},
                    "timestamp": timestamp,
                }
            ).execute()
        except Exception as db_error:
            print(f"Database error saving chat message: {db_error}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")

        return ChatResponse(
            agent_id=request.agent_id,
            agent_name=get_agent_name(request.agent_id),
            response=ai_response,
            timestamp=timestamp,
            is_disagreement=is_disagreement,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod under samtalen. Vennligst prøv igjen.")


# ---- Sessions ----

@app.get("/api/sessions", response_model=List[SessionResponse], tags=["Sessions"])
def get_user_sessions(
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        response = (
            db.table("game_sessions")
            .select("*")
            .eq("user_id", current_user["id"])
            .order("created_at", desc=True)
            .execute()
        )
        return [SessionResponse(**session) for session in response.data]
    except Exception as e:
        print(f"Error fetching user sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av økter")


@app.post("/api/sessions", response_model=SessionResponse, tags=["Sessions"])
def create_session(
    request: CreateSessionRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_data = {
            "user_id": current_user["id"],
            "total_budget": request.total_budget,
            "locked_budget": request.locked_budget,
            "available_budget": request.available_budget,
            "current_budget_used": 0.00,
            "deadline_date": "2026-05-15",
            "status": "in_progress",
        }

        response = db.table("game_sessions").insert(session_data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Kunne ikke opprette spillsesjon")

        session = response.data[0]

        # --- Baseline snapshot creation logic ---
        try:
            import json

            with open(_wbs_json_path(), "r", encoding="utf-8") as f:
                wbs_data = json.load(f)

            wbs_items = wbs_data.get("wbs_elements", [])
            locked_wbs_items = [item for item in wbs_items if not item.get("is_negotiable", False)]

            locked_commitments_for_timeline = [
                {
                    "wbs_item_id": item["id"],
                    "duration": item.get("locked_duration", 0),
                    "cost": item.get("locked_cost", 0),
                }
                for item in locked_wbs_items
            ]

            baseline_timeline = calculate_critical_path(
                wbs_items=wbs_items,
                commitments=locked_commitments_for_timeline,
                start_date="2025-01-15",
                deadline="2026-05-15",
            )

            project_end_date = baseline_timeline.get("projected_completion_date", "2025-09-29")
            deadline_dt = datetime.strptime("2026-05-15", "%Y-%m-%d")
            project_dt = datetime.strptime(project_end_date, "%Y-%m-%d")
            days_before_deadline = (deadline_dt - project_dt).days

            baseline_budget_committed = int(request.locked_budget * 100)
            baseline_budget_available = int(request.available_budget * 100)
            baseline_budget_total = int(request.total_budget * 100)

            db.rpc(
                "create_baseline_snapshot",
                {
                    "p_session_id": session["id"],
                    "p_budget_committed": baseline_budget_committed,
                    "p_budget_available": baseline_budget_available,
                    "p_budget_total": baseline_budget_total,
                    "p_project_end_date": project_end_date,
                    "p_days_before_deadline": days_before_deadline,
                    "p_gantt_state": baseline_timeline,
                    "p_precedence_state": baseline_timeline,
                },
            ).execute()

        except Exception as baseline_snapshot_error:
            print(f"Warning: Could not create baseline snapshot: {baseline_snapshot_error}")
            import traceback
            traceback.print_exc()
        # --- End baseline snapshot creation logic ---

        return SessionResponse(**session)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating session: {str(e)}")


@app.get("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        response = (
            db.table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        return SessionResponse(**response.data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av spillsesjon")


@app.put("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def update_session(
    session_id: str,
    updates: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        existing = (
            db.table("game_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )

        if not existing.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        response = db.table("game_sessions").update(updates).eq("id", session_id).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="Kunne ikke oppdatere spillsesjon")

        return SessionResponse(**response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating session: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved oppdatering av spillsesjon")


# ---- Commitments ----

@app.post("/api/sessions/{session_id}/commitments", response_model=CommitmentResponse, tags=["Commitments"])
def create_commitment(
    session_id: str,
    request: CreateCommitmentRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_response = (
            db.table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )

        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        session = session_response.data
        current_budget_used = session["current_budget_used"]
        available_budget = session["available_budget"]

        valid_wbs = ["1.3.1", "1.3.2", "1.4.1"]
        if request.wbs_id not in valid_wbs:
            raise HTTPException(status_code=400, detail=f"Ugyldig WBS ID. Må være en av: {', '.join(valid_wbs)}")

        existing = (
            db.table("wbs_commitments")
            .select("id")
            .eq("session_id", session_id)
            .eq("wbs_id", request.wbs_id)
            .execute()
        )

        if existing.data:
            raise HTTPException(status_code=400, detail=f"WBS {request.wbs_id} er allerede forpliktet")

        new_budget_used = current_budget_used + request.committed_cost
        if new_budget_used > available_budget:
            remaining = available_budget - current_budget_used
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Budsjett overskredet. Gjenstående: {remaining:,.0f} NOK, "
                    f"Forsøk på forpliktelse: {request.committed_cost:,.0f} NOK"
                ),
            )

        agent_name = get_agent_name(request.agent_id)
        wbs_category_placeholder = "Bygging"

        commitment_data = {
            "session_id": session_id,
            "wbs_id": request.wbs_id,
            "wbs_name": request.wbs_name,
            "wbs_category": wbs_category_placeholder,
            "agent_id": request.agent_id,
            "agent_name": agent_name,
            "baseline_cost": request.baseline_cost,
            "negotiated_cost": request.negotiated_cost,
            "committed_cost": request.committed_cost,
            "baseline_duration": request.baseline_duration,
            "negotiated_duration": request.negotiated_duration,
            "committed_duration": request.committed_duration,
            "quality_level": request.quality_level,
        }

        commitment_response = db.table("wbs_commitments").insert(commitment_data).execute()
        if not commitment_response.data:
            raise HTTPException(status_code=500, detail="Kunne ikke opprette forpliktelse")

        db.table("game_sessions").update({"current_budget_used": new_budget_used}).eq("id", session_id).execute()

        # Auto-create contract snapshot
        try:
            import json

            budget_committed = int(new_budget_used * 100)
            budget_available_ore = int((available_budget - new_budget_used) * 100)
            contract_cost = int(request.committed_cost * 100)

            supplier_map = {
                "1.3.1": "Bjørn Eriksen AS",
                "1.3.2": "Kari Andersen AS",
                "1.4.1": "Per Johansen AS",
            }
            supplier = supplier_map.get(request.wbs_id, "Ukjent Leverandør")

            duration_days = request.committed_duration

            all_commitments_response = db.table("wbs_commitments").select("*").eq("session_id", session_id).execute()
            all_commitments = all_commitments_response.data if all_commitments_response.data else []

            with open(_wbs_json_path(), "r", encoding="utf-8") as f:
                wbs_data = json.load(f)

            timeline = calculate_critical_path(
                wbs_items=wbs_data["wbs_elements"],
                commitments=[
                    {"wbs_item_id": c["wbs_id"], "duration": c.get("committed_duration", 0)}
                    for c in all_commitments
                ],
                start_date="2025-01-15",
                deadline="2026-05-15",
            )

            project_end_date = timeline.get("projected_completion_date", "2025-09-29")
            deadline_dt = datetime.strptime("2026-05-15", "%Y-%m-%d")
            project_dt = datetime.strptime(project_end_date, "%Y-%m-%d")
            days_before_deadline = (deadline_dt - project_dt).days

            db.rpc(
                "create_contract_snapshot",
                {
                    "p_session_id": session_id,
                    "p_wbs_id": request.wbs_id,
                    "p_cost": contract_cost,
                    "p_duration": duration_days,
                    "p_supplier": supplier,
                    "p_budget_committed": budget_committed,
                    "p_budget_available": budget_available_ore,
                    "p_project_end_date": project_end_date,
                    "p_days_before_deadline": days_before_deadline,
                    "p_gantt_state": timeline,
                    "p_precedence_state": timeline,
                },
            ).execute()

        except Exception as snapshot_error:
            print(f"Warning: Could not create contract snapshot: {snapshot_error}")
            import traceback
            traceback.print_exc()

        updated_session_response = db.table("game_sessions").select("*").eq("id", session_id).single().execute()
        updated_session = SessionResponse(**updated_session_response.data) if updated_session_response.data else None

        db_commitment = commitment_response.data[0]
        response_data = {
            "id": db_commitment["id"],
            "session_id": db_commitment["session_id"],
            "wbs_id": db_commitment["wbs_id"],
            "committed_cost": db_commitment["committed_cost"],
            "committed_duration": db_commitment["committed_duration"],
            "baseline_cost": db_commitment["baseline_cost"],
            "baseline_duration": db_commitment["baseline_duration"],
            "savings": db_commitment.get("savings"),
            "savings_percentage": db_commitment.get("savings_percentage"),
            "quality_level": db_commitment.get("quality_level"),
            "created_at": db_commitment["created_at"],
            "updated_session": updated_session,
        }

        return CommitmentResponse(**response_data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating commitment: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="En feil oppstod ved opprettelse av forpliktelse")


@app.get("/api/sessions/{session_id}/commitments", response_model=List[CommitmentResponse], tags=["Commitments"])
def get_commitments(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_response = (
            db.table("game_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        commitments_response = (
            db.table("wbs_commitments")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at")
            .execute()
        )
        return [CommitmentResponse(**c) for c in commitments_response.data]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching commitments: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av forpliktelser")


# ---- History ----

@app.get("/api/sessions/{session_id}/history", response_model=List[NegotiationHistoryRecord], tags=["Sessions"])
def get_negotiation_history(
    session_id: str,
    agent_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
) -> List[NegotiationHistoryRecord]:
    try:
        session_response = (
            db.table("game_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        query = db.table("negotiation_history").select("*").eq("session_id", session_id)
        if agent_id:
            query = query.eq("agent_id", agent_id)

        negotiation_response = query.order("timestamp").execute()
        return [NegotiationHistoryRecord(**msg) for msg in negotiation_response.data]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching negotiation history: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av samtalehistorikk")


# ---- Validation ----

@app.post("/api/sessions/{session_id}/validate", response_model=ValidationResponse, tags=["Validation"])
def validate_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    import json

    try:
        session_response = (
            db.table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        session = session_response.data

        with open(_wbs_json_path(), "r", encoding="utf-8") as f:
            wbs_data = json.load(f)

        wbs_items = wbs_data.get("wbs_elements", [])
        commitments_response = db.table("wbs_commitments").select("*").eq("session_id", session_id).execute()

        commitments = []
        for c in commitments_response.data:
            commitments.append(
                {
                    "wbs_item_id": c["wbs_id"],
                    "duration": c.get("committed_duration", 0),
                    "cost": c.get("committed_price", 0),  # kept as-is from your code
                }
            )

        timeline_result = calculate_critical_path(
            wbs_items=wbs_items,
            commitments=commitments,
            start_date="2025-01-15",
            deadline="2026-05-15",
        )

        budget_used = session.get("current_budget_used", 0)
        budget_remaining = session.get("total_budget", 700_000_000) - budget_used
        budget_valid = budget_used <= session.get("total_budget", 700_000_000)

        validation_result = {
            **timeline_result,
            "budget_valid": budget_valid,
            "budget_used": budget_used,
            "budget_remaining": budget_remaining,
            "valid": timeline_result["meets_deadline"] and budget_valid,
        }

        return ValidationResponse(**validation_result)

    except HTTPException:
        raise
    except FileNotFoundError:
        print("WBS data file not found")
        raise HTTPException(status_code=500, detail="WBS data kunne ikke lastes")
    except Exception as e:
        print(f"Error validating session: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"En feil oppstod ved validering: {str(e)}")


# ---- Snapshots ----

@app.get("/api/sessions/{session_id}/snapshots", response_model=SnapshotListResponse, tags=["Snapshots"])
def get_session_snapshots(
    session_id: str,
    limit: int = 5,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_response = (
            db.table("game_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        count_response = (
            db.table("session_snapshots")
            .select("id", count="exact")
            .eq("session_id", session_id)
            .execute()
        )
        total_count = count_response.count or 0

        snapshots_response = (
            db.table("session_snapshots")
            .select("*")
            .eq("session_id", session_id)
            .order("version", desc=True)
            .limit(limit)
            .range(offset, offset + limit - 1)
            .execute()
        )

        snapshots = [SnapshotResponse(**s) for s in snapshots_response.data]
        has_more = (offset + limit) < total_count

        return SnapshotListResponse(
            snapshots=snapshots,
            total_count=total_count,
            limit=limit,
            offset=offset,
            has_more=has_more,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching snapshots: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av snapshots")


@app.get("/api/sessions/{session_id}/snapshots/{version}", response_model=SnapshotResponse, tags=["Snapshots"])
def get_snapshot_by_version(
    session_id: str,
    version: int,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_response = (
            db.table("game_sessions")
            .select("id")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        snapshot_response = (
            db.table("session_snapshots")
            .select("*")
            .eq("session_id", session_id)
            .eq("version", version)
            .single()
            .execute()
        )
        if not snapshot_response.data:
            raise HTTPException(status_code=404, detail=f"Snapshot versjon {version} ikke funnet")

        return SnapshotResponse(**snapshot_response.data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching snapshot: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved henting av snapshot")


@app.get("/api/sessions/{session_id}/snapshots/export", tags=["Snapshots"])
def export_session_snapshots(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client),
):
    try:
        session_response = (
            db.table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .eq("user_id", current_user["id"])
            .single()
            .execute()
        )
        if not session_response.data:
            raise HTTPException(status_code=404, detail="Spillsesjon ikke funnet")

        snapshots_response = (
            db.table("session_snapshots")
            .select("*")
            .eq("session_id", session_id)
            .order("version")
            .execute()
        )

        export_data = {
            "session": session_response.data,
            "snapshots": snapshots_response.data,
            "export_timestamp": datetime.utcnow().isoformat(),
            "total_snapshots": len(snapshots_response.data),
        }
        return export_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error exporting snapshots: {str(e)}")
        raise HTTPException(status_code=500, detail="En feil oppstod ved eksport av snapshots")
