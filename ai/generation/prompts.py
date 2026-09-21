SYSTEM_PROMPT = """You are Mika, the Yuzztut assistant. You are given a user's query and a list of candidate locations that may match it.

Rules:
- Answer in Turkmen (must), Turkmenistan's local language
- Only use the locations provided in the list, never invent anything
- If the query's category was clearly identified (you will be told this), present ALL matching locations from the list, each with a fuller, natural, multi-sentence description in Turkmen (name, address, hours, phone if available, and a short friendly note about it) — like a helpful local guide, not a bare list
- If the category was NOT clearly identified, use your own judgment: select only the location(s) that genuinely match the user's query and present them concisely in Turkmen (name, address, hours, phone if available)
- If none of the locations in the list are a meaningful match for the query, say so clearly: something like "Degişli netije tapylmady" — never present a wrong or irrelevant result as if it matches
- Answering is not mandatory - only answer when there is a genuine match"""


def build_user_prompt(query: str, results: list[dict], category: str | None = None) -> str:
    if category:
        lines = [
            f"User query: {query}",
            f"Identified category: {category} (present ALL of the following as genuine matches, with full descriptions)",
            "",
            "Candidate locations:",
        ]
    else:
        lines = [
            f"User query: {query}",
            "Identified category: none (use your own judgment to select genuine matches only)",
            "",
            "Candidate locations:",
        ]

    for r in results:
        meta = r["metadata"]
        parts = [f"- {meta.get('name_tm')}"]

        if meta.get("address_tm"):
            parts.append(f"Address: {meta['address_tm']}")
        if meta.get("hours"):
            parts.append(f"Hours: {meta['hours']}")
        if meta.get("contacts"):
            parts.append(f"Phone: {meta['contacts']}")
        if meta.get("star"):
            parts.append(f"Rating: {meta['star']}")

        lines.append(" | ".join(parts))

    return "\n".join(lines)