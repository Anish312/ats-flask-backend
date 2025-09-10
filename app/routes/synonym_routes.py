from fastapi import APIRouter
from pydantic import BaseModel
from app.services.synonym_service import SynonymService

router = APIRouter()
synonym_service = SynonymService()

class SynonymRequest(BaseModel):
    jd_tokens: list[str]
    resume_tokens: list[str]

@router.post("/map_synonyms")
def map_synonyms(req: SynonymRequest):
    result = synonym_service.map_synonyms(req.jd_tokens, req.resume_tokens)
    return {"synonym_mapping": result}
