from app.rag.chain import run_rag
from langchain.agents import Tool

rag_tool = Tool(
    name="RAG_Agent",
    func=lambda q: run_rag(q),  # langsung string, bukan dict
    description="Gunakan untuk pertanyaan kebijakan/aturan Covid-19 Jakarta."
)
