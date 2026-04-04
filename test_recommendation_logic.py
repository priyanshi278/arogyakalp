import sys
from unittest.mock import MagicMock

# Mock transformers before importing models
sys.modules['transformers'] = MagicMock()
sys.modules['transformers'].pipeline = MagicMock()

from app.services.recommendation_service import RecommendationService
from app.models.ner_model import DrugEntity, ADRPrediction, DrugInteraction, Recommendation
import json

def test_recommendation_logic():
    # Use the absolute path if needed, but relative should work in the Cwd
    service = RecommendationService("app/data/drug_alternatives.csv")
    
    # Mock data
    drugs = [
        DrugEntity(original="Aspirin", generic="aspirin"),
        DrugEntity(original="Ibuprofen", generic="ibuprofen")
    ]
    
    # 1. Test ADR Case
    print("--- Test ADR Case ---")
    adr_predictions = [
        ADRPrediction(drug="Aspirin", side_effects=["stomach pain"])
    ]
    interactions = []
    
    recs = service.get_recommendations(drugs, adr_predictions, interactions)
    print(f"Recommendations: {json.dumps([r.dict() for r in recs], indent=2)}")
    assert len(recs) == 1
    assert recs[0].drug == "Aspirin"
    assert "clopidogrel" in recs[0].alternative.lower()

    # 2. Test Interaction Case
    print("\n--- Test Interaction Case ---")
    adr_predictions = []
    interactions = [
        DrugInteraction(drug_pair=["aspirin", "ibuprofen"], interaction="increased bleeding risk")
    ]
    
    recs = service.get_recommendations(drugs, adr_predictions, interactions)
    print(f"Recommendations: {json.dumps([r.dict() for r in recs], indent=2)}")
    # Both aspirin and ibuprofen should be flagged if they interact
    assert len(recs) == 2
    drug_names = [r.drug.lower() for r in recs]
    assert "aspirin" in drug_names
    assert "ibuprofen" in drug_names

    print("\nAll logical checks passed!")

if __name__ == "__main__":
    test_recommendation_logic()
