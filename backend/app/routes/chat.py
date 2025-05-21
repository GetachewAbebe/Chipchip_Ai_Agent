# app/routes/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from app.utils.database import engine

router = APIRouter(prefix="/chat", tags=["Chat"])

# LLM and DB setup
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
db = SQLDatabase(engine)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# In-memory session storage
memory_sessions = {}

# Request schema
class ChatRequest(BaseModel):
    question: str
    session_id: str

@router.post("/")
async def chat_with_agent(request: ChatRequest):
    session_id = request.session_id

    # Use existing or create new memory for session
    if session_id not in memory_sessions:
        memory_sessions[session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    memory = memory_sessions[session_id]

    chat_agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
    )

    try:
        result = chat_agent.run(request.question)
        return {"answer": result}
    except Exception as e:
        return {"error": str(e)}
