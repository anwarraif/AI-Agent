# COVID-19 Jakarta AI Assistant

AI Assistant yang mengintegrasikan RAG (Retrieval-Augmented Generation) dan SQL Agent untuk memberikan informasi COVID-19 Jakarta.

## Fitur

- **LLM Supervisor**: Menentukan secara otomatis apakah menggunakan RAG atau SQL Agent berdasarkan konteks pertanyaan
- **RAG Service**: Untuk pertanyaan tentang kebijakan, prosedur, kontak, dan informasi umum COVID-19
- **SQL Agent**: Untuk pertanyaan tentang data statistik, tren, dan analisis numerik COVID-19
- **FastAPI Backend**: RESTful API yang mudah digunakan

## Struktur Project

```
app/
├── main.py              # FastAPI entry point
├── run.py               # Script untuk menjalankan server
├── config/
│   ├── __init__.py
│   └── settings.py      # Environment & database config
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic models
├── services/
│   ├── __init__.py
│   ├── rag_service.py   # RAG functionality
│   ├── sql_service.py   # SQL Agent functionality
│   └── supervisor.py    # LLM Supervisor
└── api/
    ├── __init__.py
    └── routes.py        # API endpoints
```

## Setup

1. **Masuk ke folder app:**
```bash
cd C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables (.env sudah ada):**
```
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL_SQL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
DB_USERNAME=postgres
DB_PASSWORD=admin
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

4. **Pastikan Ollama running dengan model:**
- llama3.1:8b
- nomic-embed-text

5. **Pastikan vector database tersedia di:**
`C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\docs_kebijakan_covid_jkt`

## Running

**Opsi 1: Menggunakan uvicorn langsung**
```bash
cd C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Opsi 2: Menggunakan run script**
```bash
cd C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\app
python run.py
```

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Query
```
POST /api/v1/query
Content-Type: application/json

{
    "question": "infoin dong nomor telpon dinas kesehatan jkt"
}
```

Response:
```json
{
    "answer": "...",
    "source": "rag",
    "reasoning": "Supervisor memilih RAG agent berdasarkan analisis konteks pertanyaan."
}
```

## Contoh Penggunaan

**RAG (akan dipilih untuk):**
- "infoin dong nomor telpon dinas kesehatan jkt"
- "apa protokol kesehatan untuk covid?"
- "dimana bisa tes covid di jakarta?"

**SQL Agent (akan dipilih untuk):**
- "Total kematian baru akibat Covid di Jakarta pada bulan Juli 2021"
- "berapa kasus covid baru bulan maret 2020?"
- "tren kasus covid jakarta tahun 2021"

## Testing

1. **Akses Swagger UI:** http://localhost:8000/docs
2. **Test dengan curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "infoin dong nomor telpon dinas kesehatan jkt"}'
```

## Troubleshooting

1. **Import Error**: Pastikan menjalankan dari folder `app/`
2. **Vector DB Error**: Pastikan path vector database benar
3. **Ollama Error**: Pastikan Ollama service running di localhost:11434
4. **Database Error**: Pastikan PostgreSQL running dan kredensial benar
