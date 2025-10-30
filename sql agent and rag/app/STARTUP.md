# 🚀 Cara Menjalankan FastAPI

## Langkah-langkah:

### 1. Masuk ke folder app
```bash
cd C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\app
```

### 2. Aktivasi virtual environment (jika ada)
```bash
# Jika menggunakan conda
conda activate test_env

# Atau jika menggunakan venv
# ..\test_env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Test komponen (opsional)
```bash
python test_simple.py
```

### 5. Jalankan FastAPI
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Akses aplikasi
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health
- **Root**: http://localhost:8000/api/v1/

## Test dengan curl:

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Query RAG
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d "{\"question\": \"infoin dong nomor telpon dinas kesehatan jkt\"}"
```

### Query SQL
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d "{\"question\": \"berapa kasus covid baru bulan maret 2020?\"}"
```

## Troubleshooting:

1. **Error "Could not import module main"**
   - Pastikan Anda di folder `app/`
   - Jalankan: `cd C:\Users\acer\Documents\Rubythalib\rubythalib\technical_test\app`

2. **Import errors**
   - Jalankan `python test_simple.py` untuk debug
   - Pastikan semua dependencies terinstall

3. **Ollama connection error**
   - Pastikan Ollama running: `ollama serve`
   - Check model tersedia: `ollama list`

4. **Database connection error**
   - Pastikan PostgreSQL running
   - Check kredensial di file `.env`
