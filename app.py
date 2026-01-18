import streamlit as st
import os
import re
from urllib.parse import quote_plus

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from python_backend import generate_sql, run_query
# ----------------------------
# Helpers
# ----------------------------
import pandas as pd

def result_to_df(result):
    if not result:
        return None

    if isinstance(result, str):
        return result

    col_count = len(result[0])
    columns = [f"col_{i+1}" for i in range(col_count)]

    return pd.DataFrame(result, columns=columns)
# ----------------------------
# Page Setup
# ----------------------------
st.set_page_config(page_title="Text to SQL Assistant", layout="centered")
st.title("AI SQL Assistant")
st.caption("Ask questions in plain English. Queries are validated before execution.")

# ----------------------------
# DB Connection (cached)
# ----------------------------
@st.cache_resource
def connect_db():
    host = "localhost"
    port = "3306"
    username = "root"
    password = "Sainandan@7"
    database_schema = "text_to_sql"

    password = quote_plus(password)
    mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

    return SQLDatabase.from_uri(mysql_uri)

db = connect_db()

# ----------------------------
# LLM Setup (cached)
# ----------------------------
@st.cache_resource
def load_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-flash-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )

llm = load_llm()

# ----------------------------
# Prompt + Chain
# ----------------------------
def get_schema(_):
    return db.get_table_info()

prompt = ChatPromptTemplate.from_template("""
You are a MySQL expert.

Using ONLY the schema below, write a SQL query for the user's question.
Return ONLY the SQL query in ONE LINE. No markdown. No explanation.

Schema:
{schema}

Question:
{question}

SQL:
""")

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
)

# ----------------------------
# Validation Logic
# ----------------------------
def normalize_sql(sql: str) -> str:
    sql = sql.replace("`", "")
    sql = re.sub(r"\s+", " ", sql)
    return sql.lower().strip()

FORBIDDEN_KEYWORDS = ["drop", "delete", "update", "insert", "alter", "truncate", "create", "replace"]

def is_safe_sql(sql: str) -> bool:
    sql_lower = normalize_sql(sql)
    if not sql_lower.startswith("select"):
        return False
    for word in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{word}\b", sql_lower):
            return False
    return True

def get_schema_map():
    tables = db._inspector.get_table_names()
    schema_map = {}
    for table in tables:
        columns = db._inspector.get_columns(table)
        schema_map[normalize_sql(table)] = [
            normalize_sql(col["name"]) for col in columns
        ]
    return schema_map

def references_valid_schema(sql: str, schema_map: dict) -> bool:
    sql = normalize_sql(sql)

    active_table = None
    for table in schema_map.keys():
        if f" {table} " in f" {sql} ":
            active_table = table
            break

    if not active_table:
        return False

    select_match = re.search(r"select\s+(.*?)\s+from", sql)
    if not select_match:
        return False

    select_cols = [c.strip() for c in select_match.group(1).split(",")]

    where_cols = []
    where_match = re.search(r"where\s+(.*)", sql)
    if where_match:
        conditions = where_match.group(1)
        where_cols = re.findall(r"([a-z0-9_ ]+)\s*(?:=|<|>|like)", conditions)

    all_cols = select_cols + where_cols
    valid_columns = set(schema_map[active_table])

    for col in all_cols:
        if col == "*":
            continue
        if col.strip() not in valid_columns:
            return False

    return True

def validate_sql(sql: str, db):
    if not sql:
        raise ValueError("Empty SQL")
    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL detected")

    schema_map = get_schema_map()
    if not references_valid_schema(sql, schema_map):
        raise ValueError("SQL references invalid table or column")

    return sql

def suggest_filters(db, table, column):
    try:
        sql = f"SELECT DISTINCT {column} FROM {table} LIMIT 10"
        return db.run(sql)
    except:
        return []

# ----------------------------
# UI
# ----------------------------
# ----------------------------
# UI
# ----------------------------
question = st.text_input("Ask your database a question:")

if st.button("Run Query"):
    if not question:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            try:
                response = sql_chain.invoke({"question": question})

                st.subheader("Generated SQL")
                st.code(response, language="sql")

                safe_sql = validate_sql(response, db)

                st.subheader("Validated SQL")
                st.code(safe_sql, language="sql")

                result = db.run(safe_sql)

                st.subheader("Result")

                # Force table rendering
                import pandas as pd
                if isinstance(result, list) and len(result) > 0:
                    df = pd.DataFrame(result)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.write(result)

            except Exception as e:
                st.error(f"Query blocked: {e}")