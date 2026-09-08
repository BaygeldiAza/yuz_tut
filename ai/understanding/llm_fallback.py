import ollama
import json

SYSTEM_PROMPT = """Türkmen dilindäki ulanyjy sözlemini oka.
4-5 sany anyk, konkret açar söz/söz düzümi ýaz (ýer, zat, hereket ýa-da zerurlyk atlary).
Abstrakt ýa-da düşündiriş sözlerini ulanma.
Diňe JSON gaýtar: {"keywords": ["...", "...", "..."]}
Başga hiç zat ýazma."""

MODEL = "hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf"

def llm_fallback(query: str) -> list[str]:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        format="json",
        options={
            "temperature": 0,
            "num_predict": 30,
            "keep_alive": "30m"
        }
    )

    try:
        data = json.loads(response["message"]["content"])
        keywords = data.get("keywords", [])
        if isinstance(keywords, list):
            return [str(k).strip() for k in keywords if str(k).strip()]
        return []
    except (json.JSONDecodeError, KeyError, TypeError):
        return []