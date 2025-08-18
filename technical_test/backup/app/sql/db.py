from langchain_community.utilities import SQLDatabase
from app.core.config import DATABASE_URL

def get_db():
    return SQLDatabase.from_uri(DATABASE_URL)
