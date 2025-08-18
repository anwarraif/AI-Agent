import os
import sys
import psycopg2
from dotenv import load_dotenv
import pandas as pd

# Load environment variables dari file .env
load_dotenv()

def connect():
    """Connect to database"""
    conn = None
    try:
        print("Connecting...")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD")
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print("Connection failed:", error)
        sys.exit(1)

    print("All good, Connection successful!")
    return conn

def sql_to_dataframe(conn, query):
    """
    Import data from a PostgreSQL database using a SELECT query.
    Column names are automatically taken from the query result.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        tuples_list = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]  # ambil nama kolom otomatis
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return None
    finally:
        cursor.close()

    # Transform the list into a pandas DataFrame
    df = pd.DataFrame(tuples_list, columns=colnames)
    return df

# Get table ETL

conn = connect()
query = "SELECT * FROM id_jk"
df_covid = sql_to_dataframe(conn, query)
print(df_covid.tail())