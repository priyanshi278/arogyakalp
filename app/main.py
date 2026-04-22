from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as ner_router
from app.api.chatbot_routes import router as chatbot_router
from app.api.auth_routes import router as auth_router

app = FastAPI(title="ArogyaKalp - AI Healthcare System", description="Phase 1: Initial NER Module Implementation (Dummy Logic)")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NER, Chatbot, and Auth routes
app.include_router(ner_router)
app.include_router(chatbot_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to ArogyaKalp API Server. Use /extract_entities POST endpoint."}
