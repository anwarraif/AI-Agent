from langchain_community.utilities import SQLDatabase
from app_v2.core.config import DATABASE_URL

def get_db():
    return SQLDatabase.from_uri(DATABASE_URL)
