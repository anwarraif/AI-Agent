from app_v2.rag.chain import run_rag

class RAGAgentWrapper:
    def __init__(self):
        pass
    
    def invoke(self, query: str):
        try:
            result = run_rag(query)
            # run_rag already returns the correct format
            return result
        except Exception as e:
            return {
                "answer": f"Error in RAG processing: {str(e)}",
                "sources": [],
                "sql_preview": "",
                "sql_result": ""
            }

rag_tool = RAGAgentWrapper()
