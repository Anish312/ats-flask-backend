from typing import Dict, Any

class ATSExtraService:
    def __init__(self):
        pass

    def evaluate_extras(self, jd_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare additional non-skill factors like experience, education, and titles.
        jd_data and resume_data are expected to have structured info.
        Example:
            jd_data = {"experience": 5, "education": "bachelor", "title": "Full Stack Developer"}
            resume_data = {"experience": 6, "education": "master", "title": "Software Engineer"}
        """

        results = {
            "experience_match": False,
            "education_match": False,
            "title_match": False,
            "formatting_score": 1.0  # default full credit
        }

        # --- Experience Check ---
        if "experience" in jd_data and "experience" in resume_data:
            results["experience_match"] = resume_data["experience"] >= jd_data["experience"]

        # --- Education Check ---
        if "education" in jd_data and "education" in resume_data:
            jd_edu = jd_data["education"].lower()
            resume_edu = resume_data["education"].lower()
            edu_levels = ["highschool", "diploma", "bachelor", "master", "phd"]
            if jd_edu in edu_levels and resume_edu in edu_levels:
                results["education_match"] = edu_levels.index(resume_edu) >= edu_levels.index(jd_edu)

        # --- Job Title Check (basic string containment) ---
        if "title" in jd_data and "title" in resume_data:
            results["title_match"] = jd_data["title"].lower() in resume_data["title"].lower()

        # --- Formatting/Parse Quality (dummy rule: if resume missing sections, reduce) ---
        if not resume_data.get("skills") or not resume_data.get("experience"):
            results["formatting_score"] = 0.7  # penalize bad parsing

        return results
