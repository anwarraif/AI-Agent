from typing import Union, Literal, TypedDict, Annotated, List, Any
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
import operator, functools
from app_v2.agents.rag_agent import rag_tool
from app_v2.agents.sql_agent import sql_agent

# --- State Schema
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    reason: str
    answer: str
    sources: List[dict]
    sql_preview: str
    sql_result: Any

# --- Supervisor Schema
RouteResponseNextType = Union[Literal["FINISH"], Literal["RAG"], Literal["SQL"]]

class RouteResponse(BaseModel):
    next: RouteResponseNextType
    reason: str

prompt_message = """
Anda adalah supervisor AI yang menentukan agen mana yang harus menangani pertanyaan pengguna.

PILIHAN AGEN:
- RAG: untuk pertanyaan tentang kebijakan, aturan, dokumen, informasi umum Covid-19 Jakarta, nomor telepon, alamat, layanan kesehatan, protokol kesehatan
- SQL: untuk pertanyaan tentang data statistik, angka, grafik, analisis numerik, jumlah kasus, data temporal dari database
- FINISH: jika sudah mendapat jawaban yang memadai dari agen sebelumnya

INSTRUKSI:
1. Analisis pertanyaan pengguna dengan cermat
2. Tentukan agen yang paling tepat berdasarkan jenis informasi yang diminta
3. Berikan respons dalam format JSON yang VALID dengan kunci 'next' dan 'reason'
4. Nilai 'next' harus PERSIS salah satu dari: "RAG", "SQL", atau "FINISH"

CONTOH RESPONS:
{{"next": "RAG", "reason": "Pertanyaan tentang kebijakan atau informasi umum"}}
{{"next": "SQL", "reason": "Pertanyaan tentang data statistik atau numerik"}}

CONTOH KASUS:
- "Apa aturan PSBB di Jakarta?" → RAG (kebijakan/dokumen)
- "Nomor dinas kesehatan berapa?" → RAG (informasi kontak)
- "Berapa total kasus Covid hari ini?" → SQL (data statistik)
- "Protokol kesehatan apa saja?" → RAG (panduan/dokumen)
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_message),
    ("human", "Pertanyaan pengguna: {question}"),
    ("system", "Analisis pertanyaan dan berikan respons JSON dengan format: {{\"next\": \"RAG/SQL/FINISH\", \"reason\": \"alasan pilihan\"}}")
])

from langchain_ollama import ChatOllama
from app_v2.core.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL_SQL

llm = ChatOllama(model=OLLAMA_CHAT_MODEL_SQL, base_url=OLLAMA_BASE_URL)

def supervisor_agent(state: AgentState) -> dict:
    # Check if we already have an answer from an agent (not initial empty state)
    if (state.get("answer") and 
        state.get("answer") != "" and 
        len(state.get("messages", [])) > 1):  # More than just the initial human message
        return {
            "next": "FINISH",
            "reason": "Already have answer from previous agent"
        }
    
    # Get the user question
    question = state["messages"][-1].content
    
    try:
        # Use LLM with structured output to determine routing
        chain = (prompt | llm.with_structured_output(RouteResponse))
        response: RouteResponse = chain.invoke({"question": question})
        
        return {
            "next": response.next,
            "reason": response.reason
        }
    except Exception as e:
        # Fallback if structured output fails
        print(f"Structured output failed: {e}")
        
        # Try with regular LLM call and parse manually
        try:
            formatted_prompt = prompt.format_messages(question=question)
            raw_response = llm.invoke(formatted_prompt)
            content = raw_response.content.strip()
            
            print(f"Raw LLM response: {content}")
            
            # Simple parsing for JSON-like response
            if "RAG" in content.upper():
                return {
                    "next": "RAG",
                    "reason": "LLM determined RAG is appropriate"
                }
            elif "SQL" in content.upper():
                return {
                    "next": "SQL", 
                    "reason": "LLM determined SQL is appropriate"
                }
            else:
                # Default fallback
                return {
                    "next": "RAG",
                    "reason": "Fallback to RAG due to parsing issues"
                }
        except Exception as e2:
            print(f"LLM call failed: {e2}")
            # Final fallback
            return {
                "next": "RAG",
                "reason": "Emergency fallback to RAG"
            }

# --- Agent Nodes
def rag_node(state: AgentState) -> dict:
    query_text = state["messages"][-1].content
    result = rag_tool.invoke(query_text)
    
    # Create AI message for conversation history
    ai_msg = AIMessage(content=result.get("answer", ""), name="RAG")
    
    return {
        "messages": [ai_msg],
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "sql_preview": "",
        "sql_result": ""
    }

def sql_node(state: AgentState) -> dict:
    query_text = state["messages"][-1].content
    result = sql_agent.invoke(query_text)
    
    # Create AI message for conversation history
    ai_msg = AIMessage(content=result.get("answer", ""), name="SQL")
    
    return {
        "messages": [ai_msg],
        "answer": result.get("answer", ""),
        "sources": [],
        "sql_preview": result.get("sql_preview", ""),
        "sql_result": result.get("sql_result", "")
    }

# --- Workflow
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("RAG", rag_node)
    workflow.add_node("SQL", sql_node)

    # Add edges
    workflow.add_edge(START, "supervisor")
    workflow.add_edge("RAG", "supervisor")
    workflow.add_edge("SQL", "supervisor")

    # Conditional routing from supervisor
    def route_supervisor(state):
        return state["next"]
    
    conditional_map = {
        "RAG": "RAG", 
        "SQL": "SQL", 
        "FINISH": END
    }
    workflow.add_conditional_edges("supervisor", route_supervisor, conditional_map)

    return workflow.compile()

graph = build_graph()

def run_supervised_query(query: str, session_id: str = None):
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "next": "",
        "reason": "",
        "answer": "",  # Make sure this is empty string, not None
        "sources": [],
        "sql_preview": "",
        "sql_result": ""
    }
    
    try:
        # Stream the graph execution
        final_state = None
        rag_result = None
        sql_result = None
        supervisor_reason = ""
        
        for state in graph.stream(initial_state):
            final_state = state
            
            # Capture results from different nodes
            if "RAG" in state:
                rag_result = state["RAG"]
            elif "SQL" in state:
                sql_result = state["SQL"]
            elif "supervisor" in state:
                supervisor_reason = state["supervisor"].get("reason", "")
        
        # Determine which result to use
        if rag_result:
            return {
                "answer": rag_result.get("answer", "No answer from RAG"),
                "route_taken": "RAG",
                "sources": rag_result.get("sources", []),
                "sql_preview": "",
                "sql_result": "",
                "supervisor_reason": supervisor_reason
            }
        elif sql_result:
            return {
                "answer": sql_result.get("answer", "No answer from SQL"),
                "route_taken": "SQL",
                "sources": [],
                "sql_preview": sql_result.get("sql_preview", ""),
                "sql_result": sql_result.get("sql_result", ""),
                "supervisor_reason": supervisor_reason
            }
        else:
            return {
                "answer": "Error: No agent was executed",
                "route_taken": "Error",
                "sources": [],
                "sql_preview": "",
                "sql_result": "",
                "supervisor_reason": supervisor_reason
            }
            
    except Exception as e:
        return {
            "answer": f"Error processing query: {str(e)}",
            "route_taken": "Error",
            "sources": [],
            "sql_preview": "",
            "sql_result": "",
            "supervisor_reason": f"Exception: {str(e)}"
        }
