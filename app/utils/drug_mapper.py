import pandas as pd
import os

DRUG_MAPPING = {
    "dolo 650": "paracetamol",
    "crocin": "paracetamol",
    "brufen": "ibuprofen",
    "augmentin": "amoxicillin",
    "lipitor": "atorvastatin",
    "advil": "ibuprofen",
    "motrin": "ibuprofen",
    "ascriptin": "aspirin",
    "bayer": "aspirin",
    "aleve": "naproxen",
    "zithromax": "azithromycin",
    "plavix": "clopidogrel",
    "lasix": "furosemide",
    "prinivil": "lisinopril",
    "zestril": "lisinopril",
    "cozaar": "losartan",
    "glucophage": "metformin",
    "lopressor": "metoprolol",
    "prilosec": "omeprazole",
    "zoloft": "sertraline",
    "coumadin": "warfarin",
    "lantus": "insulin glargine",
    "vicodin": "hydrocodone/paracetamol"
}

# Cache for drug classes
_DRUG_CLASSES = None

def normalize_drug_name(drug_name: str) -> str:
    """
    Normalizes a drug brand name to its generic name using a predefined mapping.
    Performs case-insensitive matching.
    """
    if not drug_name:
        return drug_name
    
    normalized = drug_name.strip().lower()
    generic_name = DRUG_MAPPING.get(normalized)
    
    if generic_name:
        return generic_name
    return normalized

def get_drug_class(drug_name: str) -> str:
    """
    Retrieves the drug class for a given generic drug name.
    """
    global _DRUG_CLASSES
    if _DRUG_CLASSES is None:
        _load_drug_classes()
    
    generic_name = normalize_drug_name(drug_name)
    return _DRUG_CLASSES.get(generic_name, "unknown")

def _load_drug_classes():
    global _DRUG_CLASSES
    _DRUG_CLASSES = {}
    path = os.path.join(os.path.dirname(__file__), "..", "data", "drug_class_dataset.csv")
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                _DRUG_CLASSES[str(row['drug_name']).lower()] = str(row['drug_class']).lower()
        except Exception as e:
            print(f"Error loading drug classes: {e}")
