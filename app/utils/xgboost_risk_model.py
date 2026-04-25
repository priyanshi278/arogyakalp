"""
XGBoost Risk Model Utility
--------------------------
Loads the pre-trained XGBoost classifier (trained via scripts/preprocess_and_train.py)
and provides a predict_risk() helper used by the DDI service as a secondary validator.
"""

import os
import pickle
from typing import Optional

# Drug-class encoding map (must match what was used during training)
DRUG_CLASS_ENCODING = {
    "anticoagulant": 0,
    "antiplatelet": 1,
    "nsaid": 2,
    "statin": 3,
    "macrolide": 4,
    "ace_inhibitor": 5,
    "arb": 6,
    "diuretic": 7,
    "biguanide": 8,
    "ssri": 9,
    "beta_blocker": 10,
    "calcium_channel_blocker": 11,
    "pde5_inhibitor": 12,
    "nitrate": 13,
    "antifungal": 14,
    "fluoroquinolone": 15,
    "mood_stabilizer": 16,
    "antiepileptic": 17,
    "antipsychotic": 18,
    "sulfonylurea": 19,
    "unknown": 20,
}

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "xgb_risk_model.pkl")


class XGBoostRiskModel:
    def __init__(self):
        self.model = None
        self._load()

    def _load(self):
        """Load the trained XGBoost model from disk if available."""
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
            except Exception as e:
                print(f"[XGBoost] Could not load model: {e}")

    def _encode_class(self, drug_class: Optional[str]) -> int:
        if not drug_class:
            return DRUG_CLASS_ENCODING["unknown"]
        return DRUG_CLASS_ENCODING.get(drug_class.lower(), DRUG_CLASS_ENCODING["unknown"])

    def predict_risk(self, drug_class_1: Optional[str], drug_class_2: Optional[str]) -> Optional[int]:
        """
        Returns a predicted risk score (0=LOW, 1=MODERATE, 2=HIGH, 3=DANGEROUS)
        for the given pair of drug classes.
        Returns None if model is not loaded.
        """
        if self.model is None:
            return None
        try:
            c1 = self._encode_class(drug_class_1)
            c2 = self._encode_class(drug_class_2)
            features = [[min(c1, c2), max(c1, c2)]]   # canonical ordering
            prediction = self.model.predict(features)
            return int(prediction[0])
        except Exception as e:
            print(f"[XGBoost] Prediction error: {e}")
            return None


# Singleton
xgb_risk_model = XGBoostRiskModel()
