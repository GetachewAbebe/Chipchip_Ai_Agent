FROM python:3.10-slim

WORKDIR /app

# Use root-level requirements.txt
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ✅ FIX: Correct path to your actual backend code
COPY backend/app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

