from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi.concurrency import run_in_threadpool  # <-- import here

from app.services.normalization_service import normalize_tech_stack
from app.services.tokenizer_service import TokenizerService
from app.services.synonym_service import SynonymService
from app.services.matcher_service import MatcherService
from app.services.weighting_service import WeightingService
from app.services.scoring_service import ScoringService
from app.services.ats_score_service import ATSScoreService

router = APIRouter()

class TextRequest(BaseModel):
    text: str
    options: Dict = {}

# Load tokenizer once (not inside request)
tokenizer_service = TokenizerService()
synonym_service = SynonymService()
matcher_service = MatcherService()
weighting_service = WeightingService(frequency_based=False)
scoring_service = ScoringService()
ats_service = ATSScoreService()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

router = APIRouter()

# --- Request Model ---
class CompareRequest(BaseModel):
    jobDescription: str
    resume: str

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from app.services.normalization_service import normalize_tech_stack
from app.services.tokenizer_service import TokenizerService
from app.services.synonym_service import SynonymService
from app.services.matcher_service import MatcherService
from app.services.weighting_service import WeightingService
from app.services.scoring_service import ScoringService
from app.services.ats_score_service import ATSScoreService

router = APIRouter()

# --- Request Model ---
class CompareRequest(BaseModel):
    jobDescription: str
    resume: str

# Load services once
tokenizer_service = TokenizerService()
synonym_service = SynonymService()
matcher_service = MatcherService()
weighting_service = WeightingService(frequency_based=False)
scoring_service = ScoringService()
ats_service = ATSScoreService()


@router.post("/result")
async def result_endpoint(request: CompareRequest):
    try:
        jd_text = request.jobDescription
        resume_text = request.resume

        # print("\n[INPUT] Job Description:", jd_text[:200])  # print first 200 chars
        # print("[INPUT] Resume:", resume_text[:200])
        # Normalize both
        jd_normalized = normalize_tech_stack(jd_text.lower())
        resume_normalized = normalize_tech_stack(resume_text.lower())
        # print("\n[NORMALIZED] JD:", jd_normalized[:200])
        # print("[NORMALIZED] Resume:", resume_normalized[:200])

        # Run blocking spaCy tokenization in threadpool
        jd_result = await run_in_threadpool(tokenizer_service.tokenize, jd_normalized)
        resume_result = await run_in_threadpool(tokenizer_service.tokenize, resume_normalized)
        # print("\n[TOKENS] JD Tokens:", jd_result["tokens"][:20])
        # print("[TOKENS] Resume Tokens:", resume_result["tokens"][:20])

        # Map synonyms
        synonyms = await run_in_threadpool(
            synonym_service.map_synonyms,
            jd_result["tokens"],
            resume_result["tokens"]
        )
        # print("\n[SYNONYMS]", synonyms)

        # Calculate similarity
        similarity = await run_in_threadpool(
            matcher_service.jaccard_similarity,
            jd_result["tokens"],
            resume_result["tokens"]
        )

        # print("\n[SIMILARITY]", similarity)


        # Matches
        matches = await run_in_threadpool(
            matcher_service.match_terms,
            jd_result["tokens"],
            resume_result["tokens"],
            synonyms
        )
        # print("\n[MATCHES]", matches["matched_terms"])

        
        # Weight matches
        weight = await run_in_threadpool(weighting_service.calculate_score, matches)
        # print("\n[WEIGHT]", weight)

        # Weighted score
        weighted_score = await run_in_threadpool(scoring_service.weighted_score, weight)
        # print("\n[WEIGHTED SCORE]", weighted_score)

        # Hybrid score
        hybrid_score = await run_in_threadpool(scoring_service.hybrid_score, weight)
        # print("\n[HYBRID SCORE]", hybrid_score)

        # Percentage scores
        percentage_score = await run_in_threadpool(
            scoring_service.percentage_score,
            jd_result["tokens"],
            matches["matched_terms"]
            # resume_result["tokens"]
        )
        # print("\n[PERCENTAGE SCORE - Tokens]", percentage_score)


        # print("\n[PERCENTAGE SCORE - Phrases]", percentage_score_phrases)

        # Hard + soft matches
   
        # print("\n[HARD MATCHES]", hard_matches[:10])
        # print("[SOFT MATCHES]", soft_matches[:10])

        # Total terms
        total_terms = len(jd_result["tokens"]) + len(resume_result["tokens"])
        # print("\n[TOTAL TERMS]", total_terms)

        # --- Final Score Calculation ---
        # Normalize values into 0–100 scale
        sim_score = similarity * 100 if similarity <= 1 else similarity
        weighted = weighted_score * 100 if weighted_score <= 1 else weighted_score
        hybrid = hybrid_score * 100 if hybrid_score <= 1 else hybrid_score
        percent = min(percentage_score, 100)
        print(percent)
        # Final weighted average
        score_sum = round(
            (0.20 * weighted) +
            (0.10 * hybrid) +
            (0.70 * percent),
            2
        )

        return {
            "job_description": {
                "original_text": jd_text,
                "normalized_text": jd_normalized,
                "tokens": jd_result["tokens"],
                "phrases": jd_result["phrases"],
            },
            "resume": {
                "original_text": resume_text,
                "normalized_text": resume_normalized,
                "tokens": resume_result["tokens"],
                "phrases": resume_result["phrases"],
            },
            "synonyms": synonyms,
            "hard_matches": matches["hard_matches"],
            "soft_matches": matches["soft_matches"],
            "matched_terms": matches["matched_terms"],
            "missing_resume_terms": matches["missing_resume_terms"],
            "total_terms": total_terms,
            "matches": matches,
            "similarity": similarity,
            "weight": weight,
            "weighted_score": weighted_score,
            "hybrid_score": hybrid_score,
            "percentage_score": percentage_score,
            "score_sum": score_sum
            
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
