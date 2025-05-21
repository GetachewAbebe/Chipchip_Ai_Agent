from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.agent.query_engine import chat_agent_executor
from backend.utils.logger import logger  # ✅ Logging support

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat")
async def chat_with_memory(request: ChatRequest):
    try:
        # Run the chat agent with memory
        response = chat_agent_executor.run(request.question)

        # ✅ Log the question and response
        logger.info(f"[CHAT] Question: {request.question} | Answer: {response}")

        return {
            "status": "success",
            "question": request.question,
            "answer": response,
        }

    except Exception as e:
        logger.error(f"[CHAT] Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong with the AI agent.")
