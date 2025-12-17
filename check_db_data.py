import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load backend environment variables
env_path = Path("backend/.env.local")
load_dotenv(dotenv_path=env_path)

supabase_url = os.getenv("SUPABASE_URL")
anon_key = os.getenv("SUPABASE_ANON_KEY")

headers = {
    "apikey": anon_key,
    "Authorization": f"Bearer {anon_key}",
    "Content-Type": "application/json"
}

print(f"Targeting Supabase URL: {supabase_url}")

# Define the session and agent to specifically test
test_session_id = "4563ac43-87c3-492d-b133-7957c9ab6b86"
test_agent_id = "bjorn-eriksen"

# 1. Fetch negotiation history for a specific session and agent
print(f"--- Fetching negotiation history for Session: {test_session_id}, Agent: {test_agent_id} ---")
url = f"{supabase_url}/rest/v1/negotiation_history?session_id=eq.{test_session_id}&agent_id=eq.{test_agent_id}&select=*"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(f"Total records found for specific query: {len(data)}")
    for record in data:
        print(f" - ID: {record.get('id')}")
        print(f"   Session: {record.get('session_id')}")
        print(f"   Agent: {record.get('agent_id')}")
        print(f"   Msg: {record.get('user_message')[:30]}...")
else:
    print(f"Error fetching specific history: {response.status_code} {response.text}")

# 2. Fetch all sessions (unchanged, just to verify full list)
print("\n--- Fetching ALL sessions ---")
url = f"{supabase_url}/rest/v1/game_sessions?select=id,created_at,user_id,status"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Total sessions found: {len(data)}")
    for session in data:
        print(f" - Session ID: {session.get('id')} (Status: {session.get('status')})")
