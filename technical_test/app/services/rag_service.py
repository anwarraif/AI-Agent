import warnings
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.prompts import ChatPromptTemplate
from config.settings import settings

warnings.filterwarnings("ignore")

class RAGService:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.EMBEDDING_MODEL, 
            base_url=settings.OLLAMA_BASE_URL
        )
        
        self.vector_store = FAISS.load_local(
            settings.VECTOR_DB_PATH, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )
        
        self.retriever = self.vector_store.as_retriever(
            search_type='similarity', 
            search_kwargs={'k': 5}
        )
        
        self.llm = ChatOllama(
            model=settings.LLM_MODEL, 
            base_url=settings.OLLAMA_BASE_URL
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
Anda adalah seorang asisten yang ahli dalam memberikan informasi seputar Covid-19 di wilayah Jakarta. 
Jawablah pertanyaan pengguna hanya berdasarkan *knowledge base* (dokumen hasil pencarian vektor) yang telah disediakan. 

Aturan:
1. Gunakan bahasa Indonesia yang jelas, singkat, dan mudah dipahami.
2. Jika informasi ada dalam konteks, rangkum secara akurat tanpa menambahkan opini atau asumsi.
3. Jika informasi tidak ada dalam konteks atau konteks tidak relevan, jawab: 
   "Maaf, saya tidak menemukan informasi yang ditanyakan."
4. Jika terdapat data penting (misalnya nomor telepon, alamat instansi, kebijakan resmi), sampaikan apa adanya sesuai konteks.
5. Jangan mengarang jawaban di luar knowledge base.
informasi umum :
Hubungi Dinas Kesehatan melalui no. telp : 0813-8837-6955 
Kementerian Kesehatan melalui no. telp : 021-5210411 / 0812-1212-3119

---
Pertanyaan Pengguna:
{question}

Konteks (hasil pencarian dokumen):
{context}

Jawaban:
""")
        
        self.rag_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _format_docs(self, docs):
        return '\n\n'.join([doc.page_content for doc in docs])
    
    def query(self, question: str) -> str:
        """Execute RAG query and return response"""
        try:
            response = self.rag_chain.invoke(question)
            return response
        except Exception as e:
            return f"Error dalam RAG query: {str(e)}"
