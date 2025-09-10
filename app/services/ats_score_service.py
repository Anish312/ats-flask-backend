from typing import List, Dict, Any


class ATSScoreService:
    def __init__(self):
        pass

    def calculate_score(
        self,
        hard_matches: List[Dict[str, Any]],
        soft_matches: List[Dict[str, Any]], 
        total_terms: int,
        all_jd_tokens: List[str] = None  # Add this parameter to get all JD tokens
    ) -> Dict[str, Any]:
        """
        Calculate ATS score and breakdown
        """

        # Raw weighted score
        raw_score = 0
        for match in hard_matches:
            raw_score += match["score"]
        for match in soft_matches:
            raw_score += match["score"] * 0.5  # softer weight

        # Normalize to percentage
        max_score = total_terms  # assume each term max=1
        percentage = (raw_score / max_score) * 100 if max_score > 0 else 0

        # --- Breakdown ---
        skills_terms = [m for m in hard_matches + soft_matches if "js" in m["jd_term"] or "sql" in m["jd_term"] or "api" in m["jd_term"]]
        education_terms = [m for m in hard_matches + soft_matches if "bachelor" in m["jd_term"].lower()]
        experience_terms = [m for m in hard_matches + soft_matches if "experience" in m["jd_term"].lower()]

        breakdown = {
            "skills": round((len(skills_terms) / (len(skills_terms) or 1)) * 100, 2),
            "education": round((len(education_terms) / (len(education_terms) or 1)) * 100, 2),
            "experience": round((len(experience_terms) / (len(experience_terms) or 1)) * 100, 2),
        }

        # --- Missing Keywords ---
        matched_jd_terms = {m["jd_term"] for m in hard_matches + soft_matches}
        all_jd_terms = {m["jd_term"] for m in hard_matches + soft_matches}
        missing = list(all_jd_terms - matched_jd_terms)

        return {
            "raw_score": f"{round(percentage, 2)}/100",
            "breakdown": breakdown,
            "missing_keywords": missing,
        }
