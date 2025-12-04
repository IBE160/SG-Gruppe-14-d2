from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import os
import re

class NegotiationRequest(BaseModel):
    persona_id: str
    message: str

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!"}

@app.get("/wbs")
async def get_wbs():
    # Correctly locate the PDF relative to the current script
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "data", "wbs.pdf")
    wbs_items = []

    if not os.path.exists(pdf_path):
        return {"error": "wbs.pdf not found at the expected path."}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
            
            wbs_pattern = re.compile(r"^(\d+(\.\d+)*)\s+(.*)", re.MULTILINE)
            matches = wbs_pattern.findall(full_text)

            for match in matches:
                wbs_items.append({
                    "id": match[0],
                    "name": match[2].strip(),
                    "status": "Not Started" # Default status
                })

    except Exception as e:
        return {"error": f"Failed to parse PDF: {str(e)}"}

    if not wbs_items:
        return [
            {"id": "0.0", "name": "Error: Could not parse WBS from PDF.", "status": "Error"}
        ]

    return wbs_items

@app.post("/negotiate")
async def negotiate(request: NegotiationRequest):
    
    response_message = f"I have received your message: '{request.message}'."

    if request.persona_id == 'contractor':
        wbs_mention = re.search(r'(\d+(\.\d+)*)', request.message)
        if wbs_mention:
            wbs_id = wbs_mention.group(0)
            response_message = f"Regarding WBS {wbs_id}: We are the General Contractor. We can do it for a good price, but we need to discuss the details for that specific item."
        else:
            response_message = f"As the General Contractor, I've received your message: '{request.message}'. What can I help you with today? Feel free to ask about specific WBS items."

    elif request.persona_id == 'architect':
        response_message = f"I am the Architect. My vision is non-negotiable, and my fee reflects the quality of my work. You mentioned: '{request.message}'."
    
    elif request.persona_id == 'hvac':
        response_message = f"As the HVAC Engineer, I can assure you my design is optimal. The price is based on a detailed calculation. In response to '{request.message}', please provide more technical details."

    else:
        response_message = f"Unknown persona. Your message was: '{request.message}'."


    return {"text": response_message, "sender": "ai"}
