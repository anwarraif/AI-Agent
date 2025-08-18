from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class Source(BaseModel):
    doc_id: str
    snippet: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    route_taken: str
    sources: Optional[List[Source]] = None
    sql_preview: Optional[str] = None
    sql_result: Optional[List[Dict]] = None
    supervisor_reason: Optional[str] = None
    latency_ms: float
