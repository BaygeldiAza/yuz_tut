import ollama
from understanding.llm_fallback import MODEL  # bir model ulanylýar
from generation.prompts import GENERATION_SYSTEM_PROMPT


def format_results_for_prompt(ranked_results: list[dict]) -> str:
    lines = []
    for r in ranked_results[:5]:
        meta = r["metadata"]
        dist = f"{r['distance_km']:.1f}km" if r.get("distance_km") is not None else "aralyk belli däl"
        status = "açyk" if r.get("is_open_now") else "ýapyk"
        lines.append(f"- {meta.get('name_tm')} | {dist} | {status} | {meta.get('address_tm')}")
    return "\n".join(lines)


def generate_response(ranked_results: list[dict]) -> str:
    if not ranked_results:
        return "Gynansak-da, gözlegiňize gabat gelýän ýer tapylmady."

    context = format_results_for_prompt(ranked_results)

    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
            {"role": "user", "content": context}
        ],
        options={"temperature": 0}
    )

    return response["message"]["content"]