# 🧠 ArogyaKalp - AI-Powered Clinical Decision Support System

ArogyaKalp is an AI-based Clinical Decision Support System (CDSS) designed to improve patient safety by detecting adverse drug reactions (ADRs) and drug-drug interactions (DDIs). It assists doctors in making safer prescribing decisions using intelligent analysis of patient data.

---

## 🚀 Key Features

- 🔐 **Secure Doctor Authentication**
  Login and Signup system using Indian Medical Registration (IMR) numbers for verified access.

- 📝 **Structured Patient Assessment**
  Comprehensive grid-based input for patient name, age, gender, conditions, and medications.

- 🔍 **Entity Extraction (NER)**  
  Identifies drugs, diseases, and allergies from clinical input using Bio-Medical NLP.

- ⚠️ **ADR Prediction**  
  Predicts potential adverse drug reactions for newly prescribed medications.

- 🔗 **Drug-Drug Interaction Detection**  
  Identifies harmful combinations between new prescriptions and current medications.

- 💬 **Smart Clinical Assessment**
  Generates a human-readable safety summary in plain English for quick decision-making.

---

## 🏗️ Project Structure

```text
arogyakalp/
├── app/                        # Backend (FastAPI)
│   ├── api/                    # API Endpoints (Auth, NER, Chatbot)
│   ├── services/               # Logic (ADR, DDI, Recommendation)
│   ├── models/                 # Data Models (Pydantic)
│   ├── utils/                  # Helpers (Text preprocessing, Drug mapping)
│   └── data/                   # Knowledge Bases (JSON/CSV Datasets)
├── frontend/                   # Frontend (React + Vite)
│   ├── src/                    # Components (LoginPage, InputSection, Header)
│   └── public/                 # Assets
├── venv/                       # Python Virtual Environment (Ignored)
├── requirements.txt            # Python Dependencies
└── README.md                   # Project Documentation
```

---

## 🛠️ Setup Instructions for Team Members

### 1. Backend Setup (Python)
From the project root:
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup (React)
From the project root:
```powershell
cd frontend
npm install
```

---

## 🏃 Running the Application

### Step 1: Start the Backend
```powershell
uvicorn app.main:app --reload --port 8000
```

### Step 2: Start the Frontend
In a **new** terminal:
```powershell
cd frontend
npm run dev
```
Open **http://localhost:5173** to access the dashboard.

---

## 🧪 Test Credentials
You can use the following to log in immediately:
- **IMR Number**: `IMR-12345`
- **IMR Number**: `IMR-TEST`

---

## 🧬 Roadmap
- [ ] Integration of BioBERT for deep-learning-based NER.
- [ ] Support for multi-lingual clinical notes (Hindi/English).
- [ ] Database integration for persistent patient history.
- [ ] Advanced visualization for drug interaction networks.

---

## 📫 Stay Connected
- **Repo**: [priyanshi278/arogyakalp](https://github.com/priyanshi278/arogyakalp)
- **Contributors**: Please pull the latest changes before starting work.
- **Support**: Open an issue on GitHub for any technical bugs.
