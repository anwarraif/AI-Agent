import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# 1. Load embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

# 2. Load FAISS index dari disk
db_name = r"C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\docs_kebijakan_covid_jkt"
vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)

# 3. Uji retrieval
query = "nomor telepon dinas kesehatan"
docs = vector_store.similarity_search(query, k=3)

print("Query:", query)
print("="*10)
for i, d in enumerate(docs, 1):
    print(f"Hasil {i}:")
    print(d.page_content[:500])  # tampilkan max 500 char
    print("-"*10)
