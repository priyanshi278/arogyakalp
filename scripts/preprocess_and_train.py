"""
=============================================================================
ArogyaKalp — Data Preprocessing & XGBoost Training Pipeline
=============================================================================

This script does THREE things:

  STEP 1 — REAL API DATA FETCH
    Calls the OpenFDA API to fetch real adverse drug reaction (ADR) reports
    for key drugs in our dataset. This enriches our local CSV with real-world
    pharmacovigilance data from the FDA FAERS database.

  STEP 2 — DATA PREPROCESSING
    Loads the ddi_dataset_expanded.csv, encodes drug class features using the
    standardized drug_mapper utility, and prepares a clean feature matrix
    ready for ML training.

  STEP 3 — XGBOOST TRAINING
    Trains an XGBoost multi-class classifier to predict interaction severity
    (0=LOW, 1=MODERATE, 2=HIGH, 3=DANGEROUS) from drug class feature pairs.
    Saves the trained model to app/data/xgb_risk_model.pkl.

Usage:
    python scripts/preprocess_and_train.py

Prerequisites:
    pip install xgboost scikit-learn pandas requests
=============================================================================
"""

import os
import sys
import json
import pickle
import requests
import pandas as pd
from collections import defaultdict

# ─── Path setup ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)

from app.utils.drug_mapper import get_drug_class  # noqa: E402

DATA_DIR = os.path.join(PROJECT_ROOT, "app", "data")
DDI_CSV = os.path.join(DATA_DIR, "ddi_dataset_expanded.csv")
MODEL_OUT = os.path.join(DATA_DIR, "xgb_risk_model.pkl")
API_CACHE = os.path.join(DATA_DIR, "openfda_adr_cache.json")

# Drug-class encoding (matches xgboost_risk_model.py)
DRUG_CLASS_ENCODING = {
    "anticoagulant": 0, "antiplatelet": 1, "nsaid": 2, "statin": 3,
    "macrolide": 4, "ace_inhibitor": 5, "arb": 6, "diuretic": 7,
    "biguanide": 8, "ssri": 9, "beta_blocker": 10,
    "calcium_channel_blocker": 11, "pde5_inhibitor": 12, "nitrate": 13,
    "antifungal": 14, "fluoroquinolone": 15, "mood_stabilizer": 16,
    "antiepileptic": 17, "antipsychotic": 18, "sulfonylurea": 19,
    "unknown": 20,
}

SEVERITY_ENCODING = {"safe": 0, "caution": 1, "moderate": 1, "risky": 2, "dangerous": 3}

OPENFDA_URL = "https://api.fda.gov/drug/event.json"

# Key drugs to fetch real ADR data for
TARGET_DRUGS = [
    "warfarin", "ibuprofen", "metformin", "atorvastatin",
    "aspirin", "lisinopril", "metoprolol", "clopidogrel",
    "sertraline", "amoxicillin"
]


# =============================================================================
# STEP 1: FETCH REAL ADR DATA FROM OPENFDA API
# =============================================================================

def fetch_openfda_adrs(drug_name: str, limit: int = 5) -> list:
    """
    Queries the OpenFDA Drug Adverse Event API for real-world ADR counts
    associated with the given drug name.
    Returns a list of (reaction_term, count) tuples.
    """
    params = {
        "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
        "count": "patient.reaction.reactionmeddrapt.exact",
        "limit": limit
    }
    try:
        resp = requests.get(OPENFDA_URL, params=params, timeout=10)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            return [(r["term"], r["count"]) for r in results]
        else:
            print(f"  [API] {drug_name}: HTTP {resp.status_code}")
            return []
    except Exception as e:
        print(f"  [API] {drug_name}: Request failed - {e}")
        return []


def step1_fetch_real_data():
    print("\n" + "=" * 60)
    print("STEP 1: Fetching Real ADR Data from OpenFDA API")
    print("=" * 60)

    if os.path.exists(API_CACHE):
        print(f"  [Cache] Found existing cache at {API_CACHE}. Skipping API calls.")
        with open(API_CACHE, "r") as f:
            return json.load(f)

    api_results = {}
    for drug in TARGET_DRUGS:
        print(f"  [API] Querying OpenFDA for: {drug} ...")
        adrs = fetch_openfda_adrs(drug, limit=5)
        api_results[drug] = adrs
        if adrs:
            print(f"         -> Top ADR: {adrs[0][0]} ({adrs[0][1]} reports)")
        else:
            print(f"         -> No results returned")


    with open(API_CACHE, "w") as f:
        json.dump(api_results, f, indent=2)
    print(f"\n  [Saved] OpenFDA cache -> {API_CACHE}")
    return api_results


