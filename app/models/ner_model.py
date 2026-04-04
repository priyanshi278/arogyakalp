from pydantic import BaseModel
from typing import List, Optional
from transformers import pipeline

# Load pretrained biomedical NER pipeline once
# model: d4data/biomedical-ner-all
# It handles entities like DISEASE, CHEMICAL, DRUG, etc.
ner_pipeline = pipeline(
    "ner", 
    model="d4data/biomedical-ner-all", 
    aggregation_strategy="simple"
)

class NERRequest(BaseModel):
    text: str

class DrugEntity(BaseModel):
    original: str
    generic: str

class ADRPrediction(BaseModel):
    drug: str
    side_effects: List[str]

class DrugInteraction(BaseModel):
    drug_pair: List[str]
    interaction: str

class NERResponse(BaseModel):
    drugs: List[DrugEntity]
    diseases: List[str]
    allergies: List[str]
    adr_predictions: List[ADRPrediction] = []
    drug_interactions: List[DrugInteraction] = []
