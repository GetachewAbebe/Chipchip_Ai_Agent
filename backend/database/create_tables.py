import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path

def drop_all_tables(cursor):
    print("⚠️ Dropping all tables in the database...")
    cursor.execute("""
        DO $$ DECLARE
            r RECORD;
        BEGIN
            -- Loop through all tables
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
    """)
    print("✅ All tables dropped.")

def create_tables(cursor, schema_sql):
    print("🛠️ Creating tables from schema.sql...")
    cursor.execute(schema_sql)
    print("✅ Tables created successfully.")

def main():
    # Load .env from root directory
    env_path = Path(__file__).resolve().parents[2] / '.env'
    load_dotenv(dotenv_path=env_path)

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in .env")
        return

    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://")

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        drop_all_tables(cursor)

        # Load schema.sql
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, "r") as f:
            schema_sql = f.read()

        create_tables(cursor, schema_sql)

        conn.commit()

    except Exception as e:
        print("❌ Error:", e)
        conn.rollback()

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        print("✅ Done.")

if __name__ == "__main__":
    main()
