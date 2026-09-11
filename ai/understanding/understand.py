from ai.retrieval.search import LocationSearch
from ai.ranking.rank import rank_results
from ai.understanding.rules import rule_based_extract
from ai.understanding.llm_fallback import llm_fallback

REFUSE_MESSAGE = "Näme gözleýäniňizi has anyk aýdyp bilersiňizmi?"


def understand_query(query):
    result = rule_based_extract(query)

    if result["category"] is not None:
        result["source"] = "rule_based"
        result["refuse"] = False
        return result

    keywords = llm_fallback(query)

    if not keywords:
        return {
            "category": None,
            "sort_by": None,
            "open_now_only": False,
            "source": "llm_fallback",
            "refuse": True,
            "message": REFUSE_MESSAGE,
        }

    compressed_query = " ".join(keywords)
    result = rule_based_extract(compressed_query)

    if result["category"] is None:
        return {
            "category": None,
            "sort_by": None,
            "open_now_only": False,
            "source": "llm_fallback",
            "refuse": True,
            "message": REFUSE_MESSAGE,
        }

    result["source"] = "llm_fallback"
    result["refuse"] = False
    return result   