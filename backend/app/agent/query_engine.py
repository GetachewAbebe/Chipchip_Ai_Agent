# app/agent/query_engine.py
from typing import Optional, Dict, Any

# Use more generic imports
from langchain_core.language_models import BaseLanguageModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent import AgentExecutor

# Import your specific database engine
from app.utils.database import engine

# Optional: Allow dependency injection
class QueryEngine:
    def __init__(
        self, 
        db: Optional[SQLDatabase] = None, 
        llm: Optional[BaseLanguageModel] = None
    ):
        # Use provided or default database and LLM
        self.db = db or SQLDatabase(engine)
        self.llm = llm
        
        # Memory management
        self.memory_sessions: Dict[str, ConversationBufferMemory] = {}

    def get_or_create_memory(self, session_id: str) -> ConversationBufferMemory:
        """
        Retrieve or create a memory session for a given session ID
        """
        if session_id not in self.memory_sessions:
            self.memory_sessions[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.memory_sessions[session_id]

    def create_agent(
        self, 
        session_id: str, 
        llm: Optional[BaseLanguageModel] = None
    ) -> AgentExecutor:
        """
        Create an agent with SQL toolkit and memory
        """
        # Use provided LLM or default
        current_llm = llm or self.llm
        
        # Create SQL toolkit
        toolkit = SQLDatabaseToolkit(db=self.db, llm=current_llm)
        
        # Retrieve or create memory for this session
        memory = self.get_or_create_memory(session_id)

        # Initialize and return agent
        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=current_llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
        )

    def run_query(
        self, 
        question: str, 
        session_id: str, 
        llm: Optional[BaseLanguageModel] = None
    ) -> Dict[str, Any]:
        """
        Run a query using the agent
        """
        try:
            # Create agent for this session
            agent = self.create_agent(session_id, llm)
            
            # Run the query
            response = agent.run(question)
            
            return {"answer": response}
        except Exception as e:
            return {"error": str(e)}

# Create a default instance
default_query_engine = QueryEngine()
