## ChipChip AI Agent

The ChipChip AI Agent is a proof-of-concept (PoC) application designed to empower the marketing team of ChipChip, a social marketplace grocery platform, with data-driven insights. The agent allows users to ask natural language questions (e.g., "How many orders per group?") and retrieves answers from a structured database, providing clear responses and visualization suggestions (e.g., bar charts). The system features a React-based frontend, a FastAPI backend, and a PostgreSQL database for persistent chat history, hosted on Render and Railway.

## Live Demo

Frontend: https://chipchip-ai-agent-frontend.onrender.com/
Backend API: https://chipchip-ai-agent-backend.onrender.com/docs

## Features

Natural Language Queries: Translate marketing questions into SQL using LangChain and OpenAI's GPT-3.5-turbo.
Data-Driven Insights: Query data on users, groups, orders, and products in the ChipChip marketplace.
Conversational Context: Maintain chat history per session, stored in PostgreSQL on Railway.
User-Friendly Interface: React frontend with chat history management, PDF export, and visualization suggestions.
Scalable Backend: FastAPI server with SQLAlchemy for database interactions.

## Architecture

The application follows a client-server architecture:
Frontend: React (AskAgent.jsx) for user interaction, fetching chat history and sending queries.
Backend: FastAPI (main.py, chat.py, query_engine.py) handles API requests, query processing, and database operations.
AI Agent: LangChain with SQLDatabaseToolkit and GPT-3.5-turbo translates queries to SQL.
Database: PostgreSQL (Railway) stores marketplace data and chat history.
Memory: ConversationBufferMemory (backend) for LLM context; PostgreSQL for persistent chat history.

## Technology Stack:

Frontend: React 18, Tailwind CSS, jsPDF, uuid
Backend: FastAPI, LangChain, OpenAI GPT-3.5-turbo, SQLAlchemy, psycopg2
Database: PostgreSQL (Railway)
Deployment: Render (frontend/backend), Railway (database)

## Usage

## Access the Application:

Visit https://chipchip-ai-agent-frontend.onrender.com/.

Start a new chat or load an existing session from the sidebar.

## Ask Questions:

Type queries like:

"How many orders were placed by each group?"

"What are the top-selling products by revenue?"

"Show order trends for users who joined in 2024 by month"

Press Enter or click the paper plane icon to send.

## View Responses:

Responses appear with chart suggestions (e.g., "Suggested Chart: bar").

Chat history is saved to PostgreSQL and accessible across sessions.

## Manage Chats:

Rename, delete, or download chats as PDFs using the sidebar dropdown.

Switch between sessions to review past queries.


In-Memory LLM Context: ConversationBufferMemory is in-memory, lost on server restart (though chat history persists in PostgreSQL).


Hardcoded Mappings: Group leader IDs are mapped manually in query_engine.py.


Chart Rendering: Suggestions are displayed but not visualized.


Scalability: PostgreSQL needs optimization for high concurrency.


Security: No authentication or rate limiting in the API.

## Future Improvements

Persistent Memory: Use Redis for ConversationBufferMemory

Dynamic Mappings: Fetch group leader names from the database.

Chart Visualization: Integrate Chart.js in the frontend.

Security: Add JWT authentication and rate limiting to FastAPI.

Advanced Analytics: Support cohort analysis and predictive insights.

Testing: Add unit tests (Pytest, Jest) and end-to-end tests (Cypress).

## Contact

Project Owner: [Getachew Abebe]

Email: [gechachin@gmail.com]

GitHub: [https://github.com/GetachewAbebe]