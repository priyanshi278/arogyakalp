import pandas as pd
import os
from typing import List, Dict, Optional


class RecommendationService:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.alternatives = {}
        self._load_dataset()

    def _load_dataset(self):
        if not os.path.exists(self.dataset_path): return
        try:
            df = pd.read_csv(self.dataset_path)
            for _, row in df.iterrows():
                drug = str(row['drug']).strip().lower()
                alt_data = {
                    "name": str(row['alternative']).strip().lower(),
                    "condition": str(row.get('condition', 'any')).strip().lower(),
                    "priority": str(row.get('priority', 'reserve')).strip().lower(),
                    "avoid_if": [s.strip().lower() for s in str(row.get('avoid_if', '')).split(',') if s.strip()],
                    "reason": str(row.get('reason', 'safer alternative')).strip()
                }
                if drug not in self.alternatives: self.alternatives[drug] = []
                self.alternatives[drug].append(alt_data)
        except: pass

    def suggest_alternative(self, drug: str, patient_status: List[str]) -> Optional[Dict]:
        drug_lower = drug.lower()
        if drug_lower not in self.alternatives: return None
        status_lower = [s.lower() for s in patient_status]
        possible_alts = self.alternatives[drug_lower]
        safe_alts = [a for a in possible_alts if not any(c in status_lower for c in a['avoid_if'])]
        if not safe_alts: return None
        priority_map = {"first_line": 0, "second_line": 1, "reserve": 2}
        safe_alts.sort(key=lambda x: priority_map.get(x['priority'], 99))
        return safe_alts[0]



# Singleton instance
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "drug_alternatives.csv")
recommendation_service = RecommendationService(data_path)
