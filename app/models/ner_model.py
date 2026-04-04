from pydantic import BaseModel
from typing import List
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

class NERResponse(BaseModel):
    drugs: List[str]
    diseases: List[str]
    allergies: List[str]
