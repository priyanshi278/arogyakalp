import pandas as pd
import os
from typing import List, Dict, Tuple
from itertools import combinations

class DDIService:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.interactions = {}
        self._load_dataset()

    def _load_dataset(self):
        """
        Loads the DDI dataset and standardizes drug names for fast lookup.
        """
        if not os.path.exists(self.dataset_path):
            # If dataset doesn't exist, log error (or handle it)
            print(f"Warning: DDI dataset not found at {self.dataset_path}")
            return
            
        df = pd.read_csv(self.dataset_path)
        for _, row in df.iterrows():
            d1 = row['drug_1'].strip().lower()
            d2 = row['drug_2'].strip().lower()
            interaction = row['interaction'].strip().lower()
            
            # Use a sorted tuple to ensure order doesn't matter for matching
            pair = tuple(sorted([d1, d2]))
            self.interactions[pair] = interaction

    def check_interactions(self, drugs: List[str]) -> List[Dict]:
        """
        Takes a list of normalized (generic) drug names and checks for all pairs.
        Returns a list of interaction results.
        """
        if len(drugs) < 2:
            return []
            
        results = []
        # Generate all unique pairs from the list of drugs
        processed_drugs = [d.strip().lower() for d in drugs if d]
        unique_drug_list = sorted(list(set(processed_drugs)))
        
        drug_pairs = list(combinations(unique_drug_list, 2))
        
        for p1, p2 in drug_pairs:
            # Check both directions by sorting
            pair_key = tuple(sorted([p1, p2]))
            interaction = self.interactions.get(pair_key, "no known interaction")
            
            # Format output as requested
            results.append({
                "drug_pair": [p1, p2],
                "interaction": interaction
            })
            
        return results

# Singleton instance to be loaded at startup
dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "ddi_dataset_expanded.csv")
ddi_service = DDIService(dataset_path)
