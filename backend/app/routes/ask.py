# app/routes/ask.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import json
from typing import Optional

from app.utils.logger import logger
from app.agent.query_engine import default_query_engine

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = Field(default=None)  # Add optional session ID

@router.post("/ask")
async def ask(request: Request):
    try:
        # Parse request body
        body = await request.json()
        
        # Validate request
        question_request = QuestionRequest(**body)
        
        # Generate a default session ID if not provided
        session_id = question_request.session_id or str(hash(request.client.host))
        
        # Log the incoming question
        logger.info(f"Received question: {question_request.question}")
        
        # Run query using the query engine
        result = default_query_engine.run_query(
            question=question_request.question, 
            session_id=session_id
        )
        
        # Check for errors in the result
        if "error" in result:
            logger.error(f"Query error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Prepare successful response
        return {
            "status": "success",
            "question": question_request.question,
            "answer": result.get("answer", ""),
            "session_id": session_id
        }

    except json.JSONDecodeError:
        logger.error("Invalid JSON in request")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
