from typing import Union, Literal
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, BaseMessage
import operator, functools
from app.agents.rag_agent import rag_tool
from app.agents.sql_agent import sql_agent
from langchain_core.runnables import Runnable

# --- Supervisor Schema
RouteResponseNextType = Union[Literal["FINISH"], Literal["RAG"], Literal["SQL"]]

class RouteResponse(BaseModel):
    next: RouteResponseNextType
    reason: str

prompt_message = """
Anda adalah supervisor. Pilih agen:
- RAG: untuk pertanyaan kebijakan/dokumen Covid-19 Jakarta.
- SQL: untuk pertanyaan angka/statistik dari database Postgres (tabel id_jk).
Jawablah dalam format JSON dengan kunci 'next' dan 'reason'.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_message),
    MessagesPlaceholder(variable_name="messages"),
    ("system", "Siapa yang harus bertindak selanjutnya?")
])

from langchain_ollama import ChatOllama
from app.core.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL_SQL

llm = ChatOllama(model=OLLAMA_CHAT_MODEL_SQL, base_url=OLLAMA_BASE_URL)

def supervisor_agent(state):
    chain = (prompt | llm.with_structured_output(RouteResponse))
    response: RouteResponse = chain.invoke(state)

    return {
        "next": response.next,
        "reason": response.reason,
        "messages": state["messages"],  # teruskan messages biar agent berikutnya bisa baca query
    }

# --- Nodes
from langchain_core.messages import AIMessage

def agent_node(state: dict, agent, name: str):
    query_text = state["messages"][-1].content
    result = agent.invoke(query_text)

    # Kalau result bukan dict, bungkus dulu
    if not isinstance(result, dict):
        result = {"answer": str(result)}

    # Tambahkan ke messages biar trace lengkap
    new_msg = AIMessage(content=str(result), name=name)

    # Merge state lama dengan hasil baru
    return {
        "messages": state["messages"] + [new_msg],
        **result  # tambahkan field lain (sources/sql_result dsb)
    }



# --- Workflow
def build_graph():
    workflow = StateGraph(dict)
    workflow.add_node("RAG", functools.partial(agent_node, agent=rag_tool, name="RAG"))
    workflow.add_node("SQL", functools.partial(agent_node, agent=sql_agent, name="SQL"))
    workflow.add_node("supervisor", supervisor_agent)

    workflow.add_edge("RAG", "supervisor")
    workflow.add_edge("SQL", "supervisor")

    conditional_map = {"RAG": "RAG", "SQL": "SQL", "FINISH": END}
    workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
    workflow.add_edge(START, "supervisor")

    return workflow.compile()


graph = build_graph()

def run_supervised_query(query: str, session_id: str = None):
    events = graph.stream({"messages": [HumanMessage(content=query)]})
    final_answer = {}
    for s in events:
        final_answer = s
    return {
        "answer": str(final_answer),
        "route_taken": final_answer.get("next", "RAG"),
        "sources": final_answer.get("sources"),
        "sql_preview": final_answer.get("sql_preview"),
        "sql_result": final_answer.get("result"),
        "supervisor_reason": final_answer.get("reason")
    }
