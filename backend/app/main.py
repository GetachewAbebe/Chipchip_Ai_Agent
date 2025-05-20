from fastapi import FastAPI
from app.db import models, database
from app.db.database import SessionLocal

app = FastAPI()

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)

    db = SessionLocal()

    # Check if data already exists
    if db.query(models.Customer).first():
        db.close()
        return  # Prevent duplicate insert

    # Insert Customers
    c1 = models.Customer(name="Alice", email="alice@example.com")
    c2 = models.Customer(name="Bob", email="bob@example.com")
    db.add_all([c1, c2])
    db.commit()

    # Insert Products
    p1 = models.Product(name="Notebook", category="Stationery", price=10)
    p2 = models.Product(name="Pen", category="Stationery", price=2)
    db.add_all([p1, p2])
    db.commit()

    # Insert Orders
    o1 = models.Order(customer_id=c1.id, total_amount=12.0)
    o2 = models.Order(customer_id=c2.id, total_amount=2.0)
    db.add_all([o1, o2])
    db.commit()

    # Insert Order Items
    oi1 = models.OrderItem(order_id=o1.id, product_id=p1.id, quantity=1)
    oi2 = models.OrderItem(order_id=o1.id, product_id=p2.id, quantity=1)
    oi3 = models.OrderItem(order_id=o2.id, product_id=p2.id, quantity=1)
    db.add_all([oi1, oi2, oi3])
    db.commit()

    db.close()
