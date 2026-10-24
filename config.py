import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gemini-3.5-flash-lite")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
LLM_API_KEY = os.environ["LLM_API_KEY"]

NIGHTFURY_EMOJI = os.environ["NIGHTFURY_EMOJI"]
AI_CHAT_BUBBLE_EMOJI = os.environ["AI_CHAT_BUBBLE_EMOJI"]
