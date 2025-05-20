from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    return {"answer": f"Answer to your question: {question}"}
