import psycopg2 # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

def getConnection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
