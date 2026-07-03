from langchain_groq import ChatGroq

from app.core.config import GROQ_API_KEY


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0,
    max_retries=2,
)