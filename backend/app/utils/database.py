import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")  # Use env var in Render

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
