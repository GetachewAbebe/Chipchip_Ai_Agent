import uuid
import random
from datetime import datetime, timedelta, timezone
import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path
from faker import Faker

fake = Faker()

# Load DB URL
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")

def uid(): return str(uuid.uuid4())

def recent_date(days=730):
    return datetime.now(timezone.utc) - timedelta(days=random.randint(0, days), hours=random.randint(0, 23))

def seed():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("🔄 Seeding data...")

        # USERS
        print("👥 Seeding 120 users...")
        user_ids = []
        group_leader_ids = []
        segments = ["Working Professionals", "Students", "Parents", "Seniors"]
        reg_channels = ["organic", "referral", "paid ad", "email", "influencer"]
        for i in range(120):
            is_leader = i < 20
            name = fake.name()
            uid_ = uid()
            user_ids.append(uid_)
            if is_leader:
                group_leader_ids.append(uid_)

            cur.execute("""
                INSERT INTO users (id, name, email, registration_channel, user_status, user_type, customer_segment, created_at)
                VALUES (%s, %s, %s, %s, 'active', %s, %s, %s)
            """, (
                uid_,
                name,
                fake.email(),
                random.choice(reg_channels),
                'group_leader' if is_leader else 'customer',
                random.choice(segments),
                recent_date()
            ))

        # CATEGORIES
        print("📦 Seeding 5 categories...")
        cat_names = ["Fresh Produce", "Dairy", "Meat", "Snacks", "Bakery"]
        category_ids = {}
        for name in cat_names:
            cid = uid()
            category_ids[name] = cid
            cur.execute("INSERT INTO categories (id, name, status) VALUES (%s, %s, 'active')", (cid, name))

        # PRODUCTS
        print("🛒 Seeding 30 products...")
        product_ids = []
        for i in range(30):
            name = fake.word().capitalize()
            category = random.choice(list(category_ids.values()))
            pid = uid()
            product_ids.append(pid)
            cur.execute("""
                INSERT INTO products (id, name, name_id, status, unit_price)
                VALUES (%s, %s, %s, 'active', %s)
            """, (pid, name, category, round(random.uniform(3, 25), 2)))

        # CAMPAIGNS
        print("📢 Seeding 10 campaigns...")
        campaign_ids = []
        for i in range(10):
            cid = uid()
            campaign_ids.append(cid)
            cur.execute("""
                INSERT INTO campaigns (id, name, channel, start_date, status)
                VALUES (%s, %s, %s, %s, 'active')
            """, (
                cid,
                f"{random.choice(['Holiday', 'Promo', 'Flash'])} Campaign {i+1}",
                random.choice(["facebook", "influencer", "email", "tiktok"]),
                recent_date()
            ))

        # GROUP DEALS
        print("🤝 Seeding 30 group deals...")
        group_deal_ids = []
        for i in range(30):
            gid = uid()
            group_deal_ids.append(gid)
            created_at = recent_date()
            effective_from = created_at + timedelta(days=1)
            cur.execute("""
                INSERT INTO group_deals (id, product_id, max_group_member, group_price, created_at, effective_from)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                gid,
                random.choice(product_ids),
                random.randint(3, 10),
                round(random.uniform(2, 15), 2),
                created_at,
                effective_from
            ))

        # GROUPS
        print("👨‍👩‍👧‍👦 Seeding 50 groups...")
        group_ids = []
        for i in range(50):
            gid = uid()
            group_ids.append(gid)
            cur.execute("""
                INSERT INTO groups (id, group_deals_id, created_by, status, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                gid,
                random.choice(group_deal_ids),
                random.choice(group_leader_ids),
                random.choice(['completed', 'open']),
                recent_date()
            ))

        # GROUP MEMBERS
        print("➕ Seeding 200 group members...")
        for _ in range(200):
            cur.execute("""
                INSERT INTO group_members (id, group_id, user_id, joined_at)
                VALUES (%s, %s, %s, %s)
            """, (
                uid(),
                random.choice(group_ids),
                random.choice(user_ids),
                recent_date()
            ))

        # ORDERS + ORDER ITEMS
        print("📦 Seeding 300 orders and 900+ items...")
        for _ in range(300):
            order_id = uid()
            user_id = random.choice(user_ids)
            group_id = random.choice(group_ids)
            campaign_id = random.choice(campaign_ids)
            order_date = recent_date()

            # Step 1: Insert placeholder order
            cur.execute("""
                INSERT INTO orders (id, groups_carts_id, user_id, status, total_amount, order_date, campaign_id)
                VALUES (%s, %s, %s, 'completed', %s, %s, %s)
            """, (
                order_id, group_id, user_id, 0.0, order_date, campaign_id
            ))

            # Step 2: Insert order items
            total = 0
            for _ in range(random.randint(2, 5)):
                product_id = random.choice(product_ids)
                qty = random.randint(1, 3)
                price = round(random.uniform(4, 20), 2)
                total += price * qty

                cur.execute("""
                    INSERT INTO order_items (id, order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    uid(), order_id, product_id, qty, price
                ))

            # Step 3: Update total_amount
            cur.execute("""
                UPDATE orders SET total_amount = %s WHERE id = %s
            """, (round(total, 2), order_id))

        conn.commit()
        print("✅ Data seeding completed successfully.")

    except Exception as e:
        print("❌ Error during seeding:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    seed()
