from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from app.services.grammar_service import GrammarService

router = APIRouter()

class GrammarRequest(BaseModel):
    text: str

# Load once
grammar_service = GrammarService()

@router.post("/grammar-check")
async def grammar_check(request: GrammarRequest):
    try:
        result = await run_in_threadpool(grammar_service.check_text, request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
