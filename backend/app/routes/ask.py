from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import json
from app.utils.logger import logger  # ✅ Import logger


from app.agent.query_engine import agent_executor  # ✅ Real agent

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)

@router.post("/ask")
async def ask(request: Request):
    try:
        body = await request.json()
        question_request = QuestionRequest(**body)
        question = question_request.question

        # ✅ Use LangChain SQL agent
        answer = agent_executor.run(question)

        return {
            "status": "success",
            "question": question,
            "answer": answer
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
