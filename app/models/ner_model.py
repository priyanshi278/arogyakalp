from pydantic import BaseModel
from typing import List, Optional, Dict
from transformers import pipeline

# Load pretrained biomedical NER pipeline once
ner_pipeline = pipeline(
    "ner", 
    model="d4data/biomedical-ner-all", 
    aggregation_strategy="simple"
)

class NERRequest(BaseModel):
    text: str

class RecommendationDict(BaseModel):
    decision: str
    drug: str
    alternative: str
    reason: str
    monitoring: str

class AnalysisDict(BaseModel):
    mechanism: str
    impact: str
    risk_factors: str
    outcome: str

class CDSSDDI(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    meaning: str

class CDSSADR(BaseModel):
    drug: str
    effects: List[str]

class CDSSResponse(BaseModel):
    risk_level: str
    alerts: List[str]
    recommendation: RecommendationDict
    analysis: AnalysisDict
    ddi: List[CDSSDDI]
    adr: List[CDSSADR]
