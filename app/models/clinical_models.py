from pydantic import BaseModel
from typing import List, Optional

class ReasoningRequest(BaseModel):
    current_drugs: List[str] = []
    new_drug: str
    patient_status: List[str] = []

class SideEffect(BaseModel):
    effect: str
    severity: str

class RecommendationOutput(BaseModel):
    action: str
    alternative: Optional[str] = None
    why: Optional[str] = None

class ClinicalAnalysisResponse(BaseModel):
    risk_level: str
    risk_score: int
    reason: List[str]
    side_effects: List[SideEffect]
    recommendation: RecommendationOutput
