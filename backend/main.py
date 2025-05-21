from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import ask  # Import router from routes/ask.py

app = FastAPI(title="ChipChip AI Agent")

# 🌐 Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chipchip-ai-agent-frontend.onrender.com"],  # ⚠️ Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Register the /ask endpoint
app.include_router(ask.router)

# ✅ Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
