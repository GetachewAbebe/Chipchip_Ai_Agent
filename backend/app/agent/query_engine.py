from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from app.utils.database import engine  # Make sure this points to your SQLAlchemy engine

# ✅ Step 1: Reuse SQLAlchemy engine
db = SQLDatabase(engine)

# ✅ Step 2: Base LLM setup (OpenAI GPT)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# ✅ Step 3: Stateless agent for single-shot queries (used in /ask)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
)

# ✅ Step 4: Memory for multi-turn chat (used in /chat)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ✅ Step 5: Chat agent with memory (react-style)
chat_agent_executor = initialize_agent(
    tools=[],  # Optional: add SQL tools or custom tools later
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
)
