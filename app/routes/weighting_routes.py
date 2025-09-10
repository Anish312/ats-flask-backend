from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.services.weighting_service import WeightingService

router = APIRouter()
weighting_service = WeightingService(frequency_based=False)


class WeightRequest(BaseModel):
    matches: Dict[str, List[Dict]]


@router.post("/weight")
def calculate_weighted_score(request: WeightRequest):
    try:
        result = weighting_service.calculate_score(request.matches)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
