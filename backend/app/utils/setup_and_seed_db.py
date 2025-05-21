import os
import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# DB Credentials from .env
DATABASE_URL = "postgresql://postgres:ZENStvKGjPthLKeuBBjsdwIsDnpDhZUm@maglev.proxy.rlwy.net:17086/railway"

# Setup SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Data folder
DATA_DIR = Path("backend/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

# Table Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    channel = Column(String)

class GroupLeader(Base):
    __tablename__ = "group_leaders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_leader_id = Column(Integer, ForeignKey("group_leaders.id"))
    timestamp = Column(DateTime)

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

def seed_database():
    Base.metadata.create_all(engine)
    session = SessionLocal()

    if session.query(User).first():
        print("✅ Data already exists. Skipping insertion.")
        session.close()
        return

    print("🚀 Seeding data...")

    # Users
    channels = ['organic', 'referral', 'paid_ad']
    users = [User(name=fake.name(), email=fake.unique.email(), channel=fake.random_element(channels)) for _ in range(50)]
    session.add_all(users)
    session.commit()

    # Group Leaders
    group_leaders = [GroupLeader(user_id=u.id) for u in users[:10]]
    session.add_all(group_leaders)
    session.commit()

    # Products
    categories = ['vegetable', 'fruit', 'grain']
    products = [Product(name=fake.word(), category=fake.random_element(categories), price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)) for _ in range(20)]
    session.add_all(products)
    session.commit()

    # Orders
    orders = []
    for _ in range(100):
        user = fake.random_element(users)
        leader = fake.random_element(group_leaders)
        orders.append(Order(user_id=user.id, group_leader_id=leader.id, timestamp=fake.date_time_between(start_date='-30d', end_date='now')))
    session.add_all(orders)
    session.commit()

    # OrderItems
    order_items = []
    for order in orders:
        for _ in range(fake.random_int(min=1, max=3)):
            product = fake.random_element(products)
            quantity = fake.random_int(min=1, max=5)
            order_items.append(OrderItem(order_id=order.id, product_id=product.id, quantity=quantity))
    session.add_all(order_items)
    session.commit()

    # Export to CSVs
    pd.DataFrame([u.__dict__ for u in users]).drop('_sa_instance_state', axis=1).to_csv(DATA_DIR / 'users.csv', index=False)
    pd.DataFrame([gl.__dict__ for gl in group_leaders]).drop('_sa_instance_state', axis=1).to_csv(DATA_DIR / 'group_leaders.csv', index=False)
    pd.DataFrame([p.__dict__ for p in products]).drop('_sa_instance_state', axis=1).to_csv(DATA_DIR / 'products.csv', index=False)
    pd.DataFrame([o.__dict__ for o in orders]).drop('_sa_instance_state', axis=1).to_csv(DATA_DIR / 'orders.csv', index=False)
    pd.DataFrame([oi.__dict__ for oi in order_items]).drop('_sa_instance_state', axis=1).to_csv(DATA_DIR / 'order_items.csv', index=False)

    print("✅ Seeding complete. CSVs saved.")
    session.close()

if __name__ == "__main__":
    seed_database()
