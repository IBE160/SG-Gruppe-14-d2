# Troubleshooting Report: Authentication & RLS Authorization Issues

## 1. Problem Identification
The user encountered a persistent error flow when accessing the dashboard (`/dashboard`):
1.  **Initial Error:** `Invalid token: Matching key not found in JWKS`.
2.  **Secondary Error:** `new row violates row-level security policy for table "game_sessions"`.
3.  **Tertiary Error:** `Error: no active sessions` (Frontend parsing mismatch).

## 2. Root Cause Analysis

### Issue 1: "Invalid token: Matching key not found in JWKS"
*   **Observation:** The backend failed to validate the JWT token sent by the frontend. The `kid` (Key ID) in the token header did not exist in the Supabase JWKS (JSON Web Key Set).
*   **Diagnosis:** The user's browser was holding a **stale session token** from a previous project or session that used a different signing key. The backend correctly rejected it as it couldn't verify the signature against the current project's keys.
*   **Resolution:**
    1.  Added robust diagnostic logging to `backend/main.py` to inspect the token headers.
    2.  Implemented a **fallback verification mechanism** that attempts to validate tokens using the symmetric `SUPABASE_JWT_SECRET` (HS256) if the asymmetric JWKS verification fails.
    3.  Ultimately simplified the auth logic to use the official `supabase.auth.get_user()` method, which handles all key rotation and verification complexity automatically.

### Issue 2: "Row-Level Security (RLS) Policy Violation"
*   **Observation:** Once authentication passed, the `create_session` endpoint failed with a 500 error: `new row violates row-level security policy`.
*   **Diagnosis:** The backend was initializing a **global** Supabase client using the `SUPABASE_ANON_KEY`.
    *   While the *API endpoint* knew who the user was (via `get_current_user`), the *database client* performing the `insert` was still operating as an **anonymous user**.
    *   The database's RLS policy for `game_sessions` requires `auth.uid() = user_id`. Since the anonymous client has no `uid`, the check failed.
*   **Resolution:**
    1.  Created a new dependency `get_db_client` in `backend/main.py`.
    2.  This dependency creates a **request-scoped client** and explicitly authenticates it with the user's token using `client.postgrest.auth(token)`.
    3.  Updated all write endpoints (`create_session`, `update_session`, `create_commitment`, `chat`) to use this authenticated client.

### Issue 3: Frontend Data Parsing Mismatch
*   **Observation:** The backend returned `200 OK`, but the frontend displayed `Error: no active sessions`.
*   **Diagnosis:** The backend was returning Pydantic models directly (e.g., `SessionResponse`), which serialize to JSON as the object itself (e.g., `{ id: "...", ... }`).
    *   The frontend code in `frontend/lib/api/sessions.ts` was expecting a wrapper object (e.g., `data.session` or `data.sessions`).
    *   This caused `data.session` to be `undefined`, triggering the error.
*   **Resolution:**
    1.  Updated `frontend/lib/api/sessions.ts` to return the response data directly (e.g., `const data = await response.json(); return data;`).

## 3. Summary of Changes

### Backend (`backend/main.py`)
*   **Refactored Auth:** Replaced manual `jwt.decode` with `supabase.auth.get_user(token)`.
*   **Fixed RLS:** Introduced `get_db_client` dependency to authenticate database queries.
*   **Updated Endpoints:** Modified all endpoints to use the authenticated `db` client.

### Frontend (`frontend/lib/api/sessions.ts`)
*   **Fixed Parsing:** Removed `.session`, `.sessions`, and `.commitments` property accessors to match the direct JSON response from the backend.

## 4. Verification
The system now functions correctly:
1.  **Auth:** User logs in, token is verified by Supabase.
2.  **Database:** Backend performs actions *as the user*, passing RLS checks.
3.  **UI:** Frontend correctly reads the JSON response and renders the dashboard.
