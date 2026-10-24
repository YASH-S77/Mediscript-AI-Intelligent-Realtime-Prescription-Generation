
import json
from difflib import SequenceMatcher
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "medicines.json"


def load_medicines():
    """Load medicine records from the local JSON catalogue."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        medicines = json.load(file)

    if not isinstance(medicines, list):
        raise ValueError("Medicine catalogue must contain a JSON list.")

    return medicines


def normalize_name(value):
    """Normalize a medicine name for case-insensitive matching."""
    return " ".join(str(value or "").casefold().strip().split())


def search_medicines(query, limit=10):
    """
    Search the catalogue by exact, partial, or approximate name.
    Returns matching catalogue records, not prescribing advice.
    """
    query = normalize_name(query)

    if not query:
        return []

    medicines = load_medicines()
    matches = []

    for medicine in medicines:
        searchable_fields = [
            medicine.get("name"),
            medicine.get("generic_name"),
            medicine.get("brand_name"),
        ]

        searchable_names = [
            normalize_name(value)
            for value in searchable_fields
            if value
        ]

        if not searchable_names:
            continue

        best_score = max(
            SequenceMatcher(None, query, name).ratio()
            for name in searchable_names
        )

        exact_match = any(query == name for name in searchable_names)
        partial_match = any(
            query in name or name in query
            for name in searchable_names
        )

        if exact_match:
            score = 1.0
        elif partial_match:
            score = max(best_score, 0.85)
        else:
            score = best_score

        # Keep exact, partial, and reasonably close spelling matches.
        if exact_match or partial_match or score >= 0.65:
            matches.append({
                **medicine,
                "match_score": round(score, 3),
            })

    matches.sort(
        key=lambda item: (
            item["match_score"],
            normalize_name(item.get("name")),
        ),
        reverse=True,
    )

    return matches[:max(1, min(limit, 25))]
