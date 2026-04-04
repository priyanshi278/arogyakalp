from app.utils.preprocessing import preprocess_text
from app.models.ner_model import NERResponse, DrugEntity, ADRPrediction, DrugInteraction, ner_pipeline
from app.utils.drug_mapper import normalize_drug_name
from app.services.adr_service import adr_service
from app.services.ddi_service import ddi_service
from typing import List

class NERService:
    def __init__(self):
        # The model is loaded once in ner_model.py
        pass

    def extract_entities(self, text: str) -> NERResponse:
        """
        Extract drugs, diseases, and allergies using a transformer pipeline.
        Also predicts ADR (Adverse Drug Reaction) and checks for DDI (Drug-Drug Interactions).
        """
        if not text or not text.strip():
            return NERResponse(drugs=[], diseases=[], allergies=[], adr_predictions=[], drug_interactions=[])

        original_text = text
        # Keep preprocessing as requested
        clean_text = preprocess_text(text)
        
        # Call model for predictions
        results = ner_pipeline(clean_text)
        
        drugs = []
        diseases = []
        allergies = []
        adr_predictions = []
        
        # We'll use a set to keep track of added drug originals to avoid duplicates
        added_drugs = set()
        # Keep a list of all generic names for DDI checking
        generic_drug_names = []
        
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
                    generic_drug_names.append(generic_name)
                    
                    # Predict ADR for each drug found
                    # Use generic name for better prediction consistency
                    side_effects = adr_service.predict_adr(generic_name)
                    if side_effects:
                        adr_predictions.append(ADRPrediction(drug=word, side_effects=side_effects))
                        
            elif label == "DISEASE" or label == "DISORDER":
                if word not in diseases:
                    diseases.append(word)
            elif label == "CHEMICAL" or label == "ALLERGEN":
                if word not in allergies:
                    allergies.append(word)
        
        # Check for Drug-Drug Interactions (DDI)
        drug_interactions = []
        if len(generic_drug_names) >= 2:
            interaction_results = ddi_service.check_interactions(generic_drug_names)
            for res in interaction_results:
                drug_interactions.append(DrugInteraction(
                    drug_pair=res["drug_pair"],
                    interaction=res["interaction"]
                ))
                    
        return NERResponse(
            drugs=drugs,
            diseases=diseases,
            allergies=allergies,
            adr_predictions=adr_predictions,
            drug_interactions=drug_interactions
        )
