import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_API_BASE = os.getenv('OLLAMA_API_BASE', 'http://localhost:11434')
    LLM_MODEL = 'llama3.1:8b'
    EMBEDDING_MODEL = 'nomic-embed-text'
    
    # Vector Database Configuration
    VECTOR_DB_PATH = r"C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\docs_kebijakan_covid_jkt"
    
    # PostgreSQL Configuration
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    
    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
