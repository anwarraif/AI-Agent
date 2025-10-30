import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest, QueryResponse, HealthResponse
from services.supervisor import SupervisorService

router = APIRouter()

# Initialize supervisor service
supervisor = SupervisorService()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="COVID-19 Jakarta AI Assistant is running"
    )

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process user query using RAG or SQL Agent based on context"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        result = supervisor.process_query(request.question)
        
        return QueryResponse(
            answer=result["answer"],
            source=result["source"],
            reasoning=result["reasoning"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "COVID-19 Jakarta AI Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query"
        }
    }
