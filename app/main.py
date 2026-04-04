from fastapi import FastAPI
from app.api.routes import router as ner_router

app = FastAPI(title="ArogyaKalp - AI Healthcare System", description="Phase 1: Initial NER Module Implementation (Dummy Logic)")

# Include NER routes
app.include_router(ner_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ArogyaKalp API Server. Use /extract_entities POST endpoint."}
