from langchain_ollama import OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS 
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os, re

# 1. Baca semua file PDF
pdfs = []
for root, dirs, files in os.walk("C:/Users/acer/Documents/Rubythalib/rubythalib/technical_test/data/rag"):
    for file in files:
        if file.endswith(".pdf"):
            pdfs.append(os.path.join(root, file))

# 2. Load semua dokumen PDF
docs = []
for pdf in pdfs:
    loader = PyMuPDFLoader(pdf)
    temp = loader.load()
    docs.extend(temp)

# 3. Cleaning text
def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)  # opsional, hapus non-ASCII
    text = text.strip()
    return text

for doc in docs:
    doc.page_content = clean_text(doc.page_content)

# 4. Split text jadi chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(docs)

# 5. Define embeddings Ollama
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=os.getenv("OLLAMA_API_BASE"))

# Buat FAISS langsung dari documents
vector_store = FAISS.from_documents(chunks, embeddings)

# 6. Simpan ke disk
db_name = "docs_kebijakan_covid_jkt"
vector_store.save_local(db_name)

print(f"Vector store berhasil dibuat & disimpan di: {db_name}")
