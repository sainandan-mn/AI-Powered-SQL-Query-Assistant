
⸻

AI-Powered SQL Query Assistant

Overview

This project implements a secure and production-oriented Text-to-SQL system that allows users to query a MySQL database using plain English. A large language model (Google Gemini) is used to generate SQL queries, which are then passed through a custom validation layer before execution.

Unlike typical LLM-powered database tools, this system does not blindly trust model output. Every generated query is verified against the database schema and filtered for unsafe operations before it is allowed to run.

⸻

Problem Statement

Natural language interfaces for databases introduce multiple risks:
	•	LLMs may hallucinate table or column names
	•	Generated queries may include destructive operations
	•	Users may unknowingly request unsafe actions
	•	Production databases require strict access control

Most Text-to-SQL tools prioritize convenience over safety, making them unsuitable for real systems.

⸻

Solution

This system introduces a validation-first architecture.

A Gemini-powered SQL generator is paired with a backend validation layer that:
	•	Ensures only SELECT queries are allowed
	•	Blocks forbidden operations such as DROP, DELETE, and UPDATE
	•	Verifies table and column references against the live schema
	•	Normalizes and sanitizes queries before execution

Only validated queries are executed against the database.

⸻

Execution Flow
User (Browser)
   ↓
Streamlit UI (app.py)
   ↓
SQL Generator (Gemini LLM)
   ↓
Validation Layer
   - Schema Check
   - Forbidden Operations Filter
   - Normalization
   ↓
Query Executor
   ↓
MySQL Database
   ↓
Results Displayed to User


⸻

Technology Stack
	•	Python 3.11
	•	Streamlit
	•	Google Gemini (Generative AI)
	•	LangChain
	•	MySQL
	•	SQLAlchemy
	•	Pandas
	•	Bash (Environment setup)

⸻

High-Level Architectur

⸻

Project Structure
AI-Powered-SQL-Query-Assistant/
├── README.md               # Project documentation
├── app.py                # Streamlit UI & request controller
├── python_backend.py    # Production backend with validation
├── raw_backend.py       # Experimental backend (no validation)
├── assets/              # Architecture diagrams & UI images
└── .gitignore

