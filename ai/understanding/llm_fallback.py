import ollama
from rules import rule_based_extract

MODEL_NAME = "hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf"

#SYSTEM_PROMPT = 


def llm_compress(query: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        keep_alive="30m"
    )
    return response["message"]["content"].strip()


def llm_fallback(query: str) -> dict:
    short_query = llm_compress(query)
    result = rule_based_extract(short_query)
    if result["category"] is None:
        return {"category": None, "sort_by": None, "open_now_only": False}
    return result