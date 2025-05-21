import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

# Setup
fake = Faker()
DATA_DIR = Path("backend/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Debug logger
def log(msg):
    print(f"[DEBUG] {msg}")

# Constants
CHANNELS = ['organic', 'referral', 'paid_ad']
CAMPAIGNS = ['facebook', 'influencer', 'google_ads']
SEGMENTS = ['Working Professionals', 'Students', 'Parents', 'Retired']
PRODUCT_DEFS = [
    {"name": "Carrot", "category": "vegetable", "price": 1.2, "is_fresh_produce": True},
    {"name": "Apple", "category": "fruit", "price": 0.8, "is_fresh_produce": True},
    {"name": "Banana", "category": "fruit", "price": 0.6, "is_fresh_produce": True},
    {"name": "Rice", "category": "grain", "price": 2.2, "is_fresh_produce": False},
    {"name": "Tomato", "category": "vegetable", "price": 1.0, "is_fresh_produce": True},
    {"name": "Lentils", "category": "grain", "price": 3.0, "is_fresh_produce": False},
    {"name": "Orange", "category": "fruit", "price": 1.1, "is_fresh_produce": True},
    {"name": "Spinach", "category": "vegetable", "price": 0.9, "is_fresh_produce": True},
    {"name": "Quinoa", "category": "grain", "price": 4.0, "is_fresh_produce": False},
    {"name": "Pear", "category": "fruit", "price": 1.3, "is_fresh_produce": True}
]

# Generate users
log("Generating users...")
users = []
for i in range(1, 201):
    signup_offset = random.randint(0, 180)
    signup_date = datetime.now() - timedelta(days=signup_offset)
    users.append({
        "id": i,
        "name": fake.name(),
        "email": fake.unique.email(),
        "channel": random.choice(CHANNELS),
        "acquisition_campaign": random.choice(CAMPAIGNS),
        "signup_date": signup_date,
        "segment": random.choice(SEGMENTS),
        "created_at": signup_date
    })
log(f"✅ Created {len(users)} users.")

# Group leaders
log("Generating group leaders...")
group_leaders = [{"id": i+1, "user_id": users[i]["id"], "created_at": users[i]["created_at"]} for i in range(40)]
log(f"✅ Created {len(group_leaders)} group leaders.")

# Products
log("Generating products...")
products = [{"id": i+1, **prod, "created_at": datetime.now()} for i, prod in enumerate(PRODUCT_DEFS)]
price_lookup = {p["id"]: p["price"] for p in products}
log(f"✅ Created {len(products)} products.")

# Orders + OrderItems
log("Generating orders and order items with total order value and is_first_order...")
orders = []
order_items = []
order_id_counter = 1
order_item_id = 1
user_first_order_flag = {}

for _ in range(2200):
    user = random.choice(users)
    group_leader = random.choice(group_leaders)
    timestamp = user["signup_date"] + timedelta(days=random.randint(0, 120), hours=random.randint(6, 22))
    is_first_order = not user_first_order_flag.get(user["id"], False)
    user_first_order_flag[user["id"]] = True

    items = []
    total_value = 0.0
    for _ in range(random.randint(1, 4)):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price = price_lookup[product["id"]]
        total_value += price * quantity
        items.append({
            "id": order_item_id,
            "order_id": order_id_counter,
            "product_id": product["id"],
            "quantity": quantity,
            "created_at": timestamp
        })
        order_item_id += 1
    order_items.extend(items)
    orders.append({
        "id": order_id_counter,
        "user_id": user["id"],
        "group_leader_id": group_leader["id"],
        "timestamp": timestamp,
        "order_total_value": round(total_value, 2),
        "is_first_order": is_first_order,
        "created_at": timestamp
    })
    order_id_counter += 1
log(f"✅ Created {len(orders)} orders and {len(order_items)} order items.")

# Save to CSV
log("Saving CSV files with new schema...")
pd.DataFrame(users).to_csv(DATA_DIR / "users.csv", index=False)
pd.DataFrame(group_leaders).to_csv(DATA_DIR / "group_leaders.csv", index=False)
pd.DataFrame(products).to_csv(DATA_DIR / "products.csv", index=False)
pd.DataFrame(orders).to_csv(DATA_DIR / "orders.csv", index=False)
pd.DataFrame(order_items).to_csv(DATA_DIR / "order_items.csv", index=False)
log("✅ CSV export complete. Files saved to backend/data/")
