# My FastAPI Backend

This directory contains the FastAPI backend for your application, configured to work with Supabase for authentication using the modern JWKS standard.

## Setup and Running the Backend

This project uses `uv` as the package manager.

### 1. Prerequisites

-   Python 3.8+
-   `uv` installed (`pip install uv`)
-   `requests` (`uv pip install requests`)

### 2. Create a Virtual Environment

From within the `backend` directory, create and activate a virtual environment:

```bash
# Create the virtual environment
uv venv

# Activate the environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
# source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using `uv`:

```bash
uv pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file by copying the example file:

```bash
# On Windows
copy .env.example .env
# On macOS/Linux
# cp .env.example .env
```

Now, open the `.env` file and fill in the values. You only need to provide your project's URL and public anon key.

-   `SUPABASE_URL`: Found in your Supabase project's "API" settings.
-   `SUPABASE_ANON_KEY`: The public-facing "anon" key, also in the "API" settings.

### 5. Run the Development Server

Start the backend server with auto-reload enabled:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## How it Works

-   **Authentication (JWKS)**: The backend uses the modern and secure **JWKS (JSON Web Key Set)** method. Instead of a static secret, the server dynamically fetches a set of public cryptographic keys from a Supabase endpoint (`/.well-known/jwks.json`).
-   **Token Validation**: When the frontend sends a JWT, the backend uses the appropriate public key from the fetched set to verify the token's signature. This allows for seamless and secure key rotation by Supabase without requiring you to update any secrets.
-   **Protected Routes**: Endpoints that include `Depends(get_current_user)` are protected. They will only succeed if a valid JWT, signed by Supabase, is provided in the `Authorization` header.

**Note on Testing**: To test the protected `/me` endpoint, you must make a request from a client (like your frontend app) where a user is already logged in. The browser will automatically attach the valid JWT. You can no longer test it with a simple curl command using a placeholder token.
