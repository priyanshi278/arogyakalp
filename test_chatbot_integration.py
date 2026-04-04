import sys
from unittest.mock import MagicMock

# Mock transformers before importing models
sys.modules['transformers'] = MagicMock()
mock_pipeline = MagicMock()
sys.modules['transformers'].pipeline = MagicMock(return_value=mock_pipeline)

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_chatbot_flow():
    # Test case 1: Dolo 650
    print("--- Test Case 1: Dolo 650 ---")
    mock_pipeline.return_value = [{"entity_group": "DRUG", "word": "Dolo 650"}]
    payload1 = {"message": "I am taking Dolo 650 for fever, is it safe?"}
    response1 = client.post("/chat", json=payload1)
    print(f"Input: {payload1['message']}")
    print(f"Response: {response1.json()['response']}")
    assert response1.status_code == 200
    assert "paracetamol" in response1.json()['response'].lower()

    # Test case 2: Aspirin
    print("\n--- Test Case 2: Aspirin ---")
    mock_pipeline.return_value = [{"entity_group": "DRUG", "word": "aspirin"}]
    payload2 = {"message": "I take aspirin daily."}
    response2 = client.post("/chat", json=payload2)
    print(f"Input: {payload2['message']}")
    print(f"Response: {response2.json()['response']}")
    assert response2.status_code == 200
    assert "aspirin" in response2.json()['response'].lower()
    assert "side effect" in response2.json()['response'].lower()

    # Test case 3: Interacting Drugs (Aspirin + Ibuprofen)
    print("\n--- Test Case 3: Interacting Drugs ---")
    mock_pipeline.return_value = [
        {"entity_group": "DRUG", "word": "aspirin"},
        {"entity_group": "DRUG", "word": "ibuprofen"}
    ]
    payload3 = {"message": "Can I take aspirin and ibuprofen together?"}
    response3 = client.post("/chat", json=payload3)
    print(f"Input: {payload3['message']}")
    print(f"Response: {response3.json()['response']}")
    assert response3.status_code == 200
    assert "interaction" in response3.json()['response'].lower()

    # Test case 4: No drugs
    print("\n--- Test Case 4: No Drugs ---")
    mock_pipeline.return_value = []
    payload4 = {"message": "Hello, how are you?"}
    response4 = client.post("/chat", json=payload4)
    print(f"Input: {payload4['message']}")
    print(f"Response: {response4.json()['response']}")
    assert response4.status_code == 200
    assert "couldn't identify any specific drugs" in response4.json()['response'].lower()

    print("\nAll integration tests passed!")

if __name__ == "__main__":
    test_chatbot_flow()
