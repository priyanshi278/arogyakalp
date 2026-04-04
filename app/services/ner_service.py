from app.utils.preprocessing import preprocess_text
from app.models.ner_model import NERResponse, DrugEntity, ner_pipeline
from app.utils.drug_mapper import normalize_drug_name
from typing import List

class NERService:
    def __init__(self):
        # The model is loaded once in ner_model.py
        pass

    def extract_entities(self, text: str) -> NERResponse:
        """
        Extract drugs, diseases, and allergies using a transformer pipeline.
        """
        if not text or not text.strip():
            return NERResponse(drugs=[], diseases=[], allergies=[])

        original_text = text
        # Keep preprocessing as requested
        clean_text = preprocess_text(text)
        
        # Call model for predictions
        results = ner_pipeline(clean_text)
        
        drugs = []
        diseases = []
        allergies = []
        
        # We'll use a set to keep track of added drug originals to avoid duplicates
        added_drugs = set()
        
        # Categorize results
        # Mapping logic:
        # DRUG -> drugs
        # DISEASE -> diseases
        # CHEMICAL / ALLERGEN -> allergies
        for entity in results:
            label = entity.get("entity_group", "")
            word = entity.get("word", "").strip()
            
            if not word:
                continue
                
            if label == "DRUG":
                if word not in added_drugs:
                    generic_name = normalize_drug_name(word)
                    drugs.append(DrugEntity(original=word, generic=generic_name))
                    added_drugs.add(word)
            elif label == "DISEASE" or label == "DISORDER":
                if word not in diseases:
                    diseases.append(word)
            elif label == "CHEMICAL" or label == "ALLERGEN":
                if word not in allergies:
                    allergies.append(word)
                    
        return NERResponse(
            drugs=drugs,
            diseases=diseases,
            allergies=allergies
        )
