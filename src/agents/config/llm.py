from langchain_google_genai import ChatGoogleGenerativeAI
from .settings import GOOGLE_API_KEY

def get_llm_gemini(model="gemini-2.5-flash", temperature=0):
    return ChatGoogleGenerativeAI(
        model = model,
        temperature = temperature,
        google_api_key = GOOGLE_API_KEY
    )