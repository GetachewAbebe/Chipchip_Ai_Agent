from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.utils.logger import logger

router = APIRouter(prefix="/feedback", tags=["Feedback"])

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    feedback: str  # Expected: "Helpful", "Not Helpful", etc.

@router.post("/")
async def receive_feedback(payload: FeedbackRequest):
    try:
        logger.info(f"📩 Feedback received: {payload}")
        # Optionally save to DB or log to a file
        return {"status": "success", "message": "Thank you for your feedback!"}
    except Exception as e:
        logger.error(f"🔥 Error in /feedback: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
