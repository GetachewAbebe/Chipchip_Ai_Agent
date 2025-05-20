from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import models, database
from app.routes import ask

app = FastAPI()

# CORS setup to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.post("/seed")
def seed_all():
    from app.db.database import SessionLocal
    from app.db.models import Product, Customer, Order

    db = SessionLocal()

    c1 = Customer(name="Alice", email="alice@example.com")
    c2 = Customer(name="Bob", email="bob@example.com")
    db.add_all([c1, c2])
    db.commit()

    p1 = Product(name="Notebook", category="Stationery", price=10)
    p2 = Product(name="Pen", category="Stationery", price=2)
    db.add_all([p1, p2])
    db.commit()

    o1 = Order(customer_id=c1.id, total_amount=12.0)
    o2 = Order(customer_id=c2.id, total_amount=2.0)
    db.add_all([o1, o2])
    db.commit()

    db.close()
    return {"message": "All data seeded successfully"}

# Include the router for /ask endpoint
app.include_router(ask.router)
