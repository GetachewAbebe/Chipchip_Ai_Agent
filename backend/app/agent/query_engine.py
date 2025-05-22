from typing import Optional, Dict, Any
from datetime import datetime

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from app.utils.database import engine


INSTRUCTIONS = """
You are a data analyst assistant for ChipChip, a social marketplace grocery platform.

🔹 Only respond to meaningful business-related queries about the ChipChip database.
   If the question is irrelevant (e.g. "how are you"), respond:
   "I can only help with data questions related to the ChipChip platform."

🔹 Translate natural language to SQL using only the available database schema.

🔹 Always JOIN related tables to show human-readable names:
   - If showing group leaders, JOIN `group_leaders` to use `group_leader_name` instead of `group_leader_id`.
   - Similarly, use product names, user names, and cohort labels instead of raw IDs.

🔹 Format answers clearly and concisely for business use.
🔹 Suggest a chart type (bar, line, pie) if relevant.
🔹 If no data found, say: "No data available for that query."
"""

def get_prompt_with_context():
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=INSTRUCTIONS),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])


class QueryEngine:
    def __init__(
        self,
        db: Optional[SQLDatabase] = None,
        llm: Optional[ChatOpenAI] = None
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

    def create_agent(self, session_id: str) -> Any:
        memory = self.get_or_create_memory(session_id)
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)

        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            prompt=get_prompt_with_context(),
            handle_parsing_errors=True,
            verbose=True
        )

    def run_query(self, question: str, session_id: str) -> Dict[str, Any]:
        try:
            agent = self.create_agent(session_id)
            raw_answer = agent.run(question)

            final_answer = self._post_process_output(raw_answer)
            chart_type = self._extract_chart_hint(final_answer)

            return {
                "answer": final_answer,
                "chart_suggestion": chart_type,
                "session_id": session_id
            }

        except Exception as e:
            return {"error": str(e)}

    def _post_process_output(self, text: str) -> str:
        """
        Replace any group_leader_id references with group_leader_name fallback mapping.
        In production, you should fetch from the database.
        """
        group_leader_map = {
            "26": "Fatuma",
            "17": "Abebe",
            "33": "Samuel",
        }

        for gid, name in group_leader_map.items():
            text = text.replace(f"group_leader_id = {gid}", f"group_leader = {name}")
            text = text.replace(f"group_leader_id: {gid}", f"group_leader: {name}")
            text = text.replace(f"group_leader_id {gid}", f"group_leader {name}")
            text = text.replace(gid, name) if "group_leader_id" in text else text

        return text

    def _extract_chart_hint(self, text: str) -> Optional[str]:
        lowered = text.lower()
        if "bar chart" in lowered:
            return "bar"
        elif "line chart" in lowered or "trend" in lowered:
            return "line"
        elif "pie chart" in lowered:
            return "pie"
        return None


# Exported agent for use in chat.py or ask.py
default_query_engine = QueryEngine()
