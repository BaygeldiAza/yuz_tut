from ai.understanding.understand import understand_query
from ai.retrieval.search import LocationSearch
from ai.retrieval.retrieve import retrieve
from ai.ranking.rank import rank_results
from ai.generation.generate import generate_response

_searcher: LocationSearch | None = None


def get_searcher() -> LocationSearch:
    global _searcher
    if _searcher is None:
        _searcher = LocationSearch()
    return _searcher


def run_pipeline(query: str, user_lat: float | None = None, user_lon: float | None = None) -> dict:
    understanding = understand_query(query)

    searcher = get_searcher()
    results = retrieve(searcher, query, understanding)
    results = rank_results(results, understanding, user_lat, user_lon)

    answer = generate_response(query, results)

    return {
        "answer": answer,
        "understanding": understanding,
        "results": results,
    }
