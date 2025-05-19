from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import endpoints

app = FastAPI()


@app.get("/")
def root():
    return {"message": "ChipChip Agent API is live"}
# ✅ Enable CORS for frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(endpoints.router)
