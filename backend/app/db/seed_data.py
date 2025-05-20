from app.db.models import Customer, Product, Order, OrderItem
from app.db.database import SessionLocal
from datetime import datetime, timedelta
import random

def seed_if_needed():
    db = SessionLocal()

    if db.query(Customer).first():
        db.close()
        return

    segments = ["Working Professionals", "Parents", "Students"]
    channels = ["organic", "referral", "paid ad", "influencer"]
    product_names = ["Apple", "Banana", "Tomato", "Carrot", "Milk", "Cheese", "Eggs"]

    # Seed Customers
    customers = []
    for i in range(200):
        customers.append(Customer(
            name=f"Customer {i}",
            email=f"user{i}@chipchip.com",
            signup_date=datetime(2023, 6, 1) + timedelta(days=random.randint(0, 90)),
            segment=random.choice(segments),
            registration_channel=random.choice(channels),
        ))
    db.add_all(customers)
    db.commit()

    # Seed Products
    products = []
    for name in product_names:
        products.append(Product(
            name=name,
            category="Fresh Produce",
            price=random.randint(2, 10)
        ))
    db.add_all(products)
    db.commit()

    # Seed Orders and OrderItems
    all_customers = db.query(Customer).all()
    all_products = db.query(Product).all()

    for _ in range(500):
        cust = random.choice(all_customers)
        order_date = cust.signup_date + timedelta(days=random.randint(1, 60))
        order = Order(customer_id=cust.id, order_date=order_date, total_amount=0.0)
        db.add(order)
        db.commit()

        selected_products = random.sample(all_products, k=random.randint(1, 3))
        total = 0
        for prod in selected_products:
            qty = random.randint(1, 4)
            db.add(OrderItem(order_id=order.id, product_id=prod.id, quantity=qty))
            total += qty * prod.price
        order.total_amount = total
        db.commit()

    db.close()
