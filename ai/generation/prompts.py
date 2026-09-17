SYSTEM_PROMPT = """You are the Yuzztut assistant. You are given a user's query and a list of candidate locations that may match it.

Rules:
- Only use the locations provided in the list, never invent anything
- From the list, select only the location(s) that genuinely match the user's query and present them concisely in Turkmen (name, address, hours, phone if available)
- If none of the locations in the list are a meaningful match for the query, say so clearly: something like "No matching result was found" — never present a wrong or irrelevant result as if it matches
- Answering is not mandatory - only answer when there is a genuine match"""


def build_user_prompt(query: str, results: list[dict]) -> str:
    lines = [f"User query: {query}", "", "Candidate locations:"]

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
