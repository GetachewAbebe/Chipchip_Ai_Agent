from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.utils.logger import logger  # ✅ Import logger

router = APIRouter()

feedback_store = []  # In-memory store for now

class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int  # 1 (bad) to 5 (excellent)
    comment: str = ""

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest):
    try:
        feedback_store.append(feedback.dict())
        return {"status": "received", "message": "Thank you for your feedback!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
