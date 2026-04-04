from app.utils.preprocessing import preprocess_text
from app.models.ner_model import NERResponse
from typing import List

class NERService:
    def __init__(self):
        # Database of keywords for dummy NER (all lowercase for matching)
        self.drugs_db = {
            "dolo 650": "Dolo 650",
            "penicillin": "penicillin",
            "ibuprofen": "ibuprofen",
            "paracetamol": "paracetamol",
            "metformin": "metformin",
            "amoxicillin": "amoxicillin",
            "aspirin": "aspirin",
            "albuterol": "albuterol"
        }
        
        self.diseases_db = {
            "fever": "fever",
            "cough": "cough",
            "diabetes": "diabetes",
            "asthma": "asthma",
            "hypertension": "hypertension",
            "back pain": "back pain",
            "ear infection": "ear infection",
            "headache": "headache",
            "flu": "flu",
            "shortness of breath": "shortness of breath"
        }
        
        self.allergies_db = {
            "penicillin": "penicillin",
            "peanuts": "peanuts",
            "pollen": "pollen",
            "dust": "dust",
            "soy": "soy", 
            "eggs": "eggs"
        }

    def extract_entities(self, text: str) -> NERResponse:
        """
        Extract drugs, diseases, and allergies using dummy keyword matching.
        """
        original_text = text
        clean_text = preprocess_text(text)
        
        drugs = []
        diseases = []
        allergies = []
        
        # Check for drugs
        for keyword, display_name in self.drugs_db.items():
            if keyword in clean_text:
                drugs.append(display_name)
        
        # Check for diseases
        for keyword, display_name in self.diseases_db.items():
            if keyword in clean_text:
                diseases.append(display_name)
        
        # Check for allergies
        # Simple heuristic: if 'allergy' or 'allergic' is in text, 
        # and a keyword exists, add it to allergies.
        # But let's follow the user's example where 'penicillin' is both drug and allergy.
        # User example output: drugs: [Dolo 650, penicillin], diseases: [fever], allergies: [penicillin]
        # In their example, 'penicillin' is explicitly mentioned as an allergy.
        # "has allergy to penicillin" -> penicillin is allergy.
        # "taking Dolo 650" -> Dolo 650 is drug.
        
        # For dummy logic, let's just check if keywords are present in the entire text first.
        # If we wanted to be smarter, we'd look for "allergy to [X]" but let's keep it simple as requested.
        
        for keyword, display_name in self.allergies_db.items():
            if keyword in clean_text:
                # To distinguish between allergy and drug, we could check context
                # "allergy to penicillin" or "allergic to penicillin"
                if f"allergy to {keyword}" in clean_text or f"allergic to {keyword}" in clean_text:
                    allergies.append(display_name)
                # But wait, in the example "taking Dolo 650 for fever and has allergy to penicillin",
                # both "Dolo 650" and "penicillin" are listed in "drugs".
                # Let's just follow the keyword matching strictly first.
        
        # If I just do keyword matching:
        # If "penicillin" is in text, it goes into "drugs" (if in drugs_db) and "allergies" (if in allergies_db).
        
        # Let's adjust self.extract_entities to be simpler for "dummy" logic.
        
        final_drugs = []
        for keyword, display_name in self.drugs_db.items():
            if keyword in clean_text:
                final_drugs.append(display_name)
                
        final_diseases = []
        for keyword, display_name in self.diseases_db.items():
            if keyword in clean_text:
                final_diseases.append(display_name)
                
        final_allergies = []
        for keyword, display_name in self.allergies_db.items():
            if keyword in clean_text:
                # Heuristic for dummy logic: match if 'allergy to' or 'allergic to' prefix exists
                # OR if it's explicitly mentioned in the notes.
                if f"allergy to {keyword}" in clean_text or f"allergic to {keyword}" in clean_text or f"allergy {keyword}" in clean_text:
                    final_allergies.append(display_name)
        
        return NERResponse(
            drugs=final_drugs,
            diseases=final_diseases,
            allergies=final_allergies
        )
