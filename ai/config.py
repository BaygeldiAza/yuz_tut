import os

HF_ENDPOINT = "https://hf-mirror.com"
HF_HUB_OFFLINE = "1"

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"
QUERY_PREFIX = "query: "
PASSAGE_PREFIX = "passage: "

CHROMA_PATH = "ai/indexing/chroma_db"
CHROMA_COLLECTION = "locations"

OLLAMA_MODEL = "hf.co/google/gemma-4-E2B-it-qat-q4_0-gguf"
OLLAMA_KEEP_ALIVE = -1
GENERATION_TEMPERATURE = 0

TOP_N = 5

os.environ.setdefault("HF_ENDPOINT", HF_ENDPOINT)
os.environ.setdefault("HF_HUB_OFFLINE", HF_HUB_OFFLINE)