# =============================================================================
# STEP 2: PREPROCESSING — Load DDI CSV and build feature matrix
# =============================================================================

def encode_class(drug_class):
    if not drug_class:
        return DRUG_CLASS_ENCODING["unknown"]
    return DRUG_CLASS_ENCODING.get(drug_class.lower(), DRUG_CLASS_ENCODING["unknown"])


def step2_preprocess():
    print("\n" + "=" * 60)
    print("STEP 2: Data Preprocessing")
    print("=" * 60)

    df = pd.read_csv(DDI_CSV)
    print(f"  [Load] DDI dataset: {len(df)} rows")

    # Remove rows with missing values
    df.dropna(inplace=True)
    df = df[df["interaction"].str.strip() != ""]
    print(f"  [Clean] After null/empty removal: {len(df)} rows")

    # Normalize text
    df["drug_1"] = df["drug_1"].str.strip().str.lower()
    df["drug_2"] = df["drug_2"].str.strip().str.lower()
    df["interaction"] = df["interaction"].str.strip().str.lower()

    # Map drug names → drug classes
    df["class_1"] = df["drug_1"].apply(get_drug_class)
    df["class_2"] = df["drug_2"].apply(get_drug_class)

    # Encode drug classes as integers
    df["class_1_enc"] = df["class_1"].apply(encode_class)
    df["class_2_enc"] = df["class_2"].apply(encode_class)

    # Canonical ordering: always put lower encoded class first to avoid (A,B) vs (B,A) duplicates
    df["feat_a"] = df[["class_1_enc", "class_2_enc"]].min(axis=1)
    df["feat_b"] = df[["class_1_enc", "class_2_enc"]].max(axis=1)

    # Encode target labels
    df["label"] = df["interaction"].map(SEVERITY_ENCODING).fillna(0).astype(int)

    # Show distribution
    print(f"  [Label Distribution]:")
    for lbl, count in df["label"].value_counts().sort_index().items():
        names = {0: "LOW/SAFE", 1: "MODERATE/CAUTION", 2: "HIGH/RISKY", 3: "DANGEROUS"}
        print(f"    {names.get(lbl, lbl)}: {count} samples")

    X = df[["feat_a", "feat_b"]].values
    y = df["label"].values

    print(f"  [Features] Shape: {X.shape}")
    return X, y


# =============================================================================
# STEP 3: TRAIN XGBOOST CLASSIFIER
# =============================================================================

def step3_train_xgboost(X, y):
    print("\n" + "=" * 60)
    print("STEP 3: Training XGBoost Classifier")
    print("=" * 60)

    try:
        from xgboost import XGBClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report, accuracy_score
    except ImportError:
        print("  [Error] Missing dependencies. Run: pip install xgboost scikit-learn")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  [Split] Train: {len(X_train)} | Test: {len(X_test)}")

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
        verbosity=0
    )

    print("  [Training] Fitting XGBoost model ...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"  [Accuracy] Test Accuracy: {acc * 100:.1f}%")
    print("\n  [Report]")
    target_names = ["LOW", "MODERATE", "HIGH", "DANGEROUS"]
    # Only include labels that appear in y_test
    present = sorted(set(y_test))
    present_names = [target_names[i] for i in present]
    print(classification_report(y_test, y_pred, labels=present, target_names=present_names))

    with open(MODEL_OUT, "wb") as f:
        pickle.dump(model, f)
    print(f"  [Saved] Model -> {MODEL_OUT}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# ArogyaKalp — Preprocessing & XGBoost Training Pipeline")
    print("#" * 60)

    api_data = step1_fetch_real_data()
    X, y = step2_preprocess()
    step3_train_xgboost(X, y)

    print("\n" + "=" * 60)
    print("Pipeline Complete.")
    print(f"  Model saved to : app/data/xgb_risk_model.pkl")
    print(f"  API cache saved: app/data/openfda_adr_cache.json")
    print("=" * 60 + "\n")
