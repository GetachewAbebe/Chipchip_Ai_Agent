from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import examples, chat, logs  # ask removed

app = FastAPI(title="ChipChip AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register active routes only
app.include_router(chat.router)
app.include_router(examples.router)
app.include_router(logs.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
