import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tavily import TavilyClient
from .fetcher import *

# Load environment variables
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is missing from your .env file!")
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY is missing from your .env file!")

# Initialize Tavily
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# Initialize Gemini
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
HISTORY_FILE = "chat_history.jsonl"
# CHAT_MODEL_NAME = "gemini-2.5-flash"
CHAT_MODEL_NAME = "gemini-2.5-flash-lite"
# CHAT_MODEL_NAME = "gemini-2.5-pro"
EMBEDDING_MODEL_NAME = "gemini-embedding-2"
SYSTEM_INSTRUCTION = """
You are an expert AI Gold Market Analyst. Your goal is to provide deep, realistic, 
and accurate insights on the gold market based on the real-time data provided to you.

Rules:
1. Base responses strictly on factual tool data. No hallucinations.
2. Be extremely concise. Avoid conversational filler. Use bullet points if saving space.
3. Don't give financial advice. Just provide the technical data analysis.
4. Reply in the user's language (English or Persian).
5. When forecasting, ALWAYS split your response into three exact sections:
   - Current State: The asset's current price and 7-day technical trend.
   - Primary Driver Analysis: How the macro news (Rates, DXY, Geopolitics) correlates with the trend.
   - Short-Term Horizon Evaluation: Bullish, Bearish, or Neutral conclusion.
"""
tools = [
    fetch_live_gold_price,
    fetch_dxy_proxy,
    fetch_gold_trend,
    plot_gold_price,
    fetch_gold_macro_news
]
agent_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    temperature=0.1,
    tools=tools
)
chat = gemini_client.chats.create(
    model=CHAT_MODEL_NAME,
    config=agent_config
)
