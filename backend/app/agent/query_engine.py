from typing import Optional, Dict, Any
from pathlib import Path
import re

from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_toolkits import create_sql_agent
from langchain_core.messages import SystemMessage
from sqlalchemy import text as sql_text

from app.utils.database import engine


def load_schema_text() -> str:
    schema_path = Path(__file__).resolve().parents[2] / "backend/database/schema.sql"
    try:
        return schema_path.read_text()
    except Exception:
        return "-- Schema could not be loaded."


def get_system_message_with_schema(schema: str) -> str:
    return f"""
You are ChipChip’s AI-powered data analyst. You are in an ongoing conversation with a marketing stakeholder.

🧠 Use the previous chat context to answer follow-up questions. For example:
- If the user says “What about December?”, refer to the last query.
- If they say “Show the full list”, continue the previous answer.
- Don’t ask them to repeat themselves — remember for them.

⚠️ DO NOT use markdown formatting (like triple backticks ``` or ```sql) in your SQL queries. Only write raw SQL.

🔍 Database Schema:
{schema}

🔹 Business Rules:
- Group orders have `groups_carts_id` NOT NULL.
- Use readable names:
    • `users.name` instead of `user_id`
    • `products.name`, `categories.name`
    • When referencing group leaders, join `users` ON `users.id = groups.created_by`
- Use `order_date` for filtering
- Use `DATE_TRUNC('month', order_date)` for monthly stats
- Use `EXTRACT(DOW FROM order_date)` for weekends (0 = Sunday, 6 = Saturday)
- Always return actual query results, not just summaries or explanations.

❗ If no data is found, say: “No data available for that query.”
❗ If the question is not business-related, say: “I only answer business-related questions for the ChipChip platform.”
"""


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
        system_message = SystemMessage(content=get_system_message_with_schema(schema_text))

        return create_sql_agent(
            llm=self.llm,
            toolkit=toolkit,
            memory=memory,
            system_message=system_message,
            verbose=True
        )

    def run_query(self, question: str, session_id: str) -> Dict[str, Any]:
        try:
            agent = self.create_agent(session_id)
            result = agent.invoke({"input": question})

            raw_answer = result.get("output", "") if isinstance(result, dict) else result
            final_answer = self._post_process_output(str(raw_answer))
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

        # Clean up markdown formatting if it slips in
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


# Shared instance to import in routes/chat.py
default_query_engine = QueryEngine()
