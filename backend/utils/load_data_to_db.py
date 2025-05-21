import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Rest of your existing code
from backend.utils.models import Base, User, GroupLeader, Product, Order, OrderItem
# Load environment variables
load_dotenv()

# Import models

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Data directory
DATA_DIR = "backend/data"

def load_csv_to_model(model, file_name):
    try:
        path = os.path.join(DATA_DIR, file_name)
        df = pd.read_csv(path)

        # Convert datetime fields if present
        for col in df.columns:
            if "date" in col or "timestamp" in col or "created_at" in col:
                df[col] = pd.to_datetime(df[col])

        # Insert data into DB
        records = [model(**row) for row in df.to_dict(orient="records")]
        session.add_all(records)
        session.commit()
        print(f"✅ Inserted {len(records)} rows into {model.__tablename__}")
    except Exception as e:
        session.rollback()
        print(f"❌ Error inserting data into {model.__tablename__}: {e}")

# Load data
load_csv_to_model(User, "users.csv")
load_csv_to_model(GroupLeader, "group_leaders.csv")
load_csv_to_model(Product, "products.csv")
load_csv_to_model(Order, "orders.csv")
load_csv_to_model(OrderItem, "order_items.csv")

# Close the session
session.close()
