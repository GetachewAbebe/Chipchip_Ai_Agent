# backend/wait_for_postgres.py
import time
import psycopg2
import os

host = os.getenv("PGHOST", "db")
port = os.getenv("PGPORT", 5432)
user = os.getenv("PGUSER", "postgres")
password = os.getenv("PGPASSWORD", "Admin")
database = os.getenv("PGDATABASE", "chipchip")

print(f"⏳ Waiting for PostgreSQL at {host}:{port}...")

while True:
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=database
        )
        conn.close()
        print("✅ PostgreSQL is ready!")
        break
    except Exception as e:
        print(".", end="", flush=True)
        time.sleep(1)
