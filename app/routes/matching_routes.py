from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.matcher_service import MatcherService

router = APIRouter()
matcher_service = MatcherService()


class MatchRequest(BaseModel):
    jd_terms: List[str]
    resume_terms: List[str]
    synonym_mapping: Dict[str, Dict]


@router.post("/match")
def perform_matching(request: MatchRequest):
    try:
        result = matcher_service.match_terms(
            jd_terms=request.jd_terms,
            resume_terms=request.resume_terms,
            synonym_mapping=request.synonym_mapping
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
