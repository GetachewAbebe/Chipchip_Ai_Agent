# app/routes/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.query_engine import default_query_engine

router = APIRouter(prefix="/chat", tags=["Chat"])

# Request schema
class ChatRequest(BaseModel):
    question: str
    session_id: str

@router.post("/")
async def chat_with_agent(request: ChatRequest):
    if not request.question.strip():
        return {"error": "Empty question provided."}
    if not request.session_id.strip():
        return {"error": "Missing session ID."}

    return default_query_engine.run_query(
        question=request.question,
        session_id=request.session_id
    )
