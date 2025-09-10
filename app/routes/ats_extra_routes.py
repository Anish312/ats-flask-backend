from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ats_extra_service import ATSExtraService

router = APIRouter()
extra_service = ATSExtraService()

class JDResumeRequest(BaseModel):
    jd: dict
    resume: dict

@router.post("/extra-factors")
def check_extra_factors(request: JDResumeRequest):
    result = extra_service.evaluate_extras(request.jd, request.resume)
    return {"extra_factors": result}
