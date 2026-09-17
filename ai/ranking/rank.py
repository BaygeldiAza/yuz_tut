from math import radians, sin, cos, sqrt, atan2


def haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


def rank_results(results: list[dict], understanding: dict, user_lat=None, user_lon=None) -> list[dict]:
    if understanding.get("open_now_only"):
        results = [
            r for r in results
            if r["metadata"].get("is_open") or r["metadata"].get("round_the_clock")
        ]

    sort_by = understanding.get("sort_by")

    if sort_by == "distance_asc" and user_lat is not None and user_lon is not None:
        def distance_key(r):
            meta = r["metadata"]
            if not meta.get("has_location"):
                return float("inf")
            return haversine(user_lat, user_lon, meta["lat"], meta["long"])

        results.sort(key=distance_key)

    elif sort_by == "rating_desc":
        results.sort(key=lambda r: (r["metadata"].get("star", 0), r["metadata"].get("review_count", 0)), reverse=True)

    elif sort_by == "price_asc":
        results.sort(key=lambda r: r["metadata"].get("price_level", 0))

    return results
