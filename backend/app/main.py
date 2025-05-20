from fastapi import FastAPI
from app.db import models, database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.post("/seed")
def seed_all():
    from app.db.database import SessionLocal
    from app.db.models import Product, Customer, Order

    db = SessionLocal()

    # Insert sample customers
    c1 = Customer(name="Alice", email="alice@example.com")
    c2 = Customer(name="Bob", email="bob@example.com")
    db.add_all([c1, c2])
    db.commit()

    # Insert sample products
    p1 = Product(name="Notebook", category="Stationery", price=10)
    p2 = Product(name="Pen", category="Stationery", price=2)
    db.add_all([p1, p2])
    db.commit()

    # Insert sample orders
    o1 = Order(customer_id=c1.id, total_amount=12.0)
    o2 = Order(customer_id=c2.id, total_amount=2.0)
    db.add_all([o1, o2])
    db.commit()

    db.close()
    return {"message": "All data seeded successfully"}
