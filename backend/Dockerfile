FROM python:3.10-slim

# Install Python deps
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app and wait script
COPY ./backend/app /app/app
COPY ./backend/wait_for_postgres.py /app/wait_for_postgres.py

# Wait for DB using Python, then run FastAPI
CMD ["sh", "-c", "python /app/wait_for_postgres.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
