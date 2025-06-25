# wait_for_db.py
import os
import time

import psycopg2
from psycopg2 import OperationalError

db_host = os.getenv("POSTGRES_DB_HOST")
db_port = os.getenv("POSTGRES_DB_PORT")
db_name = os.getenv("POSTGRES_DB_NAME")
db_user = os.getenv("POSTGRES_DB_USER")
db_pass = os.getenv("POSTGRES_DB_PASSWORD")

while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_pass,
        )
        conn.close()
        print("✅ Connessione al DB riuscita")
        break
    except OperationalError:
        print("⏳ DB non disponibile, ritento tra 2s...")
        time.sleep(2)
