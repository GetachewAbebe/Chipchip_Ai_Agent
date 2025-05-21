FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY ./backend /app/app

# Expose the port Render expects
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
