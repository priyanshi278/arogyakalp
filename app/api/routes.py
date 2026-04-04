from fastapi import APIRouter
from app.models.ner_model import NERRequest, NERResponse
from app.services.ner_service import NERService

router = APIRouter()
ner_service = NERService()

@router.post("/extract_entities", response_model=NERResponse)
async def extract_entities_endpoint(request: NERRequest):
    """
    Endpoint to extract entities using dummy NER logic.
    """
    return ner_service.extract_entities(request.text)
