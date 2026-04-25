from app.services.ddi_service import ddi_service
from app.services.adr_service import adr_service
from app.services.recommendation_service import recommendation_service
from app.utils.drug_mapper import get_drug_class

def validate_cleanup():
    print("--- Post-Cleanup Validation ---")
    
    # 1. Check DDI Loading
    print(f"DDI Dataset: {len(ddi_service.interactions)} entries loaded.")
    assert len(ddi_service.interactions) > 0
    
    # 2. Check ADR Loading
    print(f"ADR Dataset: {len(adr_service.adr_data)} drugs loaded.")
    assert len(adr_service.adr_data) > 0
    
    # 3. Check Recommendation Loading
    print(f"Recommendation Dataset: {len(recommendation_service.alternatives)} drugs loaded.")
    assert len(recommendation_service.alternatives) > 0
    
    # 4. Check Drug Class Mapping
    test_class = get_drug_class("aspirin")
    print(f"Drug Class Mapping: aspirin -> {test_class}")
    assert test_class == "antiplatelet"

    print("\nSYSTEM STABILITY VERIFIED!")

if __name__ == "__main__":
    validate_cleanup()
