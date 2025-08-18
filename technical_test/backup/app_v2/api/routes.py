from fastapi import APIRouter
from app_v2.api.schemas import QueryRequest, QueryResponse
from app_v2.core.supervisor import run_supervised_query
import time

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    start = time.time()
    result = run_supervised_query(req.query, req.session_id)
    end = time.time()
    result["latency_ms"] = round((end - start) * 1000, 2)
    return result

@router.get("/healthz")
def health_check():
    return {"status": "ok"}
