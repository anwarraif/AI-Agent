from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.rag.retriever import get_retriever
from app.core.config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL_RAG

prompt = """
Anda adalah seorang asisten yang ahli dalam memberikan informasi seputar Covid-19 di wilayah Jakarta. 
Jawablah pertanyaan pengguna hanya berdasarkan *knowledge base* (dokumen hasil pencarian vektor) yang telah disediakan. 

Aturan:
1. Gunakan bahasa Indonesia yang jelas, singkat, dan mudah dipahami.
2. Jika informasi ada dalam konteks, rangkum secara akurat tanpa menambahkan opini atau asumsi.
3. Jika informasi tidak ada dalam konteks atau konteks tidak relevan, jawab: 
   "Maaf, saya tidak menemukan informasi yang ditanyakan."
4. Jika terdapat data penting (misalnya nomor telepon, alamat instansi, kebijakan resmi), sampaikan apa adanya sesuai konteks.
5. Jangan mengarang jawaban di luar knowledge base.

---
Pertanyaan: {question}
Konteks: {context}
Jawaban:"""

prompt = ChatPromptTemplate.from_template(prompt)

llm = ChatOllama(model=OLLAMA_CHAT_MODEL_RAG, base_url=OLLAMA_BASE_URL)

def format_docs(docs):
    return '\n\n'.join([doc.page_content for doc in docs])

retriever = get_retriever()
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def run_rag(query: str):
    answer = rag_chain.invoke(query)
    docs = retriever.get_relevant_documents(query)
    sources = [{"doc_id": str(i), "snippet": d.page_content[:200], "score": 0.0} for i, d in enumerate(docs)]
    return {"answer": answer, "sources": sources}
