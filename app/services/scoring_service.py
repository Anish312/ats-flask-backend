from typing import Dict, List


class ScoringService:
    def __init__(self):
        pass

    def percentage_score(self, jd_terms: List[str], matched_terms: List[str]) -> float:
        """Simple coverage-based score (unique matches only)."""
        if not jd_terms:
            return 0.0

        jd_set = set(map(str.lower, jd_terms))
        matched_set = set(map(str.lower, matched_terms))

        coverage = len(jd_set & matched_set) / len(jd_set)
        return round(coverage * 100, 2)

    def weighted_score(self, weighted_result: Dict) -> float:
        """Calculate score from weighting step output."""
        total_score = weighted_result.get("total_score", 0)
        max_score = weighted_result.get("max_score", 0)

        if max_score <= 0:
            return 0.0
        return round((total_score / max_score) * 100, 2)

    def hybrid_score(self, weighted_result: Dict, semantic_boost: float = 5.0) -> float:
        """
        Hybrid = weighted score + semantic bonus for high-similarity soft matches.
        """
        base_score = self.weighted_score(weighted_result)
        detailed_matches = weighted_result.get("detailed_matches", [])

        # Count strong soft matches
        strong_soft_matches = sum(
            1 for match in detailed_matches
            if match.get("match_type") == "soft_matches"
            and match.get("similarity_score", 0) >= 0.5
        )

        # Apply bonus
        semantic_bonus = strong_soft_matches * semantic_boost
        return min(base_score + semantic_bonus, 100.0)
