from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.query_engine import get_agent

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_agent(request: QueryRequest):
    try:
        agent = get_agent()
        answer = agent.run(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
