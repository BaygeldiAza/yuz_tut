import ollama

from ai.config import OLLAMA_MODEL, OLLAMA_KEEP_ALIVE, GENERATION_TEMPERATURE
from .prompts import SYSTEM_PROMPT, build_user_prompt


def generate_response(query: str, results: list[dict]) -> str:
    user_prompt = build_user_prompt(query, results)

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        keep_alive=OLLAMA_KEEP_ALIVE,
        options={"temperature": GENERATION_TEMPERATURE},
        think=False,
    )

    return response["message"]["content"]
