import os
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

load_dotenv()

from langchain_ollama import OllamaEmbeddings

import faiss
from langchain_community.vectorstores import FAISS

embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url='http://localhost:11434')

db_name = r"C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\docs_kebijakan_covid_jkt"
vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)

retriever = vector_store.as_retriever(search_type = 'similarity', 
                                      search_kwargs = {'k': 3})

from langchain_ollama import ChatOllama 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_core.prompts import ChatPromptTemplate

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
Pertanyaan Pengguna:
{question}

Konteks (hasil pencarian dokumen):
{context}

Jawaban:
"""

prompt = ChatPromptTemplate.from_template(prompt)

llm = ChatOllama(model='llama3.1:8b', base_url=os.getenv('OLLAMA_BASE_URL'))

def format_docs(docs):
    return '\n\n'.join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever|format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question = "infoin dong nomor telpon dinas kesehatan jkt, gw kena covid"
response = rag_chain.invoke(question)

print(response)
