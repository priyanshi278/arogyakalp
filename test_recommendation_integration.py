from app.services.ner_service import NERService
import json

def test_recommendation_flow():
    ner_service = NERService()
    
    # Test case 1: Drug with ADR (Aspirin)
    print("--- Test Case 1: Drug with ADR (Aspirin) ---")
    text1 = "I am taking aspirin for my heart condition."
    response1 = ner_service.extract_entities(text1)
    print(f"Text: {text1}")
    print(f"Recommendations: {json.dumps([r.dict() for r in response1.recommendations], indent=2)}")
    
    assert len(response1.recommendations) > 0
    assert response1.recommendations[0].drug.lower() == "aspirin"
    assert "clopidogrel" in response1.recommendations[0].alternative.lower()

    # Test case 2: Drug with Interaction (Aspirin and Ibuprofen)
    # Note: I need to check if aspirin and ibuprofen interact in ddi_dataset.csv
    print("\n--- Test Case 2: Drug with Interaction (Aspirin and Ibuprofen) ---")
    text2 = "I am taking aspirin and ibuprofen together."
    response2 = ner_service.extract_entities(text2)
    print(f"Text: {text2}")
    print(f"Recommendations: {json.dumps([r.dict() for r in response2.recommendations], indent=2)}")
    
    # Test case 3: No issues (Safe drug or unknown ADR)
    # "Lisinopril" is in alternatives but not in adr_dataset (it returns "No data available")
    print("\n--- Test Case 3: No issues (Lisinopril) ---")
    text3 = "I am taking lisinopril for high blood pressure."
    response3 = ner_service.extract_entities(text3)
    print(f"Text: {text3}")
    print(f"Recommendations: {json.dumps([r.dict() for r in response3.recommendations], indent=2)}")
    assert len(response3.recommendations) == 0

if __name__ == "__main__":
    test_recommendation_flow()
