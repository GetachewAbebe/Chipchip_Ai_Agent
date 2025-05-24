from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_openai import ChatOpenAI

from app.utils.database import engine


# 🔹 Load schema.sql from file
def load_schema_text() -> str:
    schema_path = Path(__file__).resolve().parents[2] / "backend/database/schema.sql"
    try:
        return schema_path.read_text()
    except Exception:
        return "-- Schema could not be loaded."


# 🔹 Prompt with schema awareness and marketing logic
def get_prompt_with_context(schema: str):
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=f"""
You are ChipChip’s AI-powered data analyst. Use the following database schema and business rules to write accurate and helpful SQL-based answers.

🔍 Database Schema:
{schema}

🔹 Group orders have `groups_carts_id` NOT NULL.
🔹 Use readable names:
   - `users.name` instead of `user_id`
   - `products.name`, `categories.name`
   - Join `users` where `user_type = 'group_leader'`
🔹 Use `order_date` for filtering
🔹 Use `DATE_TRUNC('month', order_date)` for monthly stats
🔹 Use `EXTRACT(DOW FROM order_date)` for weekends

❗ If no data is found, reply with: “No data available for that query.”

Only respond to marketing/business-related queries.
        """),
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
        schema_text = load_schema_text()

        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            prompt=get_prompt_with_context(schema_text),
            handle_parsing_errors=True,
            verbose=True
        )

    def run_query(self, question: str, session_id: str) -> Dict[str, Any]:
        try:
            agent = self.create_agent(session_id)
            response = agent.run(question)

            if "Agent stopped due to iteration limit" in response:
                return {
                    "answer": "⚠️ I couldn’t complete the answer in time. Please rephrase or try a narrower question.",
                    "session_id": session_id
                }

            final_answer = self._post_process_output(response)
            chart_type = self._extract_chart_hint(final_answer)

            return {
                "answer": final_answer,
                "chart_suggestion": chart_type,
                "session_id": session_id
            }

        except Exception as e:
            return {"error": str(e)}

    def _post_process_output(self, text: str) -> str:
        import re
        group_leader_map = {
            "26": "Fatuma",
            "17": "Abebe",
            "33": "Samuel",
        }

        for gid, name in group_leader_map.items():
            text = text.replace(f"user_id = {gid}", f"user = {name}")
            text = text.replace(f"group_leader_id = {gid}", f"group_leader = {name}")
            text = text.replace(gid, name) if "group_leader_id" in text else text

        matches = re.findall(r"\$\s?(\d{4,})(\.\d{1,2})?", text)
        for match in matches:
            raw = match[0] + (match[1] or "")
            try:
                formatted = "${:,.2f}".format(float(raw))
                text = text.replace(f"${raw}", formatted)
            except:
                continue

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


# ✅ Shared instance
default_query_engine = QueryEngine()
