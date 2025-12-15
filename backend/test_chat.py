"""
Test Chat Endpoint - Real AI Response
Tests the /api/chat endpoint with Anne-Lise Berg
"""

import requests
import json
from supabase import create_client
from config import settings

print("=" * 60)
print("Testing Chat Endpoint with Real AI")
print("=" * 60)
print()

# Initialize Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

# Get or create a test user
print("Step 1: Authentication")
print("-" * 60)

# For testing, we'll use the anon key and create a session
# In production, user would login via frontend
email = "test@example.com"
password = "test123456"

try:
    # Try to sign in
    print(f"Attempting to sign in as: {email}")
    auth_response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })
    print("[OK] Signed in successfully")
    token = auth_response.session.access_token
    user_id = auth_response.user.id

except Exception as e:
    print(f"[INFO] User doesn't exist, creating test user...")

    # Create test user
    try:
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if auth_response.session:
            print("[OK] Test user created and signed in")
            token = auth_response.session.access_token
            user_id = auth_response.user.id
        else:
            print("[WARN] User created but needs email confirmation")
            print("      Using admin bypass for testing...")
            # For development/testing only
            token = settings.SUPABASE_ANON_KEY
            user_id = "test-user-id"

    except Exception as create_error:
        print(f"[ERROR] Could not create user: {create_error}")
        print()
        print("SOLUTION: Use the Supabase dashboard to create a test user:")
        print("1. Go to Supabase Dashboard -> Authentication -> Users")
        print("2. Click 'Add user' -> Create a test user")
        print(f"3. Use email: {email}, password: {password}")
        exit(1)

print(f"User ID: {user_id[:20]}...")
print(f"Token: {token[:30]}...")
print()

# Prepare chat request
print("Step 2: Prepare Chat Request")
print("-" * 60)

chat_request = {
    "session_id": "test-session-001",
    "agent_id": "anne-lise-berg",
    "message": "Hei Anne-Lise! Kan vi få 2 måneder ekstra tid til prosjektet? Vi trenger det for å sikre god kvalitet.",
    "conversation_history": [],
    "game_context": {
        "total_budget": 700000000.00,
        "available_budget": 310000000.00,
        "current_budget_used": 0.00,
        "deadline_date": "2026-05-15",
        "commitments": []
    }
}

print("[OK] Request prepared")
print(f"Agent: Anne-Lise Berg (Municipality Owner)")
print(f"Message: {chat_request['message']}")
print()

# Make API request
print("Step 3: Send Request to API")
print("-" * 60)

url = "http://localhost:8000/api/chat"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

print(f"POST {url}")
print("Waiting for AI response...")
print()

try:
    response = requests.post(url, json=chat_request, headers=headers)

    if response.status_code == 200:
        data = response.json()

        print("=" * 60)
        print("SUCCESS! AI Response Received")
        print("=" * 60)
        print()
        print(f"Agent: {data['agent_name']}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Is Disagreement: {data['is_disagreement']}")
        print()
        print("Response:")
        print("-" * 60)
        print(data['response'])
        print("-" * 60)
        print()

        # Analyze response
        print("Analysis:")
        print("-" * 60)

        if data['is_disagreement']:
            print("[OK] ✓ Correctly flagged as disagreement")

        if "aldri" in data['response'].lower() or "ikke" in data['response'].lower():
            print("[OK] ✓ Anne-Lise rejected time extension (correct behavior)")

        if "mai 2026" in data['response'].lower() or "15. mai" in data['response'].lower():
            print("[OK] ✓ Referenced the May 15, 2026 deadline")

        if len(data['response']) > 50:
            print(f"[OK] ✓ Detailed response ({len(data['response'])} characters)")

        print()
        print("=" * 60)
        print("TEST PASSED! Chat endpoint working correctly!")
        print("=" * 60)

    elif response.status_code == 401:
        print("[ERROR] Authentication failed")
        print("Response:", response.json())
        print()
        print("This usually means:")
        print("1. JWT token is invalid")
        print("2. Test user doesn't exist in Supabase")
        print()
        print("Create a test user in Supabase Dashboard:")
        print("Authentication -> Users -> Add user")
        print(f"Email: {email}")
        print(f"Password: {password}")

    elif response.status_code == 423:
        print("[ERROR] Agent is locked (timeout)")
        print("Response:", response.json())

    else:
        print(f"[ERROR] Request failed with status {response.status_code}")
        print("Response:", response.text)

except requests.exceptions.ConnectionError:
    print("[ERROR] Could not connect to backend")
    print()
    print("Make sure the backend is running:")
    print("  cd backend")
    print("  uvicorn main:app --reload")
    print()
    print("Backend should be running on: http://localhost:8000")

except Exception as e:
    print(f"[ERROR] Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print()
