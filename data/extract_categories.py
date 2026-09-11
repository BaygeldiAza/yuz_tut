import json
from collections import Counter

INPUT_PATH = "locations_embedding_ready.jsonl"

def load_categories(path):
    counter = Counter()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            metadata = record.get("metadata") or {}
            cats = metadata.get("categories")
            if not cats:
                continue
            if isinstance(cats, str):
                cats = [c.strip() for c in cats.split(",")]
            for c in cats:
                c = c.strip()
                if c:
                    counter[c] += 1
    return counter

def main():
    counter = load_categories(INPUT_PATH)
    print(f"Unique categories: {len(counter)}\n")
    for cat, count in counter.most_common():
        print(f"{count:5d}  {cat}")

    with open("categories.json", "w", encoding="utf-8") as f:
        json.dump(
            {"total": len(counter), "categories": dict(counter.most_common())},
            f,
            ensure_ascii=False,
            indent=2,
        )
    print("\nWritten to categories.json")

if __name__ == "__main__":
    main()