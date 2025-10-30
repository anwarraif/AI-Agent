from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL, FAISS_PATH

embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL, base_url=OLLAMA_BASE_URL)
vector_store = FAISS.load_local(FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

def get_retriever():
    return retriever
