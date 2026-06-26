import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .fetcher import *


# Load environment variables
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is missing from your .env file!")


# Initialize Gemini
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
CHAT_MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL_NAME = "gemini-embedding-2"
SYSTEM_INSTRUCTION = """
You are an expert AI Gold Market Analyst. Your goal is to provide deep, realistic, 
and accurate insights on the gold market based on the real-time data provided to you.

Rules:
1. Base responses strictly on factual tool data. No hallucinations.
2. Be extremely concise. Avoid conversational filler or long intros. Use bullet points if saving space.
3. Do not give financial advice. Just provide the data analysis.
4. Reply in the user's language (English or Persian).
"""
TOOLS = [
    fetch_live_gold_price,
    fetch_dxy_proxy
]
agent_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.1,
    tools=TOOLS
)
chat = gemini_client.chats.create(
    model=CHAT_MODEL_NAME,
    config=agent_config
)
