from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json
from app.utils.setup_and_seed_db import seed_database


# 🧩 Load environment variables
load_dotenv()

# 🔁 Import seed function and router
from app.utils.setup_and_seed_db import seed_database
from app.routes import seed

app = FastAPI()

# 🌐 Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic model for input
class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

# 🔄 Seed on startup if not already seeded

@app.on_event("startup")
def startup_event():
    seed_database()


# 🔌 Include seed-data endpoint
app.include_router(seed.router)

# 🤖 Main AI endpoint
@app.post("/ask")
async def ask(request: Request):
    try:
        body = await request.json()
        question_request = QuestionRequest(**body)
        question = question_request.question
        answer = generate_ai_response(question)

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

# 📄 Fake AI response
def generate_ai_response(question: str) -> str:
    if not question:
        return "Please provide a valid question."
    return f"AI response to: '{question}'. This is a placeholder response."

# 🔍 Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Service is up and running"}
