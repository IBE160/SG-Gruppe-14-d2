"""
List Available Gemini Models
Diagnostic script to find correct model names for generateContent
"""

import google.generativeai as genai
from config import settings

print("=" * 60)
print("Gemini API - Available Models")
print("=" * 60)
print()

# Configure API
genai.configure(api_key=settings.GEMINI_API_KEY)
print(f"API Key: {settings.GEMINI_API_KEY[:20]}...")
print()

print("Models that support generateContent:")
print("-" * 60)

try:
    models = genai.list_models()
    found_models = []

    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            found_models.append(model)
            print(f"[OK] {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Methods: {', '.join(model.supported_generation_methods)}")
            print()

    if found_models:
        print("=" * 60)
        print(f"Found {len(found_models)} compatible models")
        print("=" * 60)
        print()
        print("Recommended model to use:")
        print(f"  {found_models[0].name}")
        print()
        print("Update gemini_service.py with:")
        print(f'  model_name = "{found_models[0].name}"')
        print()
    else:
        print("[ERROR] No models found that support generateContent")
        print()
        print("This could mean:")
        print("1. API key doesn't have access to Gemini models")
        print("2. API key is invalid")
        print("3. Billing not enabled on Google Cloud project")

except Exception as e:
    print(f"[ERROR] Failed to list models: {e}")
    print()
    import traceback
    traceback.print_exc()
