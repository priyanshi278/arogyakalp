from app.models.adr_model import adr_model_instance
from typing import List, Dict

class ADRService:
    def __init__(self):
        self.model = adr_model_instance

    def predict_adr(self, generic_name: str) -> List[str]:
        """
        Take a normalized (generic) drug name and return predicted side effects.
        """
        if not generic_name:
            return []
            
        # Get top 3 side effects from the model
        side_effects = self.model.predict(generic_name.lower().strip(), top_n=3)
        
        # Handle "No data available" message if it's the only element
        if len(side_effects) == 1 and "No adverse reaction data available" in side_effects[0]:
            # This is a bit of a custom return value from my ADRModel.predict
            # I'll return empty list for prediction if no data
            return []
            
        return side_effects

# Instantiate service for app-wide use
adr_service = ADRService()
