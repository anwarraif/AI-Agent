# app/core/config.py
import os
from dotenv import load_dotenv

# load .env dari root project
load_dotenv()

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_CHAT_MODEL_SQL = os.getenv("OLLAMA_CHAT_MODEL_SQL", "llama3.1:8b")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_CHAT_MODEL_RAG = os.getenv("OLLAMA_CHAT_MODEL_SQL", "llama3.1:8b")

# Database
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

FAISS_PATH = r"C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\docs_kebijakan_covid_jkt"
