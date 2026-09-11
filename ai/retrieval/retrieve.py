from understanding.understand import understand_query
from retrieval.search import LocationSearch

searcher = LocationSearch()
TOP_N = 7


def retrieve(query: str) -> dict:
    understanding = understand_query(query)

    if understanding["refuse"]:
        return {
            "refuse": True,
            "message": understanding["message"],
            "results": [],
        }

    category = understanding["category"]
    results = searcher.search(query, top_n=TOP_N)

    category_match = any(
        r["metadata"].get("categories") == category for r in results
    )

    if not category_match:
        results = searcher.search(category, top_n=TOP_N)

    return {
        "refuse": False,
        "category": category,
        "sort_by": understanding["sort_by"],
        "open_now_only": understanding["open_now_only"],
        "results": results,
    }


if __name__ == "__main__":
    test_query = "iýmek üçin ýer gerek"
    output = retrieve(test_query)
    print(output)