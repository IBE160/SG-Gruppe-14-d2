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
    message_lower = request.message.lower()
    response_message = f"I have received your message: '{request.message}'." # Default fallback

    # Common keywords
    keywords = {
        "price": "cost",
        "cost": "cost",
        "fee": "cost",
        "budget": "cost",
        "money": "cost",
        "time": "schedule",
        "schedule": "schedule",
        "deadline": "schedule",
        "delay": "schedule",
        "quality": "quality",
        "standard": "quality",
        "material": "materials",
        "materials": "materials",
        "scope": "scope",
        "deliverables": "scope",
    }
    detected_keyword = None
    for keyword, category in keywords.items():
        if keyword in message_lower:
            detected_keyword = category
            break

    if request.persona_id == 'contractor':
        wbs_mention = re.search(r'(\d+(\.\d+)*)', request.message)
        if wbs_mention:
            wbs_id = wbs_mention.group(0)
            response_message = f"Regarding WBS {wbs_id}: As the General Contractor, we are ready to discuss the details. Our estimates are competitive and our execution is efficient."
        elif detected_keyword == "cost":
            response_message = "As the General Contractor, we focus on delivering value. Let's discuss your budget and find an optimal solution."
        elif detected_keyword == "schedule":
            response_message = "Meeting deadlines is crucial for us. Share your timeline, and we'll provide a realistic plan to keep the project on track."
        elif detected_keyword == "quality":
            response_message = "Our work is defined by its quality. We ensure all specifications are met and exceed expectations where possible."
        elif detected_keyword == "materials":
            response_message = "We source high-quality materials to ensure durability and performance. Do you have specific material requirements?"
        elif detected_keyword == "scope":
            response_message = "Understanding the project scope is key. Provide us with more details about deliverables, and we'll prepare a comprehensive plan."
        else:
            response_message = f"As the General Contractor, I've received your message: '{request.message}'. How can we help you achieve your project goals?"

    elif request.persona_id == 'architect':
        if detected_keyword == "cost":
            response_message = "As the Architect, my designs optimize for long-term value and aesthetics, not just initial cost. What is your overall project vision?"
        elif detected_keyword == "schedule":
            response_message = "Design phases require careful consideration. A well-planned schedule ensures creative integrity without unnecessary rushes."
        elif detected_keyword == "quality":
            response_message = "Architectural quality is paramount. My designs adhere to the highest standards, ensuring both functionality and aesthetic appeal."
        elif detected_keyword == "materials":
            response_message = "Material selection is integral to the design. Do you have specific preferences or sustainable considerations for your materials?"
        elif detected_keyword == "scope":
            response_message = "The project scope guides the design process. Let's clearly define your objectives to create a cohesive architectural vision."
        else:
            response_message = f"I am the Architect. My vision is non-negotiable, and my fee reflects the quality of my work. You asked: '{request.message}'. What aspect of the design are you curious about?"
    
    elif request.persona_id == 'hvac':
        if detected_keyword == "cost":
            response_message = "As the HVAC Engineer, my systems are designed for optimal energy efficiency, which translates to long-term cost savings. Can you specify your budget expectations?"
        elif detected_keyword == "schedule":
            response_message = "HVAC system installation needs to be integrated seamlessly into the overall project schedule. What are your installation timelines?"
        elif detected_keyword == "quality":
            response_message = "Our HVAC designs prioritize system reliability and air quality. We adhere to all industry standards for performance."
        elif detected_keyword == "materials":
            response_message = "Specific materials for ducts, units, and insulation are chosen for efficiency and durability. Are there particular material concerns?"
        elif detected_keyword == "scope":
            response_message = "To ensure an effective HVAC system, a clear definition of the building's usage and requirements is essential. What are your specific needs?"
        else:
            response_message = f"As the HVAC Engineer, I can assure you my design is optimal. The price is based on a detailed calculation. In response to '{request.message}', please provide more technical details."

    else:
        response_message = f"Unknown persona. Your message was: '{request.message}'. Please select a valid persona to negotiate."


    return {"text": response_message, "sender": "ai"}
