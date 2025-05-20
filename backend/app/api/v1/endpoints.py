from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup for frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    return {"answer": f"Answer to your question: {question}"}
