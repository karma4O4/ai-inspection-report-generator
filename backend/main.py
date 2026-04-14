import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Import routers
from routers import auth, reports, images, ai, pdf

load_dotenv()

app = FastAPI(
    title="AI Inspection Report Generator API",
    description="Backend API for building inspection reports with GPT-4 Vision, OCR, and ReportLab PDF.",
    version="1.0.0"
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"  # Accept all for production-ready resilience or configure explicitly
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directories if they don't exist
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
uploads_dir = os.path.join(static_dir, "uploads")
os.makedirs(uploads_dir, exist_ok=True)

# Mount static folder for local upload retrieval
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(images.router)
app.include_router(ai.router)  # Includes /api/ai/* and /api/categories
app.include_router(pdf.router)

@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Inspection Report Generator API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main.py:app", host=host, port=port, reload=True)
