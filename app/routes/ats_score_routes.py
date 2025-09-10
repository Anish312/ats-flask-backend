from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.ats_score_service import ATSScoreService

router = APIRouter()
ats_service = ATSScoreService()


class MatchResult(BaseModel):
    jd_term: str
    resume_term: str
    score: float


class ATSRequest(BaseModel):
    hard_matches: List[MatchResult]
    soft_matches: List[MatchResult]
    total_terms: int


@router.post("/ats-score")
def calculate_ats_score(request: ATSRequest):
    try:
        result = ats_service.calculate_score(
            hard_matches=[m.dict() for m in request.hard_matches],
            soft_matches=[m.dict() for m in request.soft_matches],
            total_terms=request.total_terms,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
