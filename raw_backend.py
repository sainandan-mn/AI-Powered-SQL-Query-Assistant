import os
from urllib.parse import quote_plus

from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def connect_db():
    host = "localhost"
    port = "3306"
    username = "root"
    password = quote_plus(os.getenv("MYSQL_PASSWORD"))
    database = "text_to_sql"

    uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(uri)


def load_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-flash-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )


class RawSQLService:
    def __init__(self):
        self.db = connect_db()
        self.llm = load_llm()

        self.prompt = ChatPromptTemplate.from_template("""
Write a SQL query for the user's question using this schema:

{schema}

Question:
{question}

SQL:
""")

        self.chain = (
            RunnablePassthrough.assign(schema=lambda _: self.db.get_table_info())
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):
        sql = self.chain.invoke({"question": question})
        return self.db.run(sql)