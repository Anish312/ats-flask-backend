from typing import Dict, List


class WeightingService:
    def __init__(self, frequency_based: bool = False):
        self.frequency_based = frequency_based

        # Define weight dictionary (can be expanded or loaded from DB)
        self.weights = {
            "high": ["react", "react.js", "node", "node.js", "mysql", "sql", "aws", "pmp", "bachelor’s degree"],
            "medium": ["api design", "project management", "cloud computing", "leadership", "data analysis"],
            "low": ["team player", "responsible", "communication", "self-motivated"]
        }

        # Normalize dictionary terms to lowercase for consistent matching
        self.weights = {k: [t.lower() for t in v] for k, v in self.weights.items()}

    def get_weight(self, term: str) -> int:
        """Return the weight of a term based on importance level."""
        term = term.lower()
        if term in self.weights["high"]:
            return 3
        elif term in self.weights["medium"]:
            return 2
        elif term in self.weights["low"]:
            return 1
        return 1  # Default if not found

    def calculate_score(self, matches: Dict[str, List[Dict]]) -> Dict:
        """Calculate weighted score based on matches between JD and resume."""
        total_score = 0.0
        max_score = 0.0
        scored_matches = []

        for match_type, match_list in matches.items():
            if match_type not in ["hard_matches", "soft_matches"]:
                continue
 


            for match in match_list:
                jd_term = match["jd_term"].lower()
                resume_term = match["resume_term"].lower()
                score = float(match.get("score", 0))
                if match_type == "soft_matches" and score < 0.3:
                    continue  # ignore very weak matches

                # Assign weight
                weight = self.get_weight(jd_term)

                # Frequency adjustment
                match_points = weight
                if self.frequency_based:
                    freq = match.get("frequency", 1)  # Expect frequency key in match
                    match_points *= max(1, freq)

                # Weighted score
                weighted_score = round(score * match_points, 3)

                scored_matches.append({
                    "jd_term": jd_term,
                    "resume_term": resume_term,
                    "match_type": match_type,
                    "similarity_score": score,
                    "weight": weight,
                    "weighted_score": weighted_score
                })

                total_score += weighted_score
                max_score += weight * (match_points / weight)  # handles frequency case properly

        final_percentage = round((total_score / max_score) * 100, 2) if max_score > 0 else 0

        return {
            "total_score": round(total_score, 3),
            "max_score": round(max_score, 3),
            "match_percentage": final_percentage,
            "detailed_matches": scored_matches
        }
