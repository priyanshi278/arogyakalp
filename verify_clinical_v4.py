from app.services.ner_service import NERService
import sys

# Set output to UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_clinical_v4():
    ner = NERService()
    
    test_case = """
Existing Conditions:
Kidney Disease

Current Medications:
Metformin

New Drug Prescribed:
Diclofenac
"""
    
    print("\n--- Testing Clinical V4 (Inconsistency Fixes) ---")
    res = ner.extract_entities(test_case)
    
    print(f"\nOverall Risk: {res.risk_level}")
    
    print("\nInteractions (Should be escalated to DANGEROUS/RISKY):")
    for itx in res.drug_interactions:
        print(f" - {itx.drug_pair}: {itx.interaction}")
        
    print("\nReasons (Check Indirect Risk and Context Escalation):")
    for r in res.risk_reasons:
        print(f" - {r}")
        
    print("\nADR Predictions (Check Lactic Acidosis / AKI injection):")
    for adr in res.adr_predictions:
        print(f" - {adr.drug}: {adr.side_effects}")

    print("\nRecommendation Analysis:")
    for rec in res.recommendations:
        print(f" - Drug: {rec.drug}")
        print(f" - Assessment: {rec.assessment}")
        print(f" - Alt: {rec.alternative} ({rec.alt_reason})")

if __name__ == "__main__":
    verify_clinical_v4()
