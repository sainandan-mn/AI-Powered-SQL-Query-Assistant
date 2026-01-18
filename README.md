
AI-Powered SQL Query Assistant

Natural Language → Safe SQL → MySQL using Gemini LLM


⸻

Overview

This project enables users to query a MySQL database using plain English.
It uses Google Gemini (LLM) to generate SQL, a custom validation layer to enforce schema and safety rules, and a Streamlit UI to deliver results in real time.

Unlike typical Text-to-SQL tools, this system treats the LLM as a query suggestion engine, not a trusted authority. Every query is validated before execution.

⸻

Key Highlights
	•	Natural language → SQL using Gemini
	•	Schema-aware validation (no hallucinated tables or columns)
	•	Forbidden operation filtering (blocks DELETE, DROP, UPDATE, etc.)
	•	Secure credential handling with environment variables
	•	Live MySQL execution
	•	Clean frontend-backend separation
	•	Modular backend design for scaling

⸻

Architecture

Data Flow

User → Streamlit UI → SQL Generator (Gemini)
                     → Validation Layer
                     → Query Executor → MySQL Database

The validation layer ensures:
	•	Only SELECT queries run
	•	All tables and columns exist
	•	No destructive operations are allowed

⸻

Project Structure

AI-Powered-SQL-Query-Assistant/
│
├── app.py                 # Streamlit UI & request controller
├── python_backend.py    # Production backend with validation
├── raw_backend.py       # Experimental backend (no validation)
├── assets/              # Architecture & UI visuals
├── README.md
└── .gitignore


⸻

How It Works

1. User Input

Users ask questions in natural language:

“Show first 5 sales orders”
“Find orders where channel is Online”

2. SQL Generation

Gemini receives the full database schema and generates a SQL query.

3. Validation Layer

The system checks:
	•	Query starts with SELECT
	•	No forbidden keywords exist
	•	Tables and columns exist in schema

Invalid queries are blocked before reaching the database.

4. Execution & Display

Safe queries are executed in MySQL and results are rendered in a live table.

⸻

Security Model
	•	API keys and database credentials are stored as environment variables
	•	Secrets are excluded from GitHub via .gitignore
	•	LLM output is sandboxed by a validation layer
	•	Database access is backend-only

⸻

Running Locally

Set environment variables

export GEMINI_API_KEY="your_api_key"
export MYSQL_PASSWORD="your_mysql_password"

Install dependencies

pip install streamlit langchain langchain-community langchain-google-genai pymysql sqlalchemy pandas

Start the app

streamlit run app.py


⸻

Future Improvements
	•	RAGAS-based evaluation for SQL faithfulness and correctness
	•	Query confidence scoring
	•	Natural language SQL explanation
	•	Multi-database support (Postgres, BigQuery, Snowflake)
	•	Role-based query permissions

⸻


Author

Sai Nandan MN


