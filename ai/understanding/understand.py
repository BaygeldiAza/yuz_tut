from .rules import rule_based_extract


def understand_query(query: str) -> dict:
    return rule_based_extract(query)
