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

High-Level Architecture


⸻

Project Structure

AI-Powered-SQL-Query-Assistant/
├── README.md               # Project documentation
├── app.py                # Streamlit UI & request controller
├── python_backend.py    # Production backend with validation
├── raw_backend.py       # Experimental backend (no validation)
├── assets/              # Architecture diagrams & UI images
└── .gitignore


⸻

Components Explained

1. Streamlit UI (app.py)
	•	Accepts user queries in natural language
	•	Displays generated SQL
	•	Displays validated SQL
	•	Renders database results in a table
	•	Acts as the controller between user and backend

⸻

2. SQL Generator (Gemini LLM)
	•	Receives the full database schema
	•	Converts natural language into SQL
	•	Returns a single-line query with no formatting or explanation
	•	Acts as a query suggestion engine, not a trusted executor

⸻

3. Validation Layer (python_backend.py)

This is the core safety system.

It performs:
	•	Schema validation (tables and columns must exist)
	•	Operation filtering (blocks non-SELECT queries)
	•	Query normalization (format cleanup and sanitization)

If any rule fails, execution is blocked.

⸻

4. Query Executor
	•	Runs only validated SQL
	•	Connects to MySQL using SQLAlchemy
	•	Returns structured results to the UI

⸻

5. Experimental Backend (raw_backend.py)
	•	Generates SQL using Gemini
	•	Skips validation
	•	Used for testing, benchmarking, and comparison
	•	Demonstrates why validation is critical

⸻

Security Model
	•	API keys stored as environment variables
	•	Database credentials excluded from GitHub using .gitignore
	•	No secrets hardcoded in source code
	•	Backend-only database access
	•	LLM output sandboxed by validation rules

⸻

Setup & Execution

Set Environment Variables

export GEMINI_API_KEY="your_api_key"
export MYSQL_PASSWORD="your_mysql_password"


⸻

Install Dependencies

pip install streamlit langchain langchain-community langchain-google-genai pymysql sqlalchemy pandas


⸻

Run Application

streamlit run app.py


⸻

Validation Demonstration

Generated SQL

Shows the raw output produced by Gemini.

Validated SQL

Displays the same query after passing safety and schema checks.

Result Table

Only appears if the query passes validation and executes successfully.

⸻

Use Case

This project demonstrates how LLMs can be safely integrated into real database systems by treating them as assistants rather than authorities.

It is designed for:
	•	AI engineering
	•	Data engineering
	•	Secure system design
	•	Cloud and backend roles

⸻

Future Improvements
	•	RAGAS-based evaluation for SQL faithfulness and correctness
	•	Query confidence scoring
	•	Natural language SQL explanation
	•	Role-based database access
	•	Multi-database support (PostgreSQL, BigQuery, Snowflake)
	•	Query performance analysis

⸻

Key Learnings
	•	Secure LLM integration patterns
	•	Schema-aware query validation
	•	Production-safe database access
	•	Streamlit system design
	•	Prompt engineering for structured output
	•	Backend safety enforcement

⸻

Author

Sai Nandan MN
AI Systems | Data Engineering | Cloud | Secure LLM Applications

⸻

If you want, I can also give you a one-minute interview script that walks through this architecture cleanly and confidently.
This README already positions you as someone who understands real-world AI system safety, not just model usage.
