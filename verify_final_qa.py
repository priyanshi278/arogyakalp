from app.services.ner_service import NERService
import json

def verify_final_output_structure():
    print("\n--- Verifying Final Clinical Structure (Low Risk Case) ---")
    ner_service = NERService()
    
    medical_note = """
Patient Name: John Doe
Patient Age: 68 years
Gender: Male

Existing Conditions:
Kidney, Diabetes

Current Medications:
Metformin

New Drug Prescribed:
- Paracetamol
"""
    
    results = ner_service.extract_entities(medical_note)
    
    print(f"\nOVERALL RISK: {results.risk_level}")
    print(f"FINDINGS: {results.risk_reasons}")
    
    assert results.risk_level == "LOW"
    
    reasons_str = " ".join(results.risk_reasons)
    assert "clinically significant" in reasons_str
    assert "monitoring required" in reasons_str.lower()
    assert "caution advised" in reasons_str.lower()
    
    print("\nRECOMMENDATION:")
    rec = results.recommendations[0]
    print(f"Issue: {rec.issue}")
    print(f"Reason: {rec.reason}")
    
    assert "Safe to use at recommended doses" in rec.issue
    assert "Suitable first-line" in rec.alternative
    assert "Monitor renal function" in rec.reason

    print("\nFINAL CLINICAL REFINEMENT VALIDATED!")

if __name__ == "__main__":
    verify_final_output_structure()
