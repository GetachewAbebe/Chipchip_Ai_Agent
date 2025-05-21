from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    # Return a dummy placeholder answer
    return {"answer": f"Answer to your question: '{question}' — This is a placeholder response from the AI agent."}
