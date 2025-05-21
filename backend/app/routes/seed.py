from fastapi import APIRouter
from app.utils.setup_and_seed_db import seed_database

router = APIRouter()

@router.post("/seed-data")
def seed_data():
    seed_database()
    return {"status": "✅ Database seeded successfully"}