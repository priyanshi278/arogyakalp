import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import os

class ADRModel:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self._load_and_train()

    def _load_and_train(self):
        """
        Loads the synthetic dataset and trains a LogisticRegression model.
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        df = pd.read_csv(self.dataset_path)
        
        # Encoders for drug name and side effect
        self.drug_encoder = LabelEncoder()
        self.side_effect_encoder = LabelEncoder()
        
        # We lowercase everything for consistency during training
        df['drug_name'] = df['drug_name'].str.lower().str.strip()
        df['side_effect'] = df['side_effect'].str.lower().str.strip()
        
        X = self.drug_encoder.fit_transform(df['drug_name']).reshape(-1, 1)
        y = self.side_effect_encoder.fit_transform(df['side_effect'])
        
        # Using multi_class='ovr' or 'multinomial' for LogisticRegression
        # Given the small dataset, LogisticRegression with high C or default should work
        self.model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
        self.model.fit(X, y)
        
        # Keep track of known drugs
        self.known_drugs = set(self.drug_encoder.classes_)

    def predict(self, drug_name: str, top_n: int = 3) -> list:
        """
        Predicts top_n possible side effects for a given drug name.
        """
        drug_name = drug_name.lower().strip()
        
        if drug_name not in self.known_drugs:
            return ["No adverse reaction data available for this drug."]
        
        # Encode and predict proba
        drug_encoded = self.drug_encoder.transform([drug_name]).reshape(-1, 1)
        probs = self.model.predict_proba(drug_encoded)[0]
        
        # Get indices of top probabilities
        top_indices = np.argsort(probs)[-top_n:][::-1]
        
        # Decode side effects
        return [self.side_effect_encoder.inverse_transform([idx])[0] for idx in top_indices]

# Singleton instance to be loaded at startup
dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "adr_dataset.csv")
adr_model_instance = ADRModel(dataset_path)
