from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.db import models, database
from app.db.seed_data import seed_if_needed
from app.agent.query_engine import agent_executor

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=database.engine)
    seed_if_needed()

@app.get("/")
def root():
    return {"message": "ChipChip backend running"}

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    try:
        response = agent_executor.run(question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
