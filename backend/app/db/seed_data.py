# Script to load sample data
import random
from datetime import timedelta, date
from sqlalchemy.orm import Session
from app.db.models import Base, User, GroupLeader, Order, Product, OrderItem
from app.db.session import engine, SessionLocal

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

channels = ["organic", "referral", "paid ad"]
products = [
    ("Tomato", "vegetable"),
    ("Banana", "fruit"),
    ("Carrot", "vegetable"),
    ("Apple", "fruit"),
    ("Onion", "vegetable"),
    ("Lettuce", "vegetable"),
    ("Mango", "fruit"),
]

# Add products
product_objs = []
for name, cat in products:
    p = Product(name=name, category=cat)
    db.add(p)
    product_objs.append(p)

# Add group leaders
group_leaders = []
for i in range(10):
    gl = GroupLeader(name=f"Leader {i+1}")
    db.add(gl)
    group_leaders.append(gl)

# Add users
users = []
start_date = date.today() - timedelta(days=365)
for i in range(200):
    u = User(
        name=f"User {i+1}",
        signup_channel=random.choice(channels),
        signup_date=start_date + timedelta(days=random.randint(0, 364))
    )
    db.add(u)
    users.append(u)

db.commit()

# Add orders
for user in users:
    for _ in range(random.randint(1, 10)):
        order_date = user.signup_date + timedelta(days=random.randint(0, 90))
        order = Order(
            user_id=user.id,
            group_leader_id=random.choice(group_leaders).id,
            order_date=order_date
        )
        db.add(order)
        db.flush()  # to get order.id

        # Add order items
        for _ in range(random.randint(1, 3)):
            item = OrderItem(
                order_id=order.id,
                product_id=random.choice(product_objs).id,
                quantity=random.randint(1, 5),
                price=round(random.uniform(1.5, 10.0), 2)
            )
            db.add(item)

db.commit()
print("✅ Sample data inserted.")
