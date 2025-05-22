# app/routes/ask.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import json
import traceback
import uuid
from typing import Optional

from app.utils.logger import logger
from app.agent.query_engine import default_query_engine

router = APIRouter(prefix="/ask", tags=["Ask"])

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = Field(default=None)

@router.post("/")
async def ask(request: Request):
    try:
        body = await request.json()
        question_request = QuestionRequest(**body)
        session_id = question_request.session_id or str(uuid.uuid4())

        logger.info(f"[ASK] ❓ Question: {question_request.question} | Session: {session_id}")

        result = default_query_engine.run_query(
            question=question_request.question,
            session_id=session_id
        )

        if "error" in result:
            logger.error(f"[ASK] ❌ Query Error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "question": question_request.question,
            "answer": result.get("answer", ""),
            "session_id": session_id,
            "sql": result.get("sql", None)
        }

    except json.JSONDecodeError:
        logger.error("[ASK] ❌ Invalid JSON")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as ve:
        logger.error(f"[ASK] ❌ Validation Error: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.error(f"[ASK] 🔥 Internal Server Error: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")
