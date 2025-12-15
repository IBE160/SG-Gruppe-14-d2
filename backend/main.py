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

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Decodes and verifies the JWT token using the Supabase JWKS.
    Returns the user's data if the token is valid.
    """
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token.credentials)
        kid = unverified_header.get("kid")

        # Debug logging
        print(f"[DEBUG] Token kid: {kid}")
        print(f"[DEBUG] Available JWKS kids: {[k.get('kid') for k in jwks.get('keys', [])]}")

        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token: 'kid' not found in header")

        matching_key = None
        for key in jwks["keys"]:
            if key["kid"] == kid:
                matching_key = key
                break

        if not matching_key:
            print(f"[ERROR] No matching key found for kid: {kid}")
            raise HTTPException(status_code=401, detail="Invalid token: Matching key not found in JWKS")

        # Handle both RSA and EC keys
        if matching_key["kty"] == "RSA":
            jwk_key = {
                "kty": matching_key["kty"],
                "kid": matching_key["kid"],
                "use": matching_key["use"],
                "n": matching_key["n"],
                "e": matching_key["e"],
            }
            algorithm = "RS256"
        elif matching_key["kty"] == "EC":
            jwk_key = {
                "kty": matching_key["kty"],
                "kid": matching_key["kid"],
                "use": matching_key["use"],
                "crv": matching_key["crv"],
                "x": matching_key["x"],
                "y": matching_key["y"],
            }
            algorithm = "ES256"
        else:
            raise HTTPException(status_code=401, detail=f"Unsupported key type: {matching_key['kty']}")

        public_key = jwk.construct(jwk_key)

        payload = jwt.decode(
            token.credentials,
            public_key,
            algorithms=[algorithm],
            audience="authenticated",
            issuer=f"{settings.SUPABASE_URL}/auth/v1"
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: User ID not found")
        
        return {"id": user_id, "email": payload.get("email"), "role": payload.get("role")}

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except HTTPException as e:
        # Re-raise HTTPExceptions to avoid them being caught by the generic Exception
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


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
    offer_data: Optional[Dict[str, Any]]
    context_snapshot: Dict[str, Any]
    timestamp: str
    response_time_ms: Optional[int]
    sentiment: Optional[str]

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
    current_user: dict = Depends(get_current_user)
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
            supabase.table("negotiation_history").insert({
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
            # Continue anyway - don't fail the request if DB save fails

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
    current_user: dict = Depends(get_current_user)
):
    """
    Get all game sessions for the current user.

    Returns all sessions ordered by most recent first.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        List of SessionResponse objects
    """
    try:
        response = supabase.table("game_sessions")\
            .select("*")\
            .eq("user_id", current_user["id"])\
            .order("created_at", desc=True)\
            .execute()

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
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new game session.

    Initializes a new game session with default budget values and settings.

    Args:
        request: CreateSessionRequest with budget parameters
        current_user: Authenticated user from JWT token

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

        response = supabase.table("game_sessions").insert(session_data).execute()

        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Kunne ikke opprette spillsesjon"
            )

        return SessionResponse(**response.data[0])

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="En feil oppstod ved opprettelse av spillsesjon"
        )


@app.get("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific game session by ID.

    Args:
        session_id: The UUID of the session
        current_user: Authenticated user from JWT token

    Returns:
        SessionResponse with the session data
    """
    try:
        response = supabase.table("game_sessions")\
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
    current_user: dict = Depends(get_current_user)
):
    """
    Update a game session.

    Allows updating fields like status, current_budget_used, game_state, etc.

    Args:
        session_id: The UUID of the session
        updates: Dictionary of fields to update
        current_user: Authenticated user from JWT token

    Returns:
        SessionResponse with the updated session data
    """
    try:
        # Verify session belongs to user
        existing = supabase.table("game_sessions")\
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
        response = supabase.table("game_sessions")\
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
    current_user: dict = Depends(get_current_user)
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

    Returns:
        CommitmentResponse with the created commitment
    """
    try:
        # Verify session belongs to user and get current budget
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
        existing = supabase.table("wbs_commitments")\
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

        commitment_response = supabase.table("wbs_commitments")\
            .insert(commitment_data)\
            .execute()

        if not commitment_response.data:
            raise HTTPException(
                status_code=500,
                detail="Kunne ikke opprette forpliktelse"
            )

        # Update session budget
        supabase.table("game_sessions")\
            .update({"current_budget_used": new_budget_used})\
            .eq("id", session_id)\
            .execute()

        return CommitmentResponse(**commitment_response.data[0])

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
    current_user: dict = Depends(get_current_user)
):
    """
    Get all commitments for a session.

    Args:
        session_id: The UUID of the session
        current_user: Authenticated user from JWT token

    Returns:
        List of CommitmentResponse objects
    """
    try:
        # Verify session belongs to user
        session_response = supabase.table("game_sessions")\
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
        commitments_response = supabase.table("wbs_commitments")\
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
    current_user: dict = Depends(get_current_user)
):
    """
    Get negotiation history for a specific game session.
    Optionally filter by agent_id.
    """
    try:
        # Verify session belongs to user
        session_response = supabase.table("game_sessions")\
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
        query = supabase.table("negotiation_history")\
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
