# app/routes/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.agent.query_engine import default_query_engine
from app.utils.logger import logger

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

@router.post("/")
async def chat_with_agent(request: ChatRequest):
    try:
        session_id = request.session_id or "frontend-session"
        logger.info(f"[CHAT] ❓ {request.question} | Session: {session_id}")

        result = default_query_engine.run_query(
            question=request.question,
            session_id=session_id
        )

        if "error" in result:
            logger.error(f"[CHAT] ❌ {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "answer": result["answer"],
            "session_id": session_id
        }

    except Exception as e:
        logger.error(f"[CHAT] 🔥 Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
