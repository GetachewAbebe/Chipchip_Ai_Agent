from faker import Faker
from random import choice, randint, sample
from datetime import datetime, timedelta
from app.db.models import (
    Base, Customer, GroupLeader, CustomerGroupLeaderMap,
    Product, Order, OrderItem, SegmentEnum, ChannelEnum
)
from app.db.database import SessionLocal, engine

fake = Faker()
db = SessionLocal()

# 1. Create tables if not exists
Base.metadata.create_all(bind=engine)

# 2. Seed group leaders
group_leaders = [
    GroupLeader(name=fake.name(), joined_date=fake.date_time_between(start_date="-1y", end_date="now"))
    for _ in range(50)
]
db.add_all(group_leaders)
db.commit()

# 3. Seed customers and map to group leaders
customers = []
customer_leader_map = []

for _ in range(1000):
    segment = choice(list(SegmentEnum))
    channel = choice(list(ChannelEnum))
    signup = fake.date_time_between(start_date="-6M", end_date="now")
    customer = Customer(
        name=fake.name(),
        email=fake.unique.email(),
        segment=segment,
        registration_channel=channel,
        signup_date=signup
    )
    customers.append(customer)

db.add_all(customers)
db.commit()

# Map customers to group leaders randomly
for customer in customers:
    group_leader = choice(group_leaders)
    mapping = CustomerGroupLeaderMap(customer_id=customer.id, group_leader_id=group_leader.id)
    customer_leader_map.append(mapping)

db.add_all(customer_leader_map)
db.commit()

# 4. Seed products
categories = ["Produce", "Stationery", "Snacks", "Beverages"]
product_names = ["Apple", "Tomato", "Banana", "Notebook", "Pen", "Juice", "Cookies"]

products = [
    Product(
        name=name,
        category=choice(categories),
        type="fresh produce" if name in ["Apple", "Tomato", "Banana"] else "other",
        price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
    )
    for name in product_names
]

db.add_all(products)
db.commit()

# 5. Seed orders and order items
orders = []
order_items = []

for customer in customers:
    for _ in range(randint(1, 5)):  # Each customer makes 1–5 orders
        order_date = fake.date_time_between(start_date=customer.signup_date, end_date="now")
        selected_products = sample(products, randint(1, 3))
        order = Order(
            customer_id=customer.id,
            order_datetime=order_date,
            total_amount=0  # We'll update this below
        )
        db.add(order)
        db.flush()  # Get order.id before committing

        total = 0
        for product in selected_products:
            qty = randint(1, 5)
            item = OrderItem(order_id=order.id, product_id=product.id, quantity=qty)
            order_items.append(item)
            total += product.price * qty

        order.total_amount = round(total, 2)
        orders.append(order)

db.commit()
db.add_all(order_items)
db.commit()

print("✅ Database seeded with customers, leaders, products, and orders.")
db.close()
