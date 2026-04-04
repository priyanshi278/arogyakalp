# ArogyaKalp - AI Healthcare System

ArogyaKalp is an AI-powered healthcare assistant designed to extract clinical insights from medical notes. This repository contains the initial phase of the system, focusing on modular architecture and basic Named Entity Recognition (NER).

## 🚀 Phase 1: NER Module (Initial Implementation)

In this phase, we have established a robust, modular backend foundation using FastAPI. The NER logic currently uses high-performance keyword matching as a "dummy" placeholder, ready for future machine learning model integration.

### ✨ Key Features
- **Modular Clean Architecture**: Separated concerns into API, Services, Models, and Utils.
- **Entity Extraction**: Detects Drugs, Diseases, and Allergies from clinical text.
- **Text Preprocessing**: Automated lowercasing and punctuation removal for better accuracy.
- **FastAPI Framework**: High-performance, asynchronous API endpoints with auto-generated documentation.

---

## 📁 Project Structure

```text
arogyakalp/
├── app/
│   ├── main.py                # Fast API application entry point
│   ├── api/
│   │   └── routes.py          # API route definitions (endpoints)
│   ├── services/
│   │   └── ner_service.py     # Core NER logic (Keyword matching)
│   ├── models/
│   │   └── ner_model.py       # Pydantic data models (validation)
│   ├── utils/
│   │   └── preprocessing.py   # Text cleaning utilities
│   └── data/
│       └── sample_clinical_notes.json  # Sample dataset for testing
├── venv/                      # Virtual environment
├── requirements.txt            # Project dependencies
├── test_ner.py                 # Automated test script
└── README.md                   # Project documentation
```

---

## 🛠️ Setup and Installation

### 1. Prerequisites
- Python 3.10 or higher.

### 2. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🏃 Running the Application

To start the FastAPI server, run the following command from the project root:

```powershell
uvicorn app.main:app --reload
```

- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`

---

## 🧪 Testing and Verification

### Automated Testing
We have provided a `test_ner.py` script to verify the API functionality.

```powershell
# Make sure the server is running first!
python test_ner.py
```

**Expected results for sample text:**
- **Input**: "Patient is taking Dolo 650 for fever and has allergy to penicillin"
- **Output**:
  ```json
  {
    "drugs": ["Dolo 650", "penicillin"],
    "diseases": ["fever"],
    "allergies": ["penicillin"]
  }
  ```

### Manual Verification
You can also test the API using `curl` or any API client like Postman:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/extract_entities" `
  -H "Content-Type: application/json" `
  -d '{"text": "Patient with cough taking paracetamol"}'
```

---

## 🧬 Future Scope
- Integration of BioBERT or Spacy-based ML models for advanced NER.
- Addition of ADR (Adverse Drug Reaction) prediction module.
- Integration of a database (PostgreSQL/MongoDB) for clinical record storage.
- Building a frontend dashboard.
