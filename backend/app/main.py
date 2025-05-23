# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import chat

app = FastAPI(title="ChipChip AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Only include what you're using
app.include_router(chat.router)
# app.include_router(examples.router)
# app.include_router(logs.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
