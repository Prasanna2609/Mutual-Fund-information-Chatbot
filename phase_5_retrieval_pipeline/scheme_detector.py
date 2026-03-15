"""
scheme_detector.py
Detects mutual fund scheme names in user queries by matching against known schemes.
"""

from typing import List, Optional

ALIAS_MAPPING = {
    "sbi large cap": "SBI Bluechip Fund Direct Growth",
    "hdfc large cap": "HDFC Top 100 Fund Direct Growth",
}



def _generate_name_variants(scheme_name: str) -> List[str]:
    """
    Generates progressively shorter name variants for flexible matching.
    E.g., "SBI Bluechip Fund Direct Growth" ->
        ["sbi bluechip fund", "sbi bluechip"]
    """
    name = scheme_name.lower()
    # Strip common suffixes progressively
    for suffix in [" direct growth", " direct plan growth", " growth", " direct"]:
        name = name.replace(suffix, "")
    name = name.strip()

    variants = [name]  # e.g., "sbi bluechip fund"

    # Also try without trailing "fund" / "scheme" for partial query matching
    for word in ["fund", "scheme"]:
        if name.endswith(f" {word}"):
            variants.append(name[: -(len(word) + 1)].strip())  # e.g., "sbi bluechip"

    return variants


def detect_scheme(query: str, known_schemes: List[str]) -> Optional[str]:
    """
    Detects if the user query mentions a known mutual fund scheme.

    Matches against known scheme names using case-insensitive substring matching.
    Returns the longest matching scheme name (most specific match) to avoid
    partial matches like "SBI" matching before "SBI Bluechip Fund".

    Args:
        query: The user's input query string.
        known_schemes: List of all scheme names from the vector store.

    Returns:
        The matched scheme name (as stored in metadata), or None if no match found.
    """
    query_lower = query.lower()

    # 1. Check for aliases first
    for alias, canonical_name in ALIAS_MAPPING.items():
        if alias in query_lower:
            # Optionally check if the canonical_name is actually in known_schemes
            # to be completely safe, but usually aliases map to known canonical names.
            if canonical_name in known_schemes:
                return canonical_name

    # 2. Existing flexible matching logic
    best_match = None
    best_match_length = 0

    for scheme in known_schemes:
        variants = _generate_name_variants(scheme)

        for variant in variants:
            if variant in query_lower:
                if len(variant) > best_match_length:
                    best_match = scheme  # Return the original scheme name
                    best_match_length = len(variant)

    return best_match

