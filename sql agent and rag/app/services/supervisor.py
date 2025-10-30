import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings
from services.rag_service import RAGService
from services.sql_service import SQLService

class SupervisorService:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        
        self.rag_service = RAGService()
        self.sql_service = SQLService()
        
        self.decision_prompt = ChatPromptTemplate.from_template("""
Anda adalah supervisor yang menentukan apakah pertanyaan pengguna harus dijawab menggunakan RAG (pencarian dokumen) atau SQL Agent (query database).

Kriteria untuk memilih:

**RAG (pencarian dokumen)** - pilih jika pertanyaan tentang:
- Informasi kebijakan, peraturan, atau prosedur Covid-19
- Nomor telepon, alamat, kontak instansi
- Panduan, protokol kesehatan
- Informasi umum tentang Covid-19
- Layanan kesehatan atau fasilitas medis

**SQL (query database)** - pilih jika pertanyaan tentang:
- Data numerik atau statistik Covid-19 (jumlah kasus, kematian)
- Tren data berdasarkan waktu (harian, bulanan, tahunan)
- Perbandingan angka pada periode tertentu
- Analisis data kuantitatif
- Pertanyaan yang memerlukan perhitungan atau agregasi data

Pertanyaan: {question}

Jawab hanya dengan "RAG" atau "SQL" tanpa penjelasan tambahan.
""")
        
        self.decision_chain = (
            self.decision_prompt
            | self.llm
            | StrOutputParser()
        )
    
    def decide_agent(self, question: str) -> str:
        """Decide which agent to use based on the question"""
        try:
            decision = self.decision_chain.invoke({"question": question}).strip().upper()
            # Ensure we only get RAG or SQL
            if "RAG" in decision:
                return "RAG"
            elif "SQL" in decision:
                return "SQL"
            else:
                # Default fallback to RAG if unclear
                return "RAG"
        except Exception as e:
            print(f"Error in decision making: {e}")
            return "RAG"  # Default fallback
    
    def process_query(self, question: str) -> dict:
        """Process query using appropriate agent"""
        # Decide which agent to use
        agent_choice = self.decide_agent(question)
        
        # Execute query with chosen agent
        if agent_choice == "SQL":
            answer = self.sql_service.query(question)
            source = "sql"
        else:
            answer = self.rag_service.query(question)
            source = "rag"
        
        return {
            "answer": answer,
            "source": source,
            "reasoning": f"Supervisor memilih {agent_choice} agent berdasarkan analisis konteks pertanyaan."
        }
