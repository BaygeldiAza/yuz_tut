from ai.config import TOP_N
from .search import LocationSearch


def retrieve(searcher: LocationSearch, query: str, understanding: dict) -> list[dict]:
    category = understanding.get("category")
    return searcher.query(query_text=query, top_n=TOP_N, category=category)
