from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.services.scoring_service import ScoringService

router = APIRouter()
scoring_service = ScoringService()


class ScoreRequest(BaseModel):
    jd_terms: List[str]
    matched_terms: List[str]
    weighted_result: Dict


@router.post("/score")
def calculate_score(request: ScoreRequest):
    try:
        percentage = scoring_service.percentage_score(
            jd_terms=request.jd_terms,
            matched_terms=request.matched_terms
        )
        weighted = scoring_service.weighted_score(request.weighted_result)
        hybrid = scoring_service.hybrid_score(request.weighted_result)

        return {
            "status": "success",
            "data": {
                "percentage_score": percentage,
                "weighted_score": weighted,
                "hybrid_score": hybrid
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
