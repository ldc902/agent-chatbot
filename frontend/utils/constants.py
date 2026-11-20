import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

PROVIDERS = {
    "OpenAI": ["gpt-4o-mini"],
    "Groq": ["openai/gpt-oss-120b"],
    "HF-Inference": ["Qwen/QwQ-32B"]
}