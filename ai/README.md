# yuzztut — `ai/` Folder Structure & Pipeline Documentation

**Owner:** Arslan (AI Engineering Intern)
**Scope:** embeddings, retrieval, ranking, generation, prompt engineering
**Constraint:** production server is network-isolated, CPU-only, inside Turkmenistan — fully self-hosted, quantized models only

---

## Repo layout

```
repo-root/
├── streamlit_app.py          # demo UI, run via `streamlit run streamlit_app.py`
├── data/
│   ├── merge_locations.py    # merges 3,693 raw JSON files → dedupes by id
│   └── build_embedding_text.py  # builds locations_embedding_ready.jsonl
├── data/locations_embedding_ready.jsonl   # 3,347 unique locations, final dataset
└── ai/
    ├── __init__.py
    ├── config.py
    ├── requirements.txt
    ├── pipeline.py            # (planned) single run_pipeline() entry point
    ├── indexing/
    │   ├── embed.py           # builds Chroma index from JSONL
    │   └── chroma_db/         # persistent vector store (collection: "locations")
    ├── retrieval/
    │   └── search.py          # LocationSearch class — embed query, Chroma query
    ├── understanding/
    │   ├── __init__.py
    │   ├── rules.py           # rule_based_extract() — regex/keyword category extraction
    │   ├── llm_fallback.py    # Gemma 4 fallback when rules find no category
    │   └── understand.py      # orchestrates rules → llm_fallback → refuse
    ├── ranking/
    │   └── (filter/sort logic: open_now, distance, rating — has_location flag)
    └── generation/
        └── (formats retrieved DB results into Turkmen text via Gemma 4)
```

---

## Data

- **3,347** unique locations (deduped from 3,693 raw JSON files, 225 duplicates removed)
- Two source shapes merged into one: "detail" (full fields) + "list/section" (short fields) → all records now have full detail-format fields
- **~838 locations (~25%)** have null lat/long → `has_location: false`, ranked by relevance/rating only (no distance sort)
- `embedding_text` format: `name_tm | categories | address_tm | seo_keywords | body_tm[:300]`
- Metadata carried per record: `id, name_tm, address_tm, categories, lat/long, has_location, star, review_count, is_open, round_the_clock, hours, contacts, slug`

---

## Pipeline stages

### 1. Indexing (offline, one-time)
`ai/indexing/embed.py`
- Loads `locations_embedding_ready.jsonl`
- Embeds with `intfloat/multilingual-e5-base` (batch size 64, `"passage: "` prefix)
- Writes to Chroma (`ai/indexing/chroma_db`), collection `locations`, `hnsw:space: cosine`
- **Status: done** — `collection.count() == 3347` confirmed

### 2. Retrieval (runtime)
`ai/retrieval/search.py` — `LocationSearch` class
- Wraps SentenceTransformer + Chroma query
- Embeds query with `"query: "` prefix
- Returns top-N with score / embedding_text / metadata
- **Status: done, tested** on real Turkmen queries

### 3. Understanding (runtime, query intent extraction)
`ai/understanding/` — `understand.py`, `rules.py`, `llm_fallback.py`
Settled flow:
1. `rule_based_extract()` runs first (fast, deterministic)
2. If no category found → `llm_fallback()` (Gemma 4, quantized) — same output shape `{category, sort_by, open_now_only}`
3. If LLM also returns `category=None` → refuse, ask user to rephrase (never embed/retrieve on null category)
4. If category found → embed the **raw query** (not the category) and retrieve top-N
5. Soft-check: if top-N metadata categories match extracted category, accept; else re-search using the category string as the query

**Interim state (LLM fallback disabled during dev, 30–65s latency issue):**
rule-based → if no category, embed raw query → check top-1 score against `EMBED_CONFIDENCE_THRESHOLD = 0.75` → if confident, use that record's category; else refuse.

**Known bug:** `rule_based_extract()` is brittle on Latin-keyboard spelling variants of Turkmen characters (e.g. "gurlushyk" vs "gurluşyk"), causing cross-category phonetic false-positives (near-identical scores, ~0.785–0.798) unless category filtering happens **inside** the Chroma query (`where={"categories": category}`) rather than post-retrieval.

### 4. Ranking (runtime)
Plain code logic (no AI): open/closed now, distance (only for `has_location: true` records), rating.

### 5. Generation (runtime)
Gemma 4 formats real DB top-N results into Turkmen text. **Never generates from its own knowledge** — strictly a formatting/extraction role, not free-form chat.

---

## Models & tools

| Role | Model / Tool |
|---|---|
| Embeddings | `intfloat/multilingual-e5-base` (via `sentence-transformers`) |
| Vector DB | ChromaDB, persistent local, collection `locations`, cosine space |
| LLM (understanding fallback + generation) | `hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf` (Q4_0, 4.63B params) via Ollama |
| Demo UI | Streamlit (`streamlit_app.py`) |
| Model mirror (China dev env) | `HF_ENDPOINT=https://hf-mirror.com` |

**Rejected models:** `gemma2:2b` (fast but unusable Turkmen output), `batiai/gemma4-e2b:q4` (empty responses), Qwen2.5 and NLLB (fully removed from architecture).

---

## Known issues / active work

1. LLM fallback latency (30–65s) — disabled during dev. Fix strategies: shortlist categories in system prompt (not all ~55), lower `num_predict` to ~20–30, `keep_alive=-1` in prod, `format="json"` constrained decoding. **Core lever: KV cache reuse — system prompt must be byte-identical across calls.**
2. Category filter must be validated inside Chroma `where=` clause end-to-end (not post-retrieval).
3. Synonym dictionary coverage for spelling variants / agglutination needs expansion.
4. Possible hybrid embedding+keyword scoring or re-ranking if filtering alone insufficient.
5. Cascade design under consideration: rule-based → embedding similarity → if score < ~0.60–0.70, LLM rewrites query and re-searches (retry cap to prevent loops).
6. Possible embedding model switch: `multilingual-e5-base` → `BAAI/bge-m3`.

---

## Backend integration (deferred, current lean)

Direct Python import: single `run_pipeline()` function in `ai/pipeline.py`, called directly by backend (not HTTP API) — simplest for single-machine, small-team setup. Stable input/output contract keeps AI internals free to change without breaking backend.

---

## Core principles (non-negotiable)

- System never hallucinates or invents locations — only real DB entries + GPS
- LLM's only jobs: (a) query understanding/category extraction, (b) formatting real DB results into Turkmen
- Null-category queries never reach retrieval — refuse and ask to rephrase
- Casual/chitchat intercepted by lightweight rule-based check before any LLM call
- Build end-to-end first, polish layers after — avoid over-optimizing components in isolation