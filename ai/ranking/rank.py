import json
import math
from datetime import datetime

DAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def is_open_now(metadata, now=None):
    if metadata.get("round_the_clock"):
        return True
    if not metadata.get("is_open", True):
        return False

    now = now or datetime.now()
    day = DAY_NAMES[now.weekday()]
    hours_raw = metadata.get("hours")
    if not hours_raw:
        return True

    try:
        hours = json.loads(hours_raw) if isinstance(hours_raw, str) else hours_raw
    except (json.JSONDecodeError, TypeError):
        return True

    if not hours.get(f"{day}_is_open", True):
        return False

    start = hours.get(f"{day}_start")
    end = hours.get(f"{day}_end")
    if not start or not end:
        return True

    current = now.strftime("%H:%M")
    return start <= current <= end


def rank_results(results, user_lat=None, user_long=None, open_now_only=False, sort_by=None):
    ranked = []

    for r in results:
        metadata = r["metadata"]
        open_flag = is_open_now(metadata)

        if open_now_only and not open_flag:
            continue

        distance_km = None
        if user_lat is not None and user_long is not None and metadata.get("has_location"):
            distance_km = haversine_km(
                user_lat, user_long,
                metadata["latitude"], metadata["longitude"],
            )

        ranked.append({
            **r,
            "is_open_now": open_flag,
            "distance_km": distance_km,
        })

    has_dist = [r for r in ranked if r["distance_km"] is not None]
    no_dist = [r for r in ranked if r["distance_km"] is None]

    if sort_by == "sort_by_rating":
        has_dist.sort(key=lambda r: (-r["metadata"].get("star", 0), r["distance_km"]))
        no_dist.sort(key=lambda r: (-r["metadata"].get("star", 0), -r["score"]))
    elif sort_by == "sort_by_price_asc":
        # no price field in metadata yet - falls through to default below
        has_dist.sort(key=lambda r: (r["distance_km"], -r["score"]))
        no_dist.sort(key=lambda r: (-r["score"], -r["metadata"].get("star", 0)))
    else:
        # default: nearest first when we have distance, else relevance/rating
        has_dist.sort(key=lambda r: (r["distance_km"], -r["score"]))
        no_dist.sort(key=lambda r: (-r["score"], -r["metadata"].get("star", 0)))

    return has_dist + no_dist


if __name__ == "__main__":
    from retrieval.retrieve import retrieve

    output = retrieve("kebap iyer yaly yer maslahat ber ")

    if output["refuse"]:
        print(output["message"])
    else:
        ranked = rank_results(
            output["results"],
            user_lat=37.95,
            user_long=58.38,
            open_now_only=output["open_now_only"],
            sort_by=output["sort_by"],
        )
        for r in ranked:
            dist = f"{r['distance_km']:.2f}km" if r["distance_km"] is not None else "no-loc"
            print(f"{r['score']:.3f}  {dist:>10}  {r['metadata']['name_tm']}")