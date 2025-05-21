from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import ask, examples, chat, feedback, logs  # ✅ No backend prefix

app = FastAPI(title="ChipChip AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chipchip-ai-agent-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(ask.router)
app.include_router(chat.router)
app.include_router(feedback.router)
app.include_router(examples.router)
app.include_router(logs.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
