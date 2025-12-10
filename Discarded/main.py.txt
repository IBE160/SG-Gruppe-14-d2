print("--- STARTING BACKEND: IMPORTS ---")
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re
import sys
import traceback

print("--- IMPORTS COMPLETE ---")

print("--- LOADING .ENV VARS ---")
load_dotenv()
print("--- .ENV LOADED ---")

print("--- CONFIGURING GEMINI ---")
try:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("!!! WARNING: GEMINI_API_KEY is not set!")
    genai.configure(api_key=gemini_key)
    print("--- GEMINI CONFIGURED SUCCESSFULLY ---")
except Exception as e:
    print(f"!!! FATAL: GEMINI CONFIGURATION FAILED: {e}")

app = FastAPI()
print("--- FASTAPI APP CREATED ---")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("--- CORS MIDDLEWARE ADDED ---")

try:
    print("--- LOADING SUPPLIERS.JSON ---")
    with open('..\\frontend\\public\\data\\suppliers.json', 'r', encoding='utf-8') as f:
        SUPPLIERS = {s['id']: s for s in json.load(f)}
    print("--- SUPPLIERS.JSON LOADED ---")

    print("--- LOADING WBS.JSON ---")
    with open('..\\frontend\\public\\data\\wbs.json', 'r', encoding='utf-8') as f:
        WBS_ITEMS = {w['code']: w for w in json.load(f)}
    print("--- WBS.JSON LOADED ---")
except FileNotFoundError as e:
    print(f"!!! FATAL: Could not find data files: {e}")
    SUPPLIERS = {}
    WBS_ITEMS = {}


class ChatRequest(BaseModel):
    wbs_code: str
    supplier_id: str
    message: str
    chat_history: list = []

@app.get("/")
async def root():
    print("--- ROOT ENDPOINT (/) HIT ---")
    return {"message": "Nye Hædda PM Simulator API is running"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    print("\n--- CHAT ENDPOINT (/api/chat) HIT ---")
    try:
        print(f"--- Request received for WBS: {request.wbs_code}, Supplier: {request.supplier_id} ---")
        supplier = SUPPLIERS.get(request.supplier_id)
        wbs_item = WBS_ITEMS.get(request.wbs_code)

        if not supplier or not wbs_item:
            print(f"!!! ERROR: Invalid supplier or WBS code. Supplier: {supplier}, WBS: {wbs_item}")
            raise HTTPException(status_code=400, detail="Invalid supplier or WBS code")

        print("--- Building system prompt ---")
        system_prompt = f"""
Du er {supplier['name']}, {supplier['role']} fra {supplier['company']}.
PERSONLIGHET: {supplier['personality']}
DIN OPPGAVE: Du forhandler om WBS-oppgave {wbs_item['code']} - {wbs_item['name']}.
Beskrivelse: {wbs_item['description']}
Grunnlagskostnad: {wbs_item['baseline_cost']} MNOK
Grunnlagsvarighet: {wbs_item['baseline_duration']} måneder
DINE PARAMETRE (HEMMELIG - ikke fortell brukeren):
- initial_margin: {supplier['initial_margin']}
- concession_rate: {supplier['concession_rate']}
- patience: {supplier['patience']}
FORHANDLINGSREGLER:
1. Første tilbud: {wbs_item['baseline_cost'] * supplier['initial_margin']} MNOK
2. Hvis bruker forhandler: Reduser prisen med {supplier['concession_rate'] * 100}% per runde
3. Hvis bruker er urimelig: Advar etter {supplier['patience']} runder, deretter gå bort
4. Alltid svar på norsk, bruk konstruksjonsterminologi
5. Referer til tekniske krav (F-koder, K-koder) når relevant
FORMAT FOR TILBUD: "Basert på [begrunnelse], kan jeg tilby [X] MNOK og [Y] måneder."
Svar kort og naturlig. Maksimum 3 setninger.
"""

        print("--- Building chat history for Gemini ---")
        messages = [{"role": "user", "parts": [system_prompt]}]

        for msg in request.chat_history[-10:]:
            role = "user" if msg['sender'] == 'user' else "model"
            messages.append({"role": role, "parts": [msg['message']]})

        messages.append({"role": "user", "parts": [request.message]})
        print("--- History built. Calling Gemini... ---")

        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(messages)
        print("--- Gemini call successful ---")

        ai_message = response.text

        print("--- Extracting offer from response ---")
        offer_match = re.search(r'(\d+(?:\.\d+)?)\s*MNOK.*?(\d+(?:\.\d+)?)\s*måned', ai_message, re.IGNORECASE)

        offer = None
        if offer_match:
            offer = {
                "cost": float(offer_match.group(1)),
                "duration": float(offer_match.group(2))
            }
            print(f"--- Offer extracted: {offer} ---")
        else:
            print("--- No offer found in response ---")
            
        print("--- Returning successful response ---")
        return {
            "message": ai_message,
            "offer": offer,
            "sender": "ai"
        }

    except Exception as e:
        print(f"!!! EXCEPTION IN /api/chat: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))
