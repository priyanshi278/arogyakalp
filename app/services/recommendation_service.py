import pandas as pd
import os
from typing import List
from app.models.ner_model import DrugEntity, ADRPrediction, DrugInteraction, Recommendation

class RecommendationService:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.alternatives = {}
        self._load_dataset()

    def _load_dataset(self):
        """
        Loads the drug alternatives dataset into a dictionary for lookup.
        """
        if not os.path.exists(self.dataset_path):
            print(f"Warning: Drug alternatives dataset not found at {self.dataset_path}")
            return
            
        try:
            df = pd.read_csv(self.dataset_path)
            for _, row in df.iterrows():
                drug = str(row['drug_name']).strip().lower()
                alt = str(row['alternative']).strip().lower()
                # Store the first alternative found for each drug
                if drug not in self.alternatives:
                    self.alternatives[drug] = alt
        except Exception as e:
            print(f"Error loading drug alternatives: {e}")

    def get_recommendations(
        self, 
        drugs: List[DrugEntity], 
        adr_predictions: List[ADRPrediction], 
        drug_interactions: List[DrugInteraction]
    ) -> List[Recommendation]:
        """
        Analyzes ADRs and interactions to suggest safer drug alternatives.
        """
        recommendations = []
        flagged_drugs = {} # drug_name -> issue_description

        # 1. Identify drugs with ADR risks
        for adr in adr_predictions:
            if adr.side_effects:
                # Use the first side effect as the issue description
                issue = f"Potential risk of {adr.side_effects[0]}"
                flagged_drugs[adr.drug.lower()] = issue

        # 2. Identify drugs with interaction risks
        for interaction in drug_interactions:
            # Skip if interaction is "no known interaction" or "safe"
            if interaction.interaction.lower() not in ["no known interaction", "safe"]:
                issue = f"Interaction risk: {interaction.interaction}"
                for drug in interaction.drug_pair:
                    # We flag both drugs in the interaction
                    flagged_drugs[drug.lower()] = issue

        # 3. Look up alternatives for flagged drugs
        processed_flags = set()
        for drug_info in drugs:
            drug_lower = drug_info.original.lower()
            generic_lower = drug_info.generic.lower()
            
            # Check if this drug (original or generic) is flagged
            issue = flagged_drugs.get(drug_lower) or flagged_drugs.get(generic_lower)
            
            if issue and drug_lower not in processed_flags:
                # Try to find alternative for both names
                alternative = self.alternatives.get(generic_lower) or self.alternatives.get(drug_lower)
                
                if alternative:
                    recommendations.append(Recommendation(
                        drug=drug_info.original,
                        issue=issue,
                        alternative=alternative
                    ))
                    processed_flags.add(drug_lower)

        return recommendations

# Singleton instance
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "drug_alternatives.csv")
recommendation_service = RecommendationService(data_path)
