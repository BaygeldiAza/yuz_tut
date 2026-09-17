CATEGORY_SYNONYMS = {
    "kebap": "Restoran",
    "restoran": "Restoran",
    "market": "Supermarket",
    "dükan": "Dükan",
    # ... 121 category mapping goes here
}

SORT_KEYWORDS = {
    "arzan": "price_asc",
    "iň gowy": "rating_desc",
    "ýakyn": "distance_asc",
}

OPEN_NOW_KEYWORDS = ["gije işleýän", "häzir açyk", "24 sagat"]


def rule_based_extract(query: str) -> dict:
    q = query.lower()

    category = None
    for keyword, cat in CATEGORY_SYNONYMS.items():
        if keyword in q:
            category = cat
            break

    sort_by = None
    for keyword, sort_value in SORT_KEYWORDS.items():
        if keyword in q:
            sort_by = sort_value
            break

    open_now_only = any(keyword in q for keyword in OPEN_NOW_KEYWORDS)

    return {
        "category": category,
        "sort_by": sort_by,
        "open_now_only": open_now_only,
    }
