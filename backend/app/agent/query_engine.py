from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from app.db.database import engine
import os

# Reuse SQLAlchemy engine
db = SQLDatabase(engine)

# LangChain model setup (use gpt-3.5-turbo or gpt-4)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Build the SQL agent
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True,
)
