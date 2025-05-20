from fastapi import FastAPI
from app.db import models, database

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

# (Optional) Endpoint to seed sample data
@app.post("/seed")
def seed_data():
    from app.db.database import SessionLocal
    from app.db.models import Product

    db = SessionLocal()
    db.add_all([
        Product(name="Toothpaste", category="Health", price=3),
        Product(name="Notebook", category="Stationery", price=5),
        Product(name="Water Bottle", category="Utility", price=10),
    ])
    db.commit()
    db.close()
    return {"message": "Sample data inserted"}
