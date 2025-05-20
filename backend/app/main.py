from fastapi import FastAPI
from sqlalchemy import text
from app.db import models, database
from app.db.database import SessionLocal
from app.db.seed_data import seed_if_needed

app = FastAPI()


def try_alter_tables(engine):
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE customers ADD COLUMN signup_date TIMESTAMP"))
        except Exception:
            pass
        try:
            conn.execute(text("ALTER TABLE customers ADD COLUMN segment VARCHAR"))
        except Exception:
            pass
        try:
            conn.execute(text("ALTER TABLE customers ADD COLUMN registration_channel VARCHAR"))
        except Exception:
            pass


@app.on_event("startup")
def startup_event():
    # Create all missing tables
    models.Base.metadata.create_all(bind=database.engine)

    # Try adding missing columns (Render-safe)
    try_alter_tables(database.engine)

    # Populate data if not already seeded
    seed_if_needed()
