import time
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, jwk, JWTError
from supabase import create_client, Client

from config import settings

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
        if not kid:
            raise HTTPException(status_code=401, detail="Invalid token: 'kid' not found in header")

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == kid:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break
        
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid token: Matching key not found in JWKS")

        public_key = jwk.construct(rsa_key)

        payload = jwt.decode(
            token.credentials,
            public_key,
            algorithms=["RS256"],
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
