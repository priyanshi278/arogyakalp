from fastapi import APIRouter
from app.models.ner_model import NERRequest, CDSSResponse
from app.models.clinical_models import ReasoningRequest, ClinicalAnalysisResponse
from app.services.ner_service import NERService
from app.services.clinical_reasoning_service import clinical_reasoning_service

router = APIRouter()
ner_service = NERService()

@router.post("/extract_entities", response_model=CDSSResponse)
async def extract_entities_endpoint(request: NERRequest):
    """
    Endpoint to extract entities using NER logic.
    """
    return ner_service.extract_entities(request.text)

@router.post("/analyze_clinical_risk", response_model=ClinicalAnalysisResponse)
async def analyze_clinical_risk_endpoint(request: ReasoningRequest):
    """
    Advanced clinical reasoning engine for drug interaction and patient risk.
    """
    return clinical_reasoning_service.analyze(request)
