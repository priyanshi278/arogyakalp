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
    Summarizes structured NER data into a simple, natural language clinical assessment.
    """
    if not ner_data.drugs:
        return "I couldn't identify any specific medications in the notes. Please ensure the drug names are spelled correctly for a safety analysis."

    # Identify drugs
    drug_names = [d.original.capitalize() for d in ner_data.drugs]
    drugs_str = ", ".join(drug_names)
    
    # 1. Introduction
    response = f"Based on the clinical assessment, I have identified the following medications: {drugs_str}. "

    # 2. Side effects (ADRs)
    if ner_data.adr_predictions:
        se_details = []
        for adr in ner_data.adr_predictions:
            # The backend already filters adr_predictions to only include the new drug
            if adr.side_effects:
                se_details.append(f"The newly prescribed **{adr.drug}** has potential side effects like {', '.join(adr.side_effects[:2])}")
        
        if se_details:
            response += "Regarding the new medication, " + ". ".join(se_details) + ". "
    else:
        response += "No major side effects were found for the newly prescribed medication. "

    # 3. Interactions (DDIs)
    bad_interactions = [i for i in ner_data.drug_interactions if i.interaction.lower() != "no known interaction"]
    if bad_interactions:
        # Interactions involve BOTH new and old drugs
        risky_pairs = [f"{' and '.join(i.drug_pair)}" for i in bad_interactions if "risky" in i.interaction.lower() or "danger" in i.interaction.lower()]
        
        if risky_pairs:
            response += f"IMPORTANT: There is a potential interaction risk between {', '.join(risky_pairs)}. This combination should be monitored closely. "
        else:
            response += "Some mild interactions were noted between the new and existing medications. "
    else:
        response += "I found no significant drug-drug interactions between the new and existing medications. "
    
    # 4. Recommendations
    if ner_data.recommendations:
        rec_list = []
        for r in ner_data.recommendations:
            # The backend already filters recommendations to only include the new drug
            if "risky" in r.issue.lower() or "danger" in r.issue.lower():
                rec_list.append(f"due to interaction risks with current meds, you might consider **{r.alternative}** as an alternative to **{r.drug}**")
        
        if rec_list:
            response += "For better patient safety, " + "; ".join(rec_list) + ". "

    # Closing
    response += "Please note that this is an AI-generated assessment. Always consult with a senior medical professional before making any changes to a patient's prescription."
    
    return response

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
