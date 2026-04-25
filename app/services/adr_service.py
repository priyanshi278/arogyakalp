import pandas as pd
import os
from typing import List, Dict

class ADRService:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.adr_data = {} # drug -> List[dict]
        self._load_dataset()

    def _load_dataset(self):
        if not os.path.exists(self.dataset_path):
            print(f"Warning: ADR dataset not found at {self.dataset_path}")
            return
            
        try:
            df = pd.read_csv(self.dataset_path)
            for _, row in df.iterrows():
                drug = str(row['drug_name']).strip().lower()
                effect = {
                    "effect": str(row['side_effect']).strip().lower(),
                    "severity": str(row.get('severity', 'moderate')).strip().lower()
                }
                if drug not in self.adr_data:
                    self.adr_data[drug] = []
                self.adr_data[drug].append(effect)
        except Exception as e:
            print(f"Error loading ADR dataset: {e}")

    def get_adrs(self, drug_name: str, patient_status: List[str] = []) -> List[Dict]:
        """
        Returns serious ADRs first, excluding mild common ones.
        Injects critical ADRs if patient context (e.g. kidney disease) warrants it.
        """
        drug_lower = drug_name.lower().strip()
        effects = self.adr_data.get(drug_lower, [])
        status_str = " ".join([s.lower() for s in patient_status])
        has_renal = any(k in status_str for k in ["kidney", "renal", "impairment"])
        
        # Contextual Injection
        contextual = []
        if drug_lower == "metformin" and has_renal:
            contextual.append({"effect": "lactic acidosis", "severity": "serious"})
        if "nsaid" in str(drug_lower) or drug_lower in ["diclofenac", "ibuprofen", "naproxen"] and has_renal:
            contextual.append({"effect": "acute kidney injury", "severity": "serious"})
        
        # Combine
        all_effects = contextual + effects
        
        # Filter out mild symptoms
        mild_symptoms = ["nausea", "headache", "dizziness", "heartburn", "indigestion", "tiredness"]
        filtered_effects = []
        seen = set()
        for e in all_effects:
            eff_low = e['effect'].lower()
            if eff_low not in mild_symptoms and eff_low not in seen:
                filtered_effects.append(e)
                seen.add(eff_low)
        
        # Sort by severity (serious first)
        severity_priority = {"serious": 0, "moderate": 1, "common": 2}
        sorted_effects = sorted(filtered_effects, key=lambda x: severity_priority.get(x['severity'], 99))
        
        return sorted_effects[:2]

    def predict_adr(self, drug_name: str) -> List[str]:
        """
        Backward compatibility: returns just the effect names.
        """
        adrs = self.get_adrs(drug_name)
        return [a['effect'] for a in adrs]

# Singleton instance
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "adr_dataset_expanded.csv")
adr_service = ADRService(data_path)
