from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from app.utils.database import engine

app = FastAPI()

# --- LLM and DB Setup ---
db = SQLDatabase(engine)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# --- In-memory cache for user memory sessions ---
memory_sessions = {}

# --- Request model ---
class ChatRequest(BaseModel):
    question: str
    session_id: str  # allow tracking chat history per user/session

# --- Chat agent endpoint ---
@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    # Retrieve or create memory for this session
    if request.session_id not in memory_sessions:
        memory_sessions[request.session_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    memory = memory_sessions[request.session_id]

    # Initialize agent with memory and SQL tools
    chat_agent = initialize_agent(
        tools=toolkit.get_tools(),
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
    )

    try:
        response = chat_agent.run(request.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}
