<<<<<<< HEAD
# ArogyaKalp - AI-Powered Healthcare Assistant

ArogyaKalp is a comprehensive clinical decision support system (CDSS) designed to enhance patient safety by analyzing medical notes for potential risks. The system leverages Named Entity Recognition (NER), Adverse Drug Reaction (ADR) prediction, Drug-Drug Interaction (DDI) detection, and provides safer medication recommendations through an intuitive chatbot interface.

---

## ✨ Key Features

- **Entity Extraction (NER)**: Automatically identifies Drugs, Diseases, and Allergies from clinical text.
- **ADR Prediction**: Predicts potential side effects for identified medications.
- **DDI Detection**: Identifies dangerous interactions between multiple prescribed drugs.
- **Smart Recommendations**: Suggests safer alternatives when clinical risks are detected.
- **Interactive Chatbot**: A natural language interface for healthcare providers to query patient data and receive safety alerts.
- **Modern Frontend**: A responsive, high-performance dashboard built with React and Vite.

---

## 📁 Project Structure

```text
arogyakalp/
├── app/                        # Backend (FastAPI)
│   ├── main.py                 # Application entry point
│   ├── api/                    # API route definitions
│   │   ├── routes.py           # Core extraction endpoints
│   │   └── chatbot_routes.py   # NLP chatbot endpoints
│   ├── services/               # Business logic
│   │   ├── ner_service.py      # NER & Pipeline Orchestration
│   │   ├── adr_service.py      # ADR Prediction
│   │   ├── ddi_service.py      # Interaction detection
│   │   └── recommendation_service.py # Smart alternatives
│   ├── models/                 # Pydantic data models
│   └── data/                   # Sample datasets
├── frontend/                   # Frontend (React + Vite)
│   ├── src/                    # UI Components and Logic
│   ├── public/                 # Static assets
│   └── package.json            # Frontend dependencies
├── venv/                       # Python virtual environment
├── requirements.txt            # Backend dependencies
├── test_chatbot_integration.py # Integration tests for Chatbot
└── README.md                   # Project documentation
```

---

## 🛠️ Setup and Installation

### 1. Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher

### 2. Backend Setup
From the project root:
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
From the project root:
```powershell
cd frontend
npm install
```

---

## 🏃 Running the Application

To run the full application, you need to start both the backend and the frontend servers.

### 🚀 Start Backend (FastAPI)
Open a terminal in the root directory and run:
```powershell
# Ensure venv is activated
.\venv\Scripts\activate

# Start the server
uvicorn app.main:app --reload
```
- **API URL**: `http://127.0.0.1:8000`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`

### 💻 Start Frontend (React)
Open a **new** terminal in the `frontend` directory and run:
```powershell
cd frontend
npm install @vitejs/plugin-react --save-dev

npm run dev
```
- **App URL**: `http://localhost:5173` (or the port shown in your terminal)

---

## 🧪 Testing and Verification

### Automated Backend Tests
We provide several scripts to verify the core logic:
```powershell
# Test NER & Recommendation Pipeline
python test_recommendation_integration.py

# Test Chatbot NLP Logic
python test_chatbot_integration.py
```

### Manual API Test (Powershell)
```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/chat" `
  -ContentType "application/json" `
  -Body '{"message": "Patient taking Dolo 650 with Aspirin"}'
```

---

## 🧬 Roadmap
- [ ] Integration of BioBERT for deep-learning-based NER.
- [ ] Support for multi-lingual clinical notes (Hindi/English).
- [ ] Database integration for persistent patient history.
- [ ] Advanced visualization for drug interaction networks.
=======
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
>>>>>>> 330e061 (Done with updation of frontend and backend)
