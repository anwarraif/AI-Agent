from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import warnings
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import router

warnings.filterwarnings("ignore")

app = FastAPI(
    title="COVID-19 Jakarta AI Assistant",
    description="AI Assistant untuk informasi COVID-19 Jakarta menggunakan RAG dan SQL Agent",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
