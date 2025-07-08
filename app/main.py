from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .api.v1 import router as api_v1_router

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Legal AI API", version="1.0.0")
app.include_router(api_v1_router, prefix="/api/v1")

# Serve static files (test webpage)
import os
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Eagerly load models and embeddings at startup
from legal_ai_api.document_qa.graphRag import DocumentQARAG

@app.on_event("startup")
def load_all_models():
    # Instantiate DocumentQARAG to load all models/embeddings
    global rag_agent
    rag_agent = DocumentQARAG()
    print("API ready")

# Error handling middleware
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) or "Internal Server Error"}
    )
