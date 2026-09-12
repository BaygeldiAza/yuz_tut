from retrieval.retrieve import retrieve
from ranking.rank import rank_results
from generation.generate import generate_response


def run_pipeline(query: str, user_lat: float = None, user_long: float = None) -> str:
    output = retrieve(query)

    if output["refuse"]:
        return output["message"]

    ranked = rank_results(
        output["results"],
        user_lat=user_lat,
        user_long=user_long,
        open_now_only=output["open_now_only"],
        sort_by=output["sort_by"],
    )

    return generate_response(ranked)