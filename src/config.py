import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is missing from your .env file!")

# Define global constants
CHAT_MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL_NAME = "gemini-embedding-2"

# Initialize Gemini
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# system_instruction = (
#     """
#     1. You are an assistant for question-answering tasks.
#     2. Use the retrieved context enclosed in the prompt to answer the question.
#     3. If you don't know the answer, say that you don't know.
#     4. Use three sentences maximum and keep the answer concise.
#     """
# )
# chat = gemini_client.chats.create(
#     model=CHAT_MODEL_NAME,
#     config=types.GenerateContentConfig(
#         system_instruction=system_instruction
#     )
# )
chat = gemini_client.chats.create(model=CHAT_MODEL_NAME)
