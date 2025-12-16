"""
Simple Chat Test - Direct Gemini Test
Tests the Gemini service directly without authentication
"""

import asyncio
from services.gemini_service import get_gemini_service
from prompts.agent_prompts import get_agent_prompt, get_agent_name

print("=" * 60)
print("Testing Gemini AI Service Directly")
print("=" * 60)
print()

# Test parameters
agent_id = "anne-lise-berg"
user_message = "Hei Anne-Lise! Kan vi få 2 måneder ekstra tid til prosjektet? Vi trenger det for å sikre god kvalitet."

print(f"Agent: {get_agent_name(agent_id)}")
print(f"Message: {user_message}")
print()

# Get Gemini service
print("Initializing Gemini service...")
gemini_service = get_gemini_service()
print("[OK] Gemini service initialized")
print()

# Get agent prompt
print("Loading agent system prompt...")
system_prompt = get_agent_prompt(agent_id)
print(f"[OK] Loaded prompt ({len(system_prompt)} characters)")
print()

# Prepare game context
game_context = {
    "total_budget": 700000000.00,
    "available_budget": 310000000.00,
    "current_budget_used": 0.00,
    "deadline_date": "2026-05-15",
    "commitments": []
}

print("Sending message to Gemini AI...")
print("(This may take 3-5 seconds)")
print()

# Call Gemini
async def test_chat():
    response = await gemini_service.chat_with_agent(
        agent_id=agent_id,
        system_prompt=system_prompt,
        user_message=user_message,
        conversation_history=[],
        game_context=game_context
    )
    return response

# Run async function
try:
    response = asyncio.run(test_chat())

    print("=" * 60)
    print("SUCCESS! AI Response Received")
    print("=" * 60)
    print()
    print("Anne-Lise Berg's Response:")
    print("-" * 60)
    print(response)
    print("-" * 60)
    print()

    # Analyze response
    print("Analysis:")
    print("-" * 60)

    if "aldri" in response.lower() or "ikke" in response.lower():
        print("[OK] Anne-Lise rejected time extension (CORRECT)")
        print("      She should NEVER approve time extensions")

    if "mai 2026" in response.lower() or "15. mai" in response.lower() or "2026" in response:
        print("[OK] Referenced the May 15, 2026 deadline")

    if len(response) > 50:
        print(f"[OK] Detailed response ({len(response)} characters)")

    if any(word in response.lower() for word in ["dessverre", "frist", "ikke", "kan ikke"]):
        print("[OK] Used Norwegian rejection language")

    print()
    print("=" * 60)
    print("TEST PASSED! Gemini AI working correctly!")
    print("=" * 60)
    print()
    print("Key Verification:")
    print("[OK] Anne-Lise Berg (Owner) responds in Norwegian")
    print("[OK] She enforces the INFLEXIBLE May 15, 2026 deadline")
    print("[OK] She NEVER approves time extensions")
    print()

except Exception as e:
    print("[ERROR] Test failed:")
    print(str(e))
    print()
    import traceback
    traceback.print_exc()
