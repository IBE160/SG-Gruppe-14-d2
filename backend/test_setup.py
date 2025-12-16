"""
Backend Setup Test Script
Tests that all components are configured correctly
"""

import sys
from pathlib import Path

# Use ASCII-compatible checkmarks for Windows
OK = "[OK]"
FAIL = "[FAIL]"
WARN = "[WARN]"

print("=" * 60)
print("PM Simulator Backend Setup Test")
print("=" * 60)
print()

# Test 1: Check environment variables
print("Test 1: Environment Configuration")
print("-" * 60)
try:
    from config import settings

    print(f"{OK} Config loaded successfully")
    print(f"   Supabase URL: {settings.SUPABASE_URL[:40]}...")
    print(f"   Supabase Key: {settings.SUPABASE_ANON_KEY[:20]}...")

    if hasattr(settings, 'GEMINI_API_KEY'):
        if settings.GEMINI_API_KEY == "REPLACE_WITH_YOUR_ACTUAL_API_KEY":
            print(f"{WARN} GEMINI_API_KEY not configured yet!")
            print("   Please add your real API key to backend/.env.local")
            print("   Get one from: https://aistudio.google.com/apikey")
            api_key_configured = False
        else:
            print(f"{OK} Gemini API Key: {settings.GEMINI_API_KEY[:20]}...")
            print(f"   Gemini Model: {settings.GEMINI_MODEL}")
            api_key_configured = True
    else:
        print(f"{FAIL} GEMINI_API_KEY not found in config")
        sys.exit(1)

except Exception as e:
    print(f"{FAIL} Config error: {e}")
    sys.exit(1)

print()

# Test 2: Check agent prompts
print("Test 2: Agent Prompts Loader")
print("-" * 60)
try:
    from prompts.agent_prompts import AGENT_PROMPTS, get_agent_prompt, get_agent_name

    print(f"{OK} Loaded {len(AGENT_PROMPTS)} agent prompts:")

    for agent_id, prompt in AGENT_PROMPTS.items():
        name = get_agent_name(agent_id)
        print(f"   - {agent_id}: {name}")
        print(f"     Prompt length: {len(prompt)} characters")

        if len(prompt) < 100:
            print(f"     {WARN} Warning: Prompt seems too short!")

    # Test Anne-Lise specifically
    anne_prompt = get_agent_prompt("anne-lise-berg")
    if "NEVER" in anne_prompt or "aldri" in anne_prompt.lower():
        print(f"{OK} Anne-Lise prompt contains 'NEVER' rule (correct)")
    else:
        print(f"{WARN} Anne-Lise prompt might be missing critical rules")

except Exception as e:
    print(f"{FAIL} Agent prompts error: {e}")
    sys.exit(1)

print()

# Test 3: Check Gemini service
print("Test 3: Gemini Service")
print("-" * 60)
if not api_key_configured:
    print(f"{WARN} Skipping - API key not configured")
else:
    try:
        from services.gemini_service import get_gemini_service

        gemini_service = get_gemini_service()
        print(f"{OK} Gemini service initialized")
        print(f"   Model: {gemini_service.model.model_name}")
        print(f"   Temperature: {gemini_service.generation_config['temperature']}")
        print(f"   Max tokens: {gemini_service.generation_config['max_output_tokens']}")

    except Exception as e:
        print(f"{FAIL} Gemini service error: {e}")
        print()
        print("Common fixes:")
        print("1. Check your API key is correct")
        print("2. Verify API key permissions at https://aistudio.google.com/apikey")
        sys.exit(1)

print()

# Test 4: Check Supabase connection
print("Test 4: Supabase Connection")
print("-" * 60)
try:
    from main import supabase

    # Try to query tables
    result = supabase.table("game_sessions").select("id").limit(0).execute()
    print(f"{OK} Connected to Supabase")
    print(f"{OK} game_sessions table exists")

    # Check other tables
    tables = ["wbs_commitments", "negotiation_history", "agent_timeouts", "user_analytics"]
    all_tables_exist = True
    for table in tables:
        try:
            supabase.table(table).select("id").limit(0).execute()
            print(f"{OK} {table} table exists")
        except Exception as e:
            print(f"{FAIL} {table} table missing")
            all_tables_exist = False

    if not all_tables_exist:
        print()
        print("Missing tables! You need to import the database schema:")
        print("1. Go to Supabase Dashboard -> SQL Editor")
        print("2. Copy database/migrations/001_complete_schema.sql")
        print("3. Paste and Run")
        sys.exit(1)

except Exception as e:
    print(f"{FAIL} Supabase connection error: {e}")
    print()
    print("Possible issues:")
    print("1. Database schema not imported - run the SQL migration in Supabase")
    print("2. Supabase credentials incorrect in .env.local")
    sys.exit(1)

print()
print("=" * 60)
if api_key_configured:
    print("SUCCESS! All tests passed!")
else:
    print("PARTIAL SUCCESS - Add Gemini API key to complete setup")
print("=" * 60)
print()
print("Next steps:")
if not api_key_configured:
    print("1. Add your Gemini API key to backend/.env.local")
    print("   Get key from: https://aistudio.google.com/apikey")
print("2. Start the backend: uvicorn main:app --reload")
print("3. Visit API docs: http://localhost:8000/docs")
print("4. Test chat endpoint with a real message")
print()
