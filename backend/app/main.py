import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import init_db_engine, Base, engine
from app.api.voice import router as voice_router
from app.api.nlp import router as nlp_router
from app.api.forms import router as forms_router
from app.api.schemes import router as schemes_router
from app.api.assistant import router as assistant_router
from app.api.dataset import router as dataset_router

from fastapi import Request
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI App
app = FastAPI(
    title="VoiceForm AI API",
    description="Intelligent Voice-Based Government Form Filling & Scheme Eligibility Engine",
    version="1.0.0"
)

# Configure CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("[VoiceForm AI] Starting backend server...")
    eng = init_db_engine()
    # Create tables if not already created
    Base.metadata.create_all(bind=eng)
    print("[VoiceForm AI] Database schema initialized successfully.")

# Path to built React frontend
DIST_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
ASSETS_DIR = os.path.join(DIST_DIR, "assets")

if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/")
def home(request: Request):
    # When visited from a web browser, serve the production React frontend if available
    accept = request.headers.get("accept", "")
    index_file = os.path.join(DIST_DIR, "index.html")
    if "text/html" in accept and os.path.exists(index_file):
        return FileResponse(index_file)

    # API / Automated test health status response
    return {
        "app": "VoiceForm AI",
        "tagline": "AI-Powered Voice-Based Government Form Filling & Scheme Eligibility",
        "status": "online",
        "features": [
            "OpenAI Whisper Speech-to-Text",
            "Indian Government NER / NLP Entity Extraction",
            "Auto-Fill Form Mapping",
            "Government Scheme Eligibility Engine",
            "Multilingual Smart Form Assistant (English, Hindi, Marathi)",
            "Official Application PDF Receipt Generator"
        ]
    }

# Endpoint to serve sample audio for testing without microphone
@app.get("/sample-audio")
def get_sample_audio():
    sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "voiceform_test.wav")
    if os.path.exists(sample_path):
        return FileResponse(sample_path, media_type="audio/wav", filename="voiceform_test.wav")
    return {"error": "Sample file not found"}

# Register All API Routers
app.include_router(voice_router, prefix="/api/voice", tags=["Voice Transcription & Whisper"])
app.include_router(nlp_router, prefix="/api/nlp", tags=["NLP & NER Extraction"])
app.include_router(forms_router, prefix="/api/forms", tags=["Government Forms & Submissions"])
app.include_router(schemes_router, prefix="/api/schemes", tags=["Scheme Eligibility Engine"])
app.include_router(assistant_router, prefix="/api/assistant", tags=["Smart Form Assistant"])
app.include_router(dataset_router, prefix="/api/dataset", tags=["Dataset Management & Evaluation"])

# SPA Fallback for client-side routing in production (e.g. /forms, /dataset, /schemes)
@app.get("/{full_path:path}")
def serve_spa_routes(full_path: str, request: Request):
    if full_path.startswith("api/") or full_path in ["docs", "openapi.json", "redoc", "sample-audio"]:
        return {"error": "Not Found"}

    file_path = os.path.join(DIST_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    index_file = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)

    return {"message": "VoiceForm AI Backend Running"}