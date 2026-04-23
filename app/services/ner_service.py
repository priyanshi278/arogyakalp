from app.utils.preprocessing import preprocess_text
from app.models.ner_model import NERResponse, DrugEntity, ADRPrediction, DrugInteraction, ner_pipeline
from app.utils.drug_mapper import normalize_drug_name
from app.services.adr_service import adr_service
from app.services.ddi_service import ddi_service
from app.services.recommendation_service import recommendation_service
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
        
        # Extract patient name and new drug to filter/focus analysis
        patient_name = ""
        new_drug_name = ""
        import re
        
        name_match = re.search(r"Patient Name:\s*(.*)", text)
        if name_match:
            patient_name = name_match.group(1).strip().lower()
            
        new_drug_match = re.search(r"New Drug Prescribed:\s*-?\s*(.*)", text)
        if new_drug_match:
            new_drug_name = new_drug_match.group(1).strip().lower()

        # Explicitly extract conditions and allergies from the text sections
        conditions_match = re.search(r"Existing Conditions:\s*(.*?)(?:\n\n|\n[A-Z]|$)", text, re.DOTALL | re.IGNORECASE)
        if conditions_match:
            conditions_text = conditions_match.group(1).strip()
            # Split by commas or newlines/bullets
            for cond in re.split(r'[,\n-]', conditions_text):
                c = cond.strip().strip("- ")
                if c and len(c) > 2:
                    diseases.append(c)

        allergies_match = re.search(r"Known Allergies:\s*(.*?)(?:\n\n|\n[A-Z]|$)", text, re.DOTALL | re.IGNORECASE)
        if allergies_match:
            allergies_text = allergies_match.group(1).strip()
            if allergies_text.lower() != "none":
                for alg in re.split(r'[,\n-]', allergies_text):
                    a = alg.strip().strip("- ")
                    if a and len(a) > 2:
                        allergies.append(a)
        
        # Map labels and merge subword tokens
        processed_results = []
        for entity in results:
            label = entity.get("entity_group", "")
            word = entity.get("word", "").strip()
            
            if not word:
                continue
                
            # If it's a subword token, merge it with the previous one regardless of label
            if word.startswith("##") and processed_results:
                processed_results[-1]["word"] += word[2:]
                continue
            
            processed_results.append({"label": label, "word": word})

        for entity in processed_results:
            label = entity["label"]
            word = entity["word"]
            
            # Clean: remove symbols and hashtags
            clean_word = word.replace("#", "").strip(" -_")
            
            # Skip if it's too short and not alphanumeric (noise)
            if len(clean_word) < 2 and not clean_word.isalnum():
                continue
            
            if label in ["Medication", "DRUG", "CHEMICAL"]:
                lower_word = clean_word.lower()
                
                # Skip if it matches patient name or common noise
                if patient_name and (lower_word in patient_name or patient_name in lower_word):
                    continue
                if lower_word in ["patient", "name", "age", "years", "gender", "male", "female"]:
                    continue

                if lower_word not in added_drugs:
                    generic_name = normalize_drug_name(clean_word)
                    drugs.append(DrugEntity(original=clean_word, generic=generic_name))
                    added_drugs.add(lower_word)
                    generic_drug_names.append(generic_name)
                    
                    # ONLY Predict ADR for the NEW drug
                    is_new_drug = new_drug_name and (lower_word in new_drug_name or new_drug_name in lower_word)
                    
                    if is_new_drug:
                        side_effects = adr_service.predict_adr(generic_name)
                        if side_effects:
                            adr_predictions.append(ADRPrediction(drug=clean_word, side_effects=side_effects))
                        
            elif label in ["Disease_disorder", "Sign_symptom", "DISEASE", "DISORDER"]:
                if clean_word.lower() not in [d.lower() for d in diseases]:
                    diseases.append(clean_word)
            elif label in ["Biological_structure", "ALLERGEN"]:
                if clean_word.lower() not in [a.lower() for a in allergies]:
                    allergies.append(clean_word)
        
        # Check for Drug-Drug Interactions (DDI)
        drug_interactions = []
        if len(generic_drug_names) >= 2:
            interaction_results = ddi_service.check_interactions(generic_drug_names)
            for res in interaction_results:
                drug_interactions.append(DrugInteraction(
                    drug_pair=res["drug_pair"],
                    interaction=res["interaction"]
                ))
        
        # Get recommendations but filter to only those concerning the new drug
        all_recommendations = recommendation_service.get_recommendations(drugs, adr_predictions, drug_interactions)
        filtered_recommendations = [
            r for r in all_recommendations 
            if new_drug_name and (r.drug.lower() in new_drug_name or new_drug_name in r.drug.lower())
        ]
                    
        return NERResponse(
            drugs=drugs,
            diseases=diseases,
            allergies=allergies,
            adr_predictions=adr_predictions,
            drug_interactions=drug_interactions,
            recommendations=filtered_recommendations
        )
