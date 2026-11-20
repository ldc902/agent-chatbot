import re
from .init_models import init_hf_model, init_groq_model, init_openai_model


def clean_output_text(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags = re.DOTALL).strip()