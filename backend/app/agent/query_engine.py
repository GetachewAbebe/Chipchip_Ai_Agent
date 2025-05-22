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


# ✅ Context instruction injected to the system prompt
INSTRUCTIONS = """
You are a data analyst assistant for ChipChip, a social marketplace grocery platform.

🎯 You only respond to meaningful business-related queries about the ChipChip platform data.
If the question is not related to the ChipChip database (e.g. "tell me a joke"), respond with:
"I can only help with data questions related to the ChipChip platform."

💡 Your tasks:
- Translate marketing questions into SQL queries.
- Use only the provided database tables.
- Do not hallucinate field names or data.
- Use JOINs when needed to fetch human-readable values like group leader names or product names instead of IDs.

🧠 Always:
- Replace internal IDs like `group_leader_id` with readable values like `group_leader_name`.
- Format answers clearly and concisely.
- Suggest a chart type if suitable (e.g., bar, line, pie).
- Respond with "No data found" if there are no results instead of fabricating.

Your responses should be helpful for marketing dashboards and decision-makers.
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

            # ✨ Post-processing for better formatting and replacements
            final_answer = self._post_process_output(raw_answer)
            chart_type = self._extract_chart_hint(raw_answer)

            return {
                "answer": final_answer,
                "chart_suggestion": chart_type,
                "session_id": session_id
            }

        except Exception as e:
            return {"error": str(e)}

    def _post_process_output(self, text: str) -> str:
        """
        Replace technical IDs with friendly names (simulated here).
        In production, this should query the database.
        """
        id_to_name = {
            "1": "Abebe",
            "2": "Fatuma",
            "3": "Samuel"
        }
        for gid, name in id_to_name.items():
            text = text.replace(f"group_leader_id = {gid}", f"group_leader = {name}")
            text = text.replace(f"group_leader_id: {gid}", f"group_leader: {name}")
        return text

    def _extract_chart_hint(self, text: str) -> Optional[str]:
        """
        Naively detect a chart suggestion from the LLM output.
        """
        lowered = text.lower()
        if "bar chart" in lowered:
            return "bar"
        elif "line chart" in lowered or "trend" in lowered:
            return "line"
        elif "pie chart" in lowered:
            return "pie"
        return None


# ✅ Exposed instance to be used in chat/ask endpoints
default_query_engine = QueryEngine()
