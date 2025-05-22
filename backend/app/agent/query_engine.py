# app/agent/query_engine.py
from typing import Optional, Dict, Any

from langchain_core.language_models import BaseLanguageModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent import AgentExecutor

from langchain_openai import ChatOpenAI  # ✅ Add default LLM
from sqlalchemy.exc import SQLAlchemyError

from app.utils.database import engine
from app.utils.logger import logger

class QueryEngine:
    def __init__(
        self,
        db: Optional[SQLDatabase] = None,
        llm: Optional[BaseLanguageModel] = None
    ):
        self.db = db or SQLDatabase(engine)
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

        self.memory_sessions: Dict[str, ConversationBufferMemory] = {}

    def get_or_create_memory(self, session_id: str) -> ConversationBufferMemory:
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
        current_llm = llm or self.llm
        toolkit = SQLDatabaseToolkit(db=self.db, llm=current_llm)
        memory = self.get_or_create_memory(session_id)

        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=current_llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            verbose=True
        )

    def run_query(
        self,
        question: str,
        session_id: str,
        llm: Optional[BaseLanguageModel] = None
    ) -> Dict[str, Any]:
        try:
            logger.info(f"[QueryEngine] 🔎 Running query: '{question}' | session_id={session_id}")
            agent = self.create_agent(session_id, llm)
            response = agent.run(question)

            logger.info(f"[QueryEngine] ✅ Response: {response}")
            return {
                "answer": response
                # Optionally add SQL here if toolkit returns it
            }

        except SQLAlchemyError as db_err:
            logger.error(f"[QueryEngine] ❌ SQLAlchemy error: {db_err}")
            return {"error": f"Database error: {db_err}"}

        except Exception as e:
            logger.error(f"[QueryEngine] 🔥 Unexpected error: {e}")
            return {"error": str(e)}

# ✅ Export default instance
default_query_engine = QueryEngine()
