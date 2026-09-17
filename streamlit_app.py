import streamlit as st
import ollama
from ai.retrieval.search import LocationSearch

TOP_N = 8
LLM_MODEL = "hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf"

@st.cache_resource
def get_searcher():
    return LocationSearch()

def generate_answer(query: str, results: list[dict]) -> str:
    if not results:
        return "Gynansak-da, degişli ýer tapylmady. Soragyňyzy başgaça beriň."

    context_lines = []
    for r in results:
        meta = r["metadata"]
        context_lines.append(
            f"- {meta.get('name_tm', '')} | {meta.get('categories', '')} | {meta.get('address_tm', '')}"
        )
    context = "\n".join(context_lines)

    system_prompt = (
        "Sen Turkmenistandaky ýerleri maslahat berýän kömekçisiň. "
        "Saňa ulanyjynyň sorag we mümkin bolan ýerleriň sanawy berilýär. "
        "Diňe berlen sanawdaky ýerleri ulanyp, gysga, düşnükli türkmen dilinde maslahat ber. "
        "Sanawda ýok zady oýlap tapma. Diňe berlen maglumaty gaýtadan gürrüň ber."
    )
    user_prompt = f"Sorag: {query}\n\nTapylan ýerler:\n{context}\n\nGysga maslahat ber:"

    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"num_predict": 300, "temperature": 0},
            think=False,
        )
    except Exception as e:
        st.error(f"Ollama error: {e}")
        return ""

    content = response["message"]["content"]
    if not content:
        content = response["message"].get("thinking", "")
    return content

st.title("yuzztut demo")

query = st.text_input("Sorag giriziň:")

if query:
    searcher = get_searcher()
    results = searcher.search(query, top_n=TOP_N)

    st.subheader("Retrieval netijeleri")
    for r in results:
        meta = r["metadata"]
        st.write(f"**{meta.get('name_tm', '')}** ({meta.get('categories', '')}) — score: {r.get('score', 0):.3f}")
        st.caption(meta.get("address_tm", ""))

    st.subheader("LLM jogaby")
    with st.spinner("Jogap taýýarlanýar..."):
        answer = generate_answer(query, results)
    st.write(answer)