from app.db.models import (
    Customer, GroupLeader, CustomerGroupLeaderMap,
    Product, Order, OrderItem, SegmentEnum, ChannelEnum
)
from app.db.database import SessionLocal
import random
import datetime
from faker import Faker

fake = Faker()

def seed_if_needed():
    db = SessionLocal()

    # if db.query(Customer).first():
    #     db.close()
    #     print("Data already seeded.")
    #     return

    # -------------------- Seed Group Leaders --------------------
    group_leaders = []
    for _ in range(20):
        gl = GroupLeader(name=fake.name(), joined_date=fake.date_time_between(start_date='-6M'))
        group_leaders.append(gl)
    db.add_all(group_leaders)
    db.commit()

    # -------------------- Seed Customers --------------------
    segments = list(SegmentEnum)
    channels = list(ChannelEnum)
    customers = []
    group_map = []

    for i in range(200):
        c = Customer(
            name=fake.name(),
            email=fake.unique.email(),
            signup_date=fake.date_time_between(start_date='-3M'),
            segment=random.choice(segments),
            registration_channel=random.choice(channels),
        )
        customers.append(c)

    db.add_all(customers)
    db.commit()

    # -------------------- Map Customers to Group Leaders --------------------
    for c in customers:
        gl = random.choice(group_leaders)
        group_map.append(CustomerGroupLeaderMap(customer_id=c.id, group_leader_id=gl.id))
    db.add_all(group_map)
    db.commit()

    # -------------------- Seed Products --------------------
    categories = ['Vegetables', 'Fruits', 'Stationery']
    types = ['fresh produce', 'stationery']
    products = []

    for i in range(50):
        p = Product(
            name=fake.word().capitalize(),
            category=random.choice(categories),
            type=random.choice(types),
            price=round(random.uniform(1, 50), 2)
        )
        products.append(p)

    db.add_all(products)
    db.commit()

    # -------------------- Seed Orders and OrderItems --------------------
    orders = []
    items = []

    for _ in range(2000):
        cust = random.choice(customers)
        order = Order(
            customer_id=cust.id,
            order_datetime=fake.date_time_between(start_date='-2M'),
            total_amount=0  # placeholder for total
        )
        db.add(order)
        db.flush()  # get order.id

        total = 0
        for _ in range(random.randint(1, 4)):
            prod = random.choice(products)
            qty = random.randint(1, 5)
            items.append(OrderItem(order_id=order.id, product_id=prod.id, quantity=qty))
            total += prod.price * qty

        order.total_amount = round(total, 2)

    db.add_all(items)
    db.commit()
    db.close()

    print("✅ Sample data seeded successfully.")
