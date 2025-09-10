from typing import Dict, List
from difflib import SequenceMatcher


class MatcherService:
    def __init__(self, threshold: float = 0.7):
        # Minimum score to consider as a "soft match"
        self.threshold = threshold

    def similarity_score(self, text1: str, text2: str) -> float:
        """Return similarity ratio between two strings."""

        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    def jaccard_similarity(self, jd_tokens: List[str], resume_tokens: List[str]) -> float:
        set1, set2 = set(jd_tokens), set(resume_tokens)
        if not set1 or not set2:
            return 0.0
        return len(set1 & set2) / len(set1 | set2)

    def match_terms(
        self, jd_terms: List[str], resume_terms: List[str], synonym_mapping: Dict
    ) -> Dict[str, List[Dict]]:
        """
        Match JD terms with Resume terms using hard (exact/synonym) and soft (fuzzy) matches.
        """

        hard_matches = []
        soft_matches = []
        matched_terms = set()  # collect matched resume terms

        # --- Prepare synonym lookup ---
        synonym_lookup = {
            k.lower(): v["best_match"].lower() for k, v in synonym_mapping.items()
        }

        # --- Hard Matches ---
        matched_resume_terms = set()
        for jd in jd_terms:
            jd_lower = jd.lower()
            for resume in resume_terms:
                resume_lower = resume.lower()

                # Exact match
                if jd_lower == resume_lower:
                    hard_matches.append({"jd_term": jd, "resume_term": resume, "score": 1.0})
                    matched_resume_terms.add(resume_lower)
                    matched_terms.add(resume)  # store original resume term
                    continue

                # Synonym match
                if jd_lower in synonym_lookup and synonym_lookup[jd_lower] == resume_lower:
                    score = synonym_mapping.get(jd, {}).get("score", 0.9)  # default 0.9
                    hard_matches.append({"jd_term": jd, "resume_term": resume, "score": score})
                    matched_resume_terms.add(resume_lower)
                    matched_terms.add(resume)

        # --- Soft Matches (fuzzy) ---
        for jd in jd_terms:
            jd_lower = jd.lower()
            for resume in resume_terms:
                resume_lower = resume.lower()
                if resume_lower in matched_resume_terms:
                    continue  # already counted as hard match
                score = self.similarity_score(jd, resume)
                if score >= self.threshold:
                    soft_matches.append({
                        "jd_term": jd,
                        "resume_term": resume,
                        "score": round(score, 3)
                    })
                    matched_terms.add(resume)

        missing_resume_terms = list({
            jd.lower() for jd in jd_terms if jd.lower() not in [r.lower() for r in resume_terms]
        })


        # # Remove duplicates
        # hard_matches = [dict(t) for t in {tuple(d.items()) for d in hard_matches}]
        # soft_matches = [dict(t) for t in {tuple(d.items()) for d in soft_matches}]

        return {
            "hard_matches": hard_matches,
            "soft_matches": soft_matches,
            "matched_terms": list(matched_terms)  ,
            "missing_resume_terms": missing_resume_terms
        }
