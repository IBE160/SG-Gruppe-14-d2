import time
import requests
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from supabase import create_client, Client
from pydantic import BaseModel

from config import settings
from services.gemini_service import get_gemini_service
from services.critical_path_service import calculate_critical_path
from prompts.agent_prompts import get_agent_prompt, get_agent_name, get_agent_type

# --- Supabase & Authentication Setup ---

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Scheme for bearer token authentication
auth_scheme = HTTPBearer()

# In-memory cache for JWKS with a simple expiry
jwks_cache = {
    "keys": None,
    "expiry": 0
}
JWKS_CACHE_TTL = 600  # 10 minutes

def get_jwks():
    """
    Fetches and caches the JSON Web Key Set (JWKS) from Supabase.
    """
    now = time.time()
    if jwks_cache["keys"] and jwks_cache["expiry"] > now:
        return jwks_cache["keys"]

    try:
        jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"
        response = requests.get(jwks_url)
        response.raise_for_status()
        
        jwks = response.json()
        jwks_cache["keys"] = jwks
        jwks_cache["expiry"] = now + JWKS_CACHE_TTL
        return jwks
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Could not fetch JWKS: {e}")


# --- Dependencies ---

def get_db_client(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Client:
    """
    Creates a new Supabase client authenticated with the user's token.
    This ensures RLS policies are applied correctly for database operations.
    """
    client = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    client.postgrest.auth(token.credentials)
    return client

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Verifies the JWT token using the official Supabase client.
    Returns the user's data if the token is valid.
    """
    try:
        # Use the official Supabase client to verify the user
        # This makes a network call to Supabase Auth API to ensure the token is valid and not revoked
        user_response = supabase.auth.get_user(token.credentials)
        
        if not user_response or not user_response.user:
             raise HTTPException(status_code=401, detail="Invalid token: User not found")

        user = user_response.user
        
        # Construct the user dictionary expected by the endpoints
        return {
            "id": user.id, 
            "email": user.email, 
            "role": user.role
        }

    except Exception as e:
        print(f"Auth Error (Supabase Client): {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


# --- Pydantic Models ---

class ConversationMessage(BaseModel):
    """A single message in the conversation history"""
    role: str  # "user" or "agent"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    session_id: str
    agent_id: str
    message: str
    conversation_history: List[ConversationMessage] = []
    game_context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    agent_id: str
    agent_name: str
    response: str
    timestamp: str
    is_disagreement: bool = False


class CreateSessionRequest(BaseModel):
    """Request model for creating a new game session"""
    total_budget: float = 700_000_000.00
    locked_budget: float = 390_000_000.00
    available_budget: float = 310_000_000.00


class SessionResponse(BaseModel):
    """Response model for session data"""
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
    """Request model for creating a WBS commitment"""
    wbs_id: str  # "1.3.1", "1.3.2", or "1.4.1"
    committed_price: float
    committed_duration_weeks: int
    baseline_price: float
    baseline_duration_weeks: int
    negotiated_scope: Optional[str] = None


class CommitmentResponse(BaseModel):
    """Response model for commitment data"""
    id: str
    session_id: str
    wbs_id: str
    committed_price: float
    committed_duration_weeks: int
    baseline_price: float
    baseline_duration_weeks: int
    savings: Optional[float]
    savings_percentage: Optional[float]
    negotiated_scope: Optional[str]
    created_at: str
    updated_session: Optional[SessionResponse] = None



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
    """Response model for session validation endpoint"""
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
    """Response model for session snapshot data"""
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
    """Response model for paginated snapshot list"""
    snapshots: List[SnapshotResponse]
    total_count: int
    limit: int
    offset: int
    has_more: bool

# --- FastAPI App Initialization ---

app = FastAPI(
    title="My FastAPI Backend",
    description="A backend service with Supabase integration using JWKS.",
    version="1.1.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    """A public endpoint that requires no authentication."""
    return {"message": "Welcome to the FastAPI backend with Supabase!"}


@app.get("/me", tags=["Users"])
def read_current_user(current_user: dict = Depends(get_current_user)):
    """
    A protected endpoint that returns the current authenticated user's info.
    The frontend must provide a valid Supabase JWT in the Authorization header.
    """
    return current_user


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_agent(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Send a message to an AI agent and get a response.

    This endpoint:
    1. Validates the agent_id
    2. Retrieves the agent's system prompt
    3. Calls Gemini AI with conversation context
    4. Saves the message to negotiation_history table
    5. Returns the AI agent's response

    Args:
        request: ChatRequest with session_id, agent_id, message, history, and context
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        ChatResponse with agent's response and metadata
    """
    try:
        # Validate agent_id
        valid_agents = ["anne-lise-berg", "bjorn-eriksen", "kari-andersen", "per-johansen"]
        if request.agent_id not in valid_agents:
            raise HTTPException(
                status_code=400,
                detail=f"Ugyldig agent_id. Må være en av: {', '.join(valid_agents)}"
            )

        # Get agent system prompt
        try:
            system_prompt = get_agent_prompt(request.agent_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Get Gemini service
        gemini_service = get_gemini_service()

        # Convert conversation history to dict format
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

        # Call Gemini AI
        ai_response = await gemini_service.chat_with_agent(
            agent_id=request.agent_id,
            system_prompt=system_prompt,
            user_message=request.message,
            conversation_history=conversation_history,
            game_context=request.game_context
        )

        # Detect if response is a disagreement (simple heuristic)
        is_disagreement = detect_disagreement(ai_response)

        # Save to database
        timestamp = datetime.utcnow().isoformat()

        try:
            db.table("negotiation_history").insert({
                "session_id": request.session_id,
                "agent_id": request.agent_id,
                "agent_name": get_agent_name(request.agent_id),
                "agent_type": get_agent_type(request.agent_id),
                "user_message": request.message,
                "agent_response": ai_response,
                "is_disagreement": is_disagreement,
                "context_snapshot": request.game_context or {},
                "timestamp": timestamp,
            }).execute()
        except Exception as db_error:
            print(f"Database error saving chat message: {db_error}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")

        # Return response
        return ChatResponse(
            agent_id=request.agent_id,
            agent_name=get_agent_name(request.agent_id),
            response=ai_response,
            timestamp=timestamp,
            is_disagreement=is_disagreement
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"En feil oppstod under samtalen. Vennligst prøv igjen."
        )


def detect_disagreement(ai_response: str) -> bool:
    """
    Detect if AI response contains disagreement indicators.

    Uses simple keyword matching to identify when the agent is
    rejecting or pushing back against the user's offer.

    Args:
        ai_response: The agent's response text

    Returns:
        True if disagreement detected, False otherwise
    """
    disagreement_keywords = [
        "dessverre",  # unfortunately
        "det går ikke",  # that won't work
        "for lavt",  # too low
        "urealistisk",  # unrealistic
        "kan ikke godta",  # cannot accept
        "må avslå",  # must decline
        "det er for",  # it's too
        "vi kan ikke",  # we cannot
        "ikke mulig",  # not possible
    ]

    response_lower = ai_response.lower()
    return any(keyword in response_lower for keyword in disagreement_keywords)


@app.get("/api/sessions", response_model=List[SessionResponse], tags=["Sessions"])
def get_user_sessions(
    current_user: dict = Depends(get_current_user),
    # db: Client = Depends(get_db_client) # Bypass authenticated client
):
    """
    Get all game sessions for the current user.

    Returns all sessions ordered by most recent first.

    Args:
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        List of SessionResponse objects
    """
    try:
        print(f"[DEBUG] Fetching sessions for user {current_user['id']} using GLOBAL client")
        response = supabase.table("game_sessions")\
            .select("*")\
            .eq("user_id", current_user["id"])\
            .order("created_at", desc=True)\
            .execute()
        
        print(f"[DEBUG] Found {len(response.data)} sessions")

        return [SessionResponse(**session) for session in response.data]

    except Exception as e:
        print(f"Error fetching user sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av økter"
        )


@app.post("/api/sessions", response_model=SessionResponse, tags=["Sessions"])
def create_session(
    request: CreateSessionRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Create a new game session.

    Initializes a new game session with default budget values and settings.
    Automatically creates a baseline snapshot (Version 0) showing the starting state.

    Args:
        request: CreateSessionRequest with budget parameters
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        SessionResponse with the created session data
    """
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

        # Use the authenticated client (db) instead of the global one (supabase)
        response = db.table("game_sessions").insert(session_data).execute()

        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Kunne ikke opprette spillsesjon"
            )

        session = response.data[0]
        session_id = session["id"]

        # Auto-create baseline snapshot (Version 0)
        try:
            db.rpc("create_baseline_snapshot", {
                "p_session_id": session_id,
                "p_project_end_date": "2025-08-30",
                "p_days_before_deadline": 258
            }).execute()
            print(f"Created baseline snapshot for session {session_id}")
        except Exception as snapshot_error:
            print(f"Warning: Could not create baseline snapshot: {snapshot_error}")
            # Don't fail the request if snapshot creation fails

        return SessionResponse(**session)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"En feil oppstod ved opprettelse av spillsesjon: {str(e)}"
        )


@app.get("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Get a specific game session by ID.

    Args:
        session_id: The UUID of the session
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        SessionResponse with the session data
    """
    try:
        response = db.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        return SessionResponse(**response.data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av spillsesjon"
        )


@app.put("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def update_session(
    session_id: str,
    updates: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Update a game session.

    Allows updating fields like status, current_budget_used, game_state, etc.

    Args:
        session_id: The UUID of the session
        updates: Dictionary of fields to update
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        SessionResponse with the updated session data
    """
    try:
        # Verify session belongs to user
        existing = db.table("game_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Update the session
        response = db.table("game_sessions")\
            .update(updates)\
            .eq("id", session_id)\
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Kunne ikke oppdatere spillsesjon"
            )

        return SessionResponse(**response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved oppdatering av spillsesjon"
        )


@app.post("/api/sessions/{session_id}/commitments", response_model=CommitmentResponse, tags=["Commitments"])
def create_commitment(
    session_id: str,
    request: CreateCommitmentRequest,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Create a WBS commitment (accept an offer).

    This endpoint:
    1. Validates budget is not exceeded
    2. Creates commitment in wbs_commitments table
    3. Updates session.current_budget_used
    4. Returns the commitment with calculated savings

    Args:
        session_id: The UUID of the session
        request: CreateCommitmentRequest with commitment details
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        CommitmentResponse with the created commitment
    """
    try:
        # Verify session belongs to user and get current budget
        session_response = db.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        session = session_response.data
        current_budget_used = session["current_budget_used"]
        available_budget = session["available_budget"]

        # Validate WBS ID
        valid_wbs = ["1.3.1", "1.3.2", "1.4.1"]
        if request.wbs_id not in valid_wbs:
            raise HTTPException(
                status_code=400,
                detail=f"Ugyldig WBS ID. Må være en av: {', '.join(valid_wbs)}"
            )

        # Check if this WBS area already committed
        existing = db.table("wbs_commitments")\
            .select("id")\
            .eq("session_id", session_id)\
            .eq("wbs_id", request.wbs_id)\
            .execute()

        if existing.data:
            raise HTTPException(
                status_code=400,
                detail=f"WBS {request.wbs_id} er allerede forpliktet"
            )

        # Calculate new total budget used
        new_budget_used = current_budget_used + request.committed_price

        # Validate budget not exceeded
        if new_budget_used > available_budget:
            remaining = available_budget - current_budget_used
            raise HTTPException(
                status_code=400,
                detail=f"Budsjett overskredet. Gjenstående: {remaining:,.0f} NOK, Forsøk på forpliktelse: {request.committed_price:,.0f} NOK"
            )

        # Create commitment
        commitment_data = {
            "session_id": session_id,
            "wbs_id": request.wbs_id,
            "committed_price": request.committed_price,
            "committed_duration_weeks": request.committed_duration_weeks,
            "baseline_price": request.baseline_price,
            "baseline_duration_weeks": request.baseline_duration_weeks,
            "negotiated_scope": request.negotiated_scope,
        }

        commitment_response = db.table("wbs_commitments")\
            .insert(commitment_data)\
            .execute()

        if not commitment_response.data:
            raise HTTPException(
                status_code=500,
                detail="Kunne ikke opprette forpliktelse"
            )

        # Update session budget
        db.table("game_sessions")\
            .update({"current_budget_used": new_budget_used})\
            .eq("id", session_id)\
            .execute()

        commitment = commitment_response.data[0]

        # Auto-create contract snapshot
        try:
            from services.critical_path_service import calculate_critical_path
            import json

            # Calculate updated budget values (in øre for database)
            budget_committed = int(new_budget_used * 100)  # Convert NOK to øre
            budget_available = int((available_budget - new_budget_used) * 100)
            contract_cost = int(request.committed_price * 100)

            # Map WBS ID to supplier name
            supplier_map = {
                "1.3.1": "Bjørn Eriksen AS",
                "1.3.2": "Bjørn Eriksen AS",
                "1.4.1": "Kari Andersen AS"
            }
            supplier = supplier_map.get(request.wbs_id, "Ukjent")

            # Convert weeks to days
            duration_days = request.committed_duration_weeks * 7

            # Get all commitments for this session to calculate timeline
            all_commitments_response = db.table("wbs_commitments")\
                .select("*")\
                .eq("session_id", session_id)\
                .execute()

            all_commitments = all_commitments_response.data if all_commitments_response.data else []

            # Load WBS data
            with open("data/wbs.json", "r", encoding="utf-8") as f:
                wbs_data = json.load(f)

            # Calculate critical path and timeline
            timeline = calculate_critical_path(
                wbs_items=wbs_data["wbs_elements"],
                commitments=[{
                    "wbs_item_id": c["wbs_id"],
                    "duration": c.get("committed_duration_weeks", 0) * 7
                } for c in all_commitments],
                start_date="2025-01-15",
                deadline="2026-05-15"
            )

            # Calculate project end date and days before deadline
            project_end_date = timeline.get("projected_completion_date", "2025-09-29")
            from datetime import datetime
            deadline_dt = datetime.strptime("2026-05-15", "%Y-%m-%d")
            project_dt = datetime.strptime(project_end_date, "%Y-%m-%d")
            days_before_deadline = (deadline_dt - project_dt).days

            db.rpc("create_contract_snapshot", {
                "p_session_id": session_id,
                "p_wbs_id": request.wbs_id,
                "p_cost": contract_cost,
                "p_duration": duration_days,
                "p_supplier": supplier,
                "p_budget_committed": budget_committed,
                "p_budget_available": budget_available,
                "p_project_end_date": project_end_date,
                "p_days_before_deadline": days_before_deadline,
                "p_gantt_state": timeline,  # Save full timeline data for Gantt
                "p_precedence_state": timeline  # Save full timeline data for precedence diagram
            }).execute()
            print(f"Created contract snapshot for WBS {request.wbs_id} in session {session_id}")
        except Exception as snapshot_error:
            print(f"Warning: Could not create contract snapshot: {snapshot_error}")
            # Don't fail the request if snapshot creation fails

        return CommitmentResponse(**commitment)
        # Fetch the updated session to return to the frontend
        updated_session_response = db.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .single()\
            .execute()
            
        updated_session = SessionResponse(**updated_session_response.data) if updated_session_response.data else None

        return CommitmentResponse(
            **commitment_response.data[0],
            updated_session=updated_session
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating commitment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved opprettelse av forpliktelse"
        )


@app.get("/api/sessions/{session_id}/commitments", response_model=List[CommitmentResponse], tags=["Commitments"])
def get_commitments(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Get all commitments for a session.

    Args:
        session_id: The UUID of the session
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        List of CommitmentResponse objects
    """
    try:
        # Verify session belongs to user
        session_response = db.table("game_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Get commitments
        commitments_response = db.table("wbs_commitments")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("created_at")\
            .execute()

        return [CommitmentResponse(**c) for c in commitments_response.data]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching commitments: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av forpliktelser"
        )


@app.get("/api/sessions/{session_id}/history", response_model=List[NegotiationHistoryRecord], tags=["Sessions"])
def get_negotiation_history(
    session_id: str,
    agent_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    # Temporarily bypass get_db_client to use global supabase client for debugging
    db: Client = Depends(get_db_client)
) -> List[NegotiationHistoryRecord]:
    """
    Get negotiation history for a specific game session.
    Optionally filter by agent_id.
    """
    try:
        # Verify session belongs to user (still need user_id for this check)
        session_response = db.table("game_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Build the query for negotiation history
        query = db.table("negotiation_history")\
            .select("*")\
            .eq("session_id", session_id)

        if agent_id:
            query = query.eq("agent_id", agent_id)

        # Order by timestamp for chronological history
        negotiation_response = query.order("timestamp").execute()

        return [NegotiationHistoryRecord(**msg) for msg in negotiation_response.data]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching negotiation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av samtalehistorikk"
        )


@app.post("/api/sessions/{session_id}/validate", response_model=ValidationResponse, tags=["Validation"])
def validate_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Validate a game session by calculating critical path and checking constraints.

    Performs:
    - Budget validation (total cost ≤ 700 MNOK)
    - Timeline validation (completion date ≤ May 15, 2026)
    - Critical path calculation (CPM algorithm)
    - Earliest Start/Finish calculation
    - Latest Start/Finish calculation
    - Slack time calculation

    Returns timeline data for Gantt chart and precedence diagram visualization.
    """
    import json
    from pathlib import Path

    try:
        # Verify session belongs to user
        session_response = supabase.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        session = session_response.data

        # Load WBS data from JSON file
        wbs_file_path = Path(__file__).parent.parent / "frontend" / "public" / "data" / "wbs.json"
        with open(wbs_file_path, 'r', encoding='utf-8') as f:
            wbs_data = json.load(f)

        wbs_items = wbs_data.get('wbs_elements', [])

        # Get commitments for this session
        commitments_response = supabase.table("wbs_commitments")\
            .select("*")\
            .eq("session_id", session_id)\
            .execute()

        # Convert commitment weeks to days for calculation
        commitments = []
        for c in commitments_response.data:
            commitments.append({
                'wbs_item_id': c['wbs_id'],
                'duration': c.get('committed_duration_weeks', 0) * 7,  # Convert weeks to days
                'cost': c.get('committed_price', 0)
            })

        # Calculate critical path
        timeline_result = calculate_critical_path(
            wbs_items=wbs_items,
            commitments=commitments,
            start_date="2025-01-15",
            deadline="2026-05-15"
        )

        # Budget validation
        budget_used = session.get('current_budget_used', 0)
        budget_remaining = session.get('total_budget', 700_000_000) - budget_used
        budget_valid = budget_used <= session.get('total_budget', 700_000_000)

        # Combine results
        validation_result = {
            **timeline_result,
            'budget_valid': budget_valid,
            'budget_used': budget_used,
            'budget_remaining': budget_remaining,
            'valid': timeline_result['meets_deadline'] and budget_valid
        }

        return ValidationResponse(**validation_result)

    except HTTPException:
        raise
    except FileNotFoundError:
        print("WBS data file not found")
        raise HTTPException(
            status_code=500,
            detail="WBS data kunne ikke lastes"
        )
    except Exception as e:
        print(f"Error validating session: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"En feil oppstod ved validering: {str(e)}"
        )


@app.get("/api/sessions/{session_id}/snapshots", response_model=SnapshotListResponse, tags=["Snapshots"])
def get_session_snapshots(
    session_id: str,
    limit: int = 5,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Get session snapshots with pagination.

    Returns snapshots ordered by version DESC (newest first).
    Load 5 initially, 10 more on scroll/button click.

    Args:
        session_id: The UUID of the session
        limit: Number of snapshots to return (default: 5)
        offset: Number of snapshots to skip (default: 0)
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        SnapshotListResponse with paginated snapshots
    """
    try:
        # Verify session belongs to user
        session_response = db.table("game_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Get total count
        count_response = db.table("session_snapshots")\
            .select("id", count="exact")\
            .eq("session_id", session_id)\
            .execute()

        total_count = count_response.count or 0

        # Get paginated snapshots
        snapshots_response = db.table("session_snapshots")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("version", desc=True)\
            .limit(limit)\
            .range(offset, offset + limit - 1)\
            .execute()

        snapshots = [SnapshotResponse(**s) for s in snapshots_response.data]
        has_more = (offset + limit) < total_count

        return SnapshotListResponse(
            snapshots=snapshots,
            total_count=total_count,
            limit=limit,
            offset=offset,
            has_more=has_more
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching snapshots: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av snapshots"
        )


@app.get("/api/sessions/{session_id}/snapshots/{version}", response_model=SnapshotResponse, tags=["Snapshots"])
def get_snapshot_by_version(
    session_id: str,
    version: int,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Get a specific snapshot by version number.

    Args:
        session_id: The UUID of the session
        version: The snapshot version number (0, 1, 2, ...)
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        SnapshotResponse for the specified version
    """
    try:
        # Verify session belongs to user
        session_response = db.table("game_sessions")\
            .select("id")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Get snapshot by version
        snapshot_response = db.table("session_snapshots")\
            .select("*")\
            .eq("session_id", session_id)\
            .eq("version", version)\
            .single()\
            .execute()

        if not snapshot_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Snapshot versjon {version} ikke funnet"
            )

        return SnapshotResponse(**snapshot_response.data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching snapshot: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved henting av snapshot"
        )


@app.get("/api/sessions/{session_id}/snapshots/export", tags=["Snapshots"])
def export_session_snapshots(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Client = Depends(get_db_client)
):
    """
    Export all session snapshots as JSON.

    Returns complete snapshot history for the session in JSON format.
    Useful for downloading/analyzing session progression.

    Args:
        session_id: The UUID of the session
        current_user: Authenticated user from JWT token
        db: Authenticated Supabase client

    Returns:
        JSON with all snapshots and session metadata
    """
    try:
        # Verify session belongs to user
        session_response = db.table("game_sessions")\
            .select("*")\
            .eq("id", session_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not session_response.data:
            raise HTTPException(
                status_code=404,
                detail="Spillsesjon ikke funnet"
            )

        # Get all snapshots
        snapshots_response = db.table("session_snapshots")\
            .select("*")\
            .eq("session_id", session_id)\
            .order("version")\
            .execute()

        # Build export data
        export_data = {
            "session": session_response.data,
            "snapshots": snapshots_response.data,
            "export_timestamp": datetime.utcnow().isoformat(),
            "total_snapshots": len(snapshots_response.data)
        }

        return export_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error exporting snapshots: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved eksport av snapshots"
        )
