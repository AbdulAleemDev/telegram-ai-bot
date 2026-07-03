from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY

llm = ChatGroq(
    model="openai/gpt-oss-120b",  # Recommended replacement for llama-3.3-70b
    api_key=GROQ_API_KEY,
    temperature=0,
    max_retries=2,
)