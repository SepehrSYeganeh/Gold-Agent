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
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Initialize Gemini
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
HISTORY_FILE = "chat_history.jsonl"
# CHAT_MODEL_NAME = "gemini-2.5-flash"
# CHAT_MODEL_NAME = "gemini-2.5-flash-lite"
CHAT_MODEL_NAME = "gemini-3.1-flash-lite"
SYSTEM_INSTRUCTION = """
You are an expert AI Gold Market Analyst. Your goal is to provide deep, realistic,
and accurate insights on the gold market based on the real-time data provided to you.

Rules:
1. Language Priority: ALWAYS reply in the exact language used by the user (English or Persian).
2. Base responses strictly on factual tool data. No hallucinations.
3. Be extremely concise. Avoid conversational filler. Use bullet points if saving space.
4. Don't give financial advice. Just provide the technical data analysis.
6. Buy/Sell Inquiries: If the user asks whether they should buy or sell gold, do NOT provide a direct recommendation.
   Instead, objectively explain the current market risks and potential benefits of both actions.
7. MANDATORY FORMATTING: ONLY if the user explicitly asks for a "forecast" or "analysis",
   you MUST split your response into these three exact sections (using the user's language):
   - Current State: The asset's current price and 7-day technical trend.
   - Primary Driver Analysis: How the macro news (Rates, DXY, Geopolitics) correlates with the trend.
   - Short-Term Horizon Evaluation: Bullish, Bearish, or Neutral conclusion.

   If the user is NOT asking for a forecast or analysis (e.g., just asking for a current price),
   do NOT use these sections. Provide only the direct information requested.
"""
tools = [
    fetch_recent_gold_price,
    fetch_recent_dxy,
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
