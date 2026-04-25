from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ner_service import NERService

router = APIRouter()
ner_service = NERService()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def generate_natural_response(ner_data) -> str:
    """
    Generates a supplementary clinical explanation without repeating alerts or decisions.
    Strictly follows 4-part CDSS mechanism reasoning based on dynamic data.
    """
    if(ner_data.risk_level == "LOW" and not ner_data.alerts):
        return "**Mechanism**: Standard metabolic pathways preserved.\n**Clinical Impact**: No severe impact anticipated.\n**Patient Risk Factors**: Standard clearance baselines.\n**Outcome**: Proceeds without modification."
        
    explanation = f"**Mechanism**: {ner_data.analysis.mechanism}\n"
    explanation += f"**Clinical Impact**: {ner_data.analysis.impact}\n"
    explanation += f"**Patient Risk Factors**: {ner_data.analysis.risk_factors}\n"
    explanation += f"**Outcome**: {ner_data.analysis.outcome}\n"
    
    return explanation

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    NLP Chatbot endpoint acting as pure mechanism summary.
    """
    ner_results = ner_service.extract_entities(request.message)
    natural_response = generate_natural_response(ner_results)
    
    return ChatResponse(response=natural_response)
