DRUG_MAPPING = {
    "dolo 650": "paracetamol",
    "crocin": "paracetamol",
    "brufen": "ibuprofen",
    "augmentin": "amoxicillin"
}

def normalize_drug_name(drug_name: str) -> str:
    """
    Normalizes a drug brand name to its generic name using a predefined mapping.
    Performs case-insensitive matching.
    If the drug is not found in the mapping, returns the original name.
    """
    if not drug_name:
        return drug_name
    
    normalized = drug_name.strip()
    # Case-insensitive lookup
    generic_name = DRUG_MAPPING.get(normalized.lower())
    
    if generic_name:
        return generic_name
    return normalized
