import os
import re
from urllib.parse import quote_plus

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# ----------------------------
# Database
# ----------------------------
def connect_db():
    host = "localhost"
    port = "3306"
    username = "root"
    password = quote_plus(os.getenv("MYSQL_PASSWORD"))
    database = "text_to_sql"

    uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(uri)


# ----------------------------
# LLM
# ----------------------------
def load_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-flash-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )


# ----------------------------
# Prompt + Chain
# ----------------------------
def build_chain(db, llm):

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

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )


# ----------------------------
# Validation
# ----------------------------
FORBIDDEN = ["drop", "delete", "update", "insert", "alter", "truncate", "create", "replace"]


def normalize(sql):
    sql = sql.replace("`", "")
    sql = re.sub(r"\s+", " ", sql)
    return sql.lower().strip()


def is_safe(sql):
    sql = normalize(sql)
    if not sql.startswith("select"):
        return False
    for word in FORBIDDEN:
        if re.search(rf"\b{word}\b", sql):
            return False
    return True


def validate_sql(sql, db):
    if not sql:
        raise ValueError("Empty SQL")
    if not is_safe(sql):
        raise ValueError("Unsafe SQL detected")
    return sql


# ----------------------------
# Public API
# ----------------------------
class SQLService:
    def __init__(self):
        self.db = connect_db()
        self.llm = load_llm()
        self.chain = build_chain(self.db, self.llm)

    def generate_sql(self, question):
        return self.chain.invoke({"question": question})

    def run_query(self, sql):
        validated = validate_sql(sql, self.db)
        return self.db.run(validated)