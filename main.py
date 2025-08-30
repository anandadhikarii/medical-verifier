from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import time

# --- Pydantic Models for Data Validation ---
# These models ensure the data sent to the API has the correct structure.

class Patient(BaseModel):
    """Defines the structure for patient data."""
    name: str
    age: int
    gender: str
    blood_group: str = Field(..., alias="blood_group")

class Drug(BaseModel):
    """Defines the structure for a single drug."""
    name: str
    dosage: str

class PrescriptionPayload(BaseModel):
    """Defines the structure for the main prescription analysis payload."""
    patient: Patient
    drugs: List[Drug]

class SymptomPayload(BaseModel):
    """Defines the structure for the symptom analysis payload."""
    symptoms: List[str]


# --- FastAPI Application Initialization ---
app = FastAPI(
    title="MediGuard AI Verifier API",
    description="Backend API for the AI Medical Prescription Verifier Streamlit app.",
    version="1.0.0"
)

# --- CORS (Cross-Origin Resource Sharing) Middleware ---
# This is crucial for allowing your Streamlit frontend (running on one port)
# to communicate with this FastAPI backend (running on another port).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# --- API Endpoints ---

@app.get("/")
def read_root():
    """
    Root endpoint for health checks.
    The Streamlit app pings this to check if the backend is connected.
    """
    return {"status": "MediGuard AI Backend is running"}

@app.post("/verify-prescription")
async def verify_prescription(payload: PrescriptionPayload):
    """
    Analyzes a prescription (patient info + drugs) and returns an AI-generated report.
    (This is a mock implementation for demonstration).
    """
    # Simulate a delay as if an AI model is processing
    time.sleep(2)
    
    # Mock AI analysis logic
    interaction_analysis = f"Analysis for {len(payload.drugs)} drug(s): No critical interactions found between {', '.join([d.name for d in payload.drugs])}. However, monitor for potential mild side effects."
    dosage_recommendations = f"Dosage appears standard for an adult aged {payload.patient.age}. Verify against clinical guidelines for specific conditions."
    alternative_suggestions = "For pain management, consider non-opioid alternatives if appropriate. If one of the drugs is for cholesterol, lifestyle changes are also recommended."
    
    return {
        "interaction_analysis": interaction_analysis,
        "dosage_recommendations": dosage_recommendations,
        "alternative_suggestions": alternative_suggestions
    }

@app.post("/extract-from-text")
async def extract_from_text(data: Dict[str, str]):
    """
    Extracts drug names and dosages from raw text.
    (This is a mock implementation for demonstration).
    """
    text = data.get("prescription_text", "").lower()
    # A very simple mock extraction
    drugs = []
    if "lisinopril 10mg" in text:
        drugs.append({"name": "Lisinopril", "dosage": "10mg"})
    if "metformin 500mg" in text:
        drugs.append({"name": "Metformin", "dosage": "500mg"})
    if not drugs:
         drugs.append({"name": "Extracted Drug (Mock)", "dosage": "As per text"})
    return {"drugs": drugs}

# --- NEW: The Missing Symptom Checker Endpoint ---
@app.post("/analyze-symptoms")
async def analyze_symptoms(payload: SymptomPayload):
    """
    Analyzes a list of symptoms and returns an AI-generated approximate analysis.
    (This is a mock implementation for demonstration).
    """
    # Simulate AI processing time
    time.sleep(1.5)

    symptoms = set(s.lower() for s in payload.symptoms)
    report = "### AI Symptom Analysis Report\n\n"

    # Mock AI logic based on symptom combinations
    if "fever" in symptoms and "cough" in symptoms and "sore throat" in symptoms:
        report += "**Possible Condition:** Based on the combination of fever, cough, and sore throat, a common viral respiratory infection like the **common cold or influenza** is possible.\n\n"
        report += "**Recommendations:**\n- Rest and stay hydrated.\n- Over-the-counter medications may help manage symptoms.\n- Monitor for worsening conditions like difficulty breathing."
    
    elif "headache" in symptoms and "dizziness" in symptoms:
        report += "**Possible Considerations:** Headache combined with dizziness can be related to various factors, including **dehydration, migraines, or inner ear issues**.\n\n"
        report += "**Recommendations:**\n- Ensure adequate fluid intake.\n- Rest in a quiet, dark room.\n- Avoid sudden movements."
        
    elif "nausea" in symptoms and "body aches" in symptoms:
        report += "**Possible Condition:** The combination of nausea and body aches could suggest a **gastrointestinal issue or a systemic viral infection**.\n\n"
        report += "**Recommendations:**\n- Stick to a bland diet (e.g., BRAT diet).\n- Rest is crucial for recovery."

    else:
        report += "**General Analysis:** The provided symptoms are general. It is important to monitor them closely.\n\n"
        report += "**General Recommendations:**\n- Ensure you are well-rested and hydrated.\n- A balanced diet can support your immune system."
        
    report += "\n\n---\n\n*Disclaimer: This is an AI-generated approximation and is not a substitute for professional medical advice. Please consult a healthcare provider for an accurate diagnosis.*"

    return {"report": report}
