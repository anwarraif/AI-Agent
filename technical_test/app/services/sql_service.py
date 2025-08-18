import warnings
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from config.settings import settings

warnings.filterwarnings("ignore")

class SQLService:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )
        
        self.db = SQLDatabase.from_uri(settings.database_url)
        
        # Toolkit - hanya expose table `id_jk`
        self.toolkit = SQLDatabaseToolkit(
            db=self.db, 
            llm=self.llm, 
            include_tables=["id_jk"]
        )
        self.tools = self.toolkit.get_tools()
        
        # Ambil informasi schema table
        self.table_info = self.db.get_table_info(["id_jk"])
        
        self.sql_prefix = f"""
Kamu adalah asisten ahli SQL untuk data Covid-19 Jakarta.
Berikut adalah schema tabel `id_jk`:
{self.table_info}

Instruksi Keras:
1. Jawablah hanya dengan query SQL **lengkap dan valid** untuk PostgreSQL.
2. Gunakan tabel `id_jk` saja, jangan gunakan tabel lain.
3. Semua literal tanggal harus ditulis dengan fungsi TO_DATE, contoh:
   `WHERE TO_DATE(date, 'MM/DD/YYYY') BETWEEN TO_DATE('07/01/2021','MM/DD/YYYY') AND TO_DATE('07/31/2021','MM/DD/YYYY')`
4. Jika user bertanya kasus baru → pakai kolom new_confirmed.
5. Jika user bertanya kematian baru → pakai kolom new_deceased.
6. Jika user bertanya total kumulatif → pakai kolom cumulative_confirmed atau cumulative_deceased.
7. Jika user bertanya populasi → pakai kolom population (atau sub kolom gender/usia).
8. Jika user bertanya tentang iklim → pakai kolom average_temperature_celsius, rainfall_mm, relative_humidity, dll.
9. Selalu tutup query dengan benar (tidak boleh terpotong).
10. Jangan gunakan DML (INSERT, UPDATE, DELETE, DROP).
11. Hasilkan jawaban dalam 2 bagian:
    - **SQL Query:** tampilkan query
    - **Penjelasan:** ringkas hasil query dalam bahasa natural

Definisi kolom penting:
- date: string format 'MM/DD/YYYY', harus dikonversi dengan TO_DATE(date, 'MM/DD/YYYY').
- new_confirmed: jumlah kasus baru Covid pada hari tersebut.
- new_deceased: jumlah kematian baru pada hari tersebut.
- cumulative_confirmed: total kumulatif kasus positif sampai hari tersebut.
- cumulative_deceased: total kumulatif kematian sampai hari tersebut.
- population: jumlah total populasi di area terkait.
- population_male / population_female: distribusi populasi berdasarkan gender.
- population_age_xx_yy: distribusi populasi berdasarkan rentang usia.
- latitude, longitude: koordinat lokasi.
- average_temperature_celsius, rainfall_mm, relative_humidity: data iklim/hariannya.

"""
        
        self.system_message = SystemMessage(content=self.sql_prefix)
        
        # Agent Executor
        self.agent_executor = create_react_agent(
            self.llm,
            self.tools,
            state_modifier=self.system_message,
            debug=False
        )
    
    def query(self, question: str) -> str:
        """Execute SQL Agent query and return response"""
        try:
            final_answer = ""
            for s in self.agent_executor.stream({"messages": [HumanMessage(content=question)]}):
                if "agent" in s:
                    final_answer += str(s["agent"]["messages"][0].content) + "\n"
                elif "tools" in s:
                    final_answer += str(s["tools"]) + "\n"
            
            return final_answer.strip() if final_answer else "Tidak dapat memproses query SQL."
            
        except Exception as e:
            return f"Error dalam SQL query: {str(e)}"
