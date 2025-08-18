from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_ollama import ChatOllama
from app.sql.db import get_db
from app.core.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL_SQL

llm = ChatOllama(model=OLLAMA_CHAT_MODEL_SQL, base_url=OLLAMA_BASE_URL)
db = get_db()

toolkit = SQLDatabaseToolkit(db=db, llm=llm, include_tables=["id_jk"])
tools = toolkit.get_tools()
