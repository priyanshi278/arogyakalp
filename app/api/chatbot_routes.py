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
    Summarizes structured NER data into a natural language string.
    """
    if not ner_data.drugs:
        return "I couldn't identify any specific drugs in your message. Please provide drug names for a safety analysis."

    # Identify drugs
    drug_names = []
    for d in ner_data.drugs:
        if d.original.lower() != d.generic.lower():
            drug_names.append(f"{d.original} ({d.generic})")
        else:
            drug_names.append(d.original)
    
    drugs_str = ", ".join(drug_names)
    
    # 1. Start with identification
    base_response = f"I've identified: {drugs_str}. "

    # 2. Side effects (ADRs)
    side_effects_text = ""
    if ner_data.adr_predictions:
        se_list = []
        for adr in ner_data.adr_predictions:
            if adr.side_effects:
                se_list.append(f"{adr.drug} may cause {', '.join(adr.side_effects[:2])}")
        
        if se_list:
            side_effects_text = "Possible side effects include: " + "; ".join(se_list) + ". "
    else:
        side_effects_text = "No major side effects were predicted for these drugs. "

    # 3. Interactions (DDIs)
    interaction_text = ""
    if ner_data.drug_interactions:
        bad_interactions = [i for i in ner_data.drug_interactions if i.interaction != "no known interaction"]
        if bad_interactions:
            interaction_text = "Warning: Interaction detected - " + "; ".join([i.interaction for i in bad_interactions]) + ". "
        else:
            interaction_text = "No significant drug-drug interactions detected. "
    
    # 4. Recommendations
    recommendation_text = ""
    if ner_data.recommendations:
        rec_list = [f"Consider {r.alternative} instead of {r.drug} ({r.issue})" for r in ner_data.recommendations]
        recommendation_text = "Suggested alternatives: " + "; ".join(rec_list) + ". "

    # Combine
    final_response = f"{base_response}{side_effects_text}{interaction_text}{recommendation_text}Always consult your doctor before making changes to your medication."
    
    return final_response

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    NLP Chatbot endpoint to analyze medications in natural language.
    """
    # 1. Process text through the existing pipeline
    ner_results = ner_service.extract_entities(request.message)
    
    # 2. Convert structured results to natural language
    natural_response = generate_natural_response(ner_results)
    
    return ChatResponse(response=natural_response)
