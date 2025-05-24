from typing import Optional, Dict, Any
from pathlib import Path
import re

from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import text as sql_text

from app.utils.database import engine


# Load schema file
def load_schema_text() -> str:
    schema_path = Path(__file__).resolve().parents[2] / "backend/database/schema.sql"
    try:
        return schema_path.read_text()
    except Exception:
        return "-- Schema could not be loaded."


# Custom system prompt with memory, schema, business logic
def get_prompt_with_schema(schema: str):
    return ChatPromptTemplate.from_messages([
        SystemMessage(content=f"""
You are ChipChip’s AI-powered data analyst.

🧠 You are in a multi-turn conversation. Always use memory to resolve vague follow-ups like:
- "Show me the full table"
- "What about December?"

⚠️ DO NOT use markdown syntax like triple backticks (``` or ```sql) in SQL queries.

🔍 Use this schema to construct correct SQL:
{schema}

🔹 Business Logic:
- Group orders have `groups_carts_id` NOT NULL
- Use `users.name`, `products.name`, etc.
- Join users where needed for readable names
- Use `DATE_TRUNC('month', order_date)` for monthly grouping
- Use `EXTRACT(DOW FROM order_date)` for day-of-week filters

🎯 Always return meaningful, structured results.
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])


class QueryEngine:
    def __init__(
        self,
        db: Optional[SQLDatabase] = None,
        llm: Optional[ChatOpenAI] = None
    ):
        self.db = db or SQLDatabase(engine)
        self.llm = llm or ChatOpenAI(temperature=0, model="gpt-4o")
        self.memory_sessions: Dict[str, ConversationBufferMemory] = {}

    def get_or_create_memory(self, session_id: str) -> ConversationBufferMemory:
        if session_id not in self.memory_sessions:
            self.memory_sessions[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.memory_sessions[session_id]

    def create_agent(self, session_id: str):
        memory = self.get_or_create_memory(session_id)
        toolkit = SQLDatabaseToolkit(db=self.db, llm=self.llm)
        schema_text = load_schema_text()
        prompt = get_prompt_with_schema(schema_text)

        return initialize_agent(
            tools=toolkit.get_tools(),
            llm=self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory,
            prompt=prompt,
            handle_parsing_errors=True,
            verbose=True,
            max_iterations=10
        )

    def run_query(self, question: str, session_id: str) -> Dict[str, Any]:
        try:
            agent = self.create_agent(session_id)
            result = agent.run(question)

            final_answer = self._post_process_output(str(result))
            chart_type = self._extract_chart_hint(final_answer)

            return {
                "answer": final_answer,
                "chart_suggestion": chart_type,
                "session_id": session_id
            }

        except Exception as e:
            return {"error": str(e)}

    def _post_process_output(self, text: str) -> str:
        text = self.map_user_ids_to_names(text)
        text = text.replace("```sql", "").replace("```", "").strip()

        matches = re.findall(r"\$\s?(\d{4,})(\.\d{1,2})?", text)
        for match in matches:
            raw = match[0] + (match[1] or "")
            try:
                formatted = "${:,.2f}".format(float(raw))
                text = text.replace(f"${raw}", formatted)
            except:
                continue
        return text

    def map_user_ids_to_names(self, text: str) -> str:
        ids = re.findall(r"\b[0-9a-f]{8}-[0-9a-f\-]{27,36}\b", text)
        if not ids:
            return text

        placeholders = ','.join(f"'{id}'" for id in ids)
        query = sql_text(f"SELECT id, name FROM users WHERE id IN ({placeholders})")

        try:
            with engine.connect() as conn:
                results = conn.execute(query).fetchall()
                id_name_map = {str(row[0]): row[1] for row in results}
                for uid, name in id_name_map.items():
                    text = text.replace(uid, name)
        except Exception:
            pass

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


# Shared instance to import in chat.py
default_query_engine = QueryEngine()
