import pandas as pd
import os

def verify_files():
    data_dir = "app/data"
    files = [
        "adr_dataset_expanded.csv",
        "ddi_dataset_expanded.csv",
        "dummy_test_dataset.json"
    ]
    
    print("--- Verifying Generated Datasets ---")
    
    for f in files:
        path = os.path.join(data_dir, f)
        if not os.path.exists(path):
            print(f"ERROR: {f} not found!")
            continue
            
        if f.endswith('.csv'):
            df = pd.read_csv(path)
            print(f"SUCCESS: {f} loaded with {len(df)} rows.")
        elif f.endswith('.json'):
            import json
            with open(path, 'r') as jf:
                data = json.load(jf)
                print(f"SUCCESS: {f} loaded with {len(data)} items.")

def verify_backend_loading():
    print("\n--- Verifying Backend Integration ---")
    try:
        from app.models.adr_model import adr_model_instance
        from app.services.ddi_service import ddi_service
        
        adr_count = len(adr_model_instance.known_drugs)
        ddi_count = len(ddi_service.interactions)
        
        print(f"SUCCESS: ADR Model loaded {adr_count} unique drugs.")
        print(f"SUCCESS: DDI Service loaded {ddi_count} interaction pairs.")
        
    except Exception as e:
        print(f"ERROR during backend loading check: {e}")

if __name__ == "__main__":
    verify_files()
    # verify_backend_loading() # Might fail if dependencies like sklearn aren't installed in the env where this runs
