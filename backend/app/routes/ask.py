# app/routes/ask.py

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import json
from typing import Optional
import uuid
import traceback

from app.utils.logger import logger
from app.agent.query_engine import default_query_engine

router = APIRouter(prefix="/ask", tags=["Ask"])

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = Field(default=None)

@router.post("/")
async def ask(request: Request):
    try:
        # Parse and validate request
        body = await request.json()
        question_request = QuestionRequest(**body)

        # Use provided session_id or generate one
        session_id = question_request.session_id or str(uuid.uuid4())

        # Log received question
        logger.info(f"[ASK] ❓ Question: {question_request.question} | Session: {session_id}")

        # Call the agent/query engine
        result = default_query_engine.run_query(
            question=question_request.question,
            session_id=session_id
        )

        # If error, raise and log
        if "error" in result:
            logger.error(f"[ASK] ❌ Query error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        # Return answer (and optionally the SQL or intermediate steps)
        return {
            "status": "success",
            "question": question_request.question,
            "answer": result.get("answer", ""),
            "session_id": session_id,
            "sql": result.get("sql", None),  # Optional: only if your engine returns this
        }

    except json.JSONDecodeError:
        logger.error("[ASK] ❌ Invalid JSON received")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    except ValueError as ve:
        logger.error(f"[ASK] ❌ Validation error: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))

    except Exception as e:
        logger.error(f"[ASK] 🔥 Unexpected error: {e}")
        logger.debug(traceback.format_exc())  # Full traceback for debugging
        raise HTTPException(status_code=500, detail="Internal server error")
