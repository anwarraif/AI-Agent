from pydantic import BaseModel
from typing import Optional, Literal

class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    source: Literal["rag", "sql"]
    reasoning: Optional[str] = None
    
class HealthResponse(BaseModel):
    status: str
    message: str
