from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.tokenizer_service import TokenizerService

router = APIRouter()
tokenizer_service = TokenizerService()

class TokenRequest(BaseModel):
    text: str

@router.post("/tokenize")
def tokenize_text(request: TokenRequest):
    try:
        result = tokenizer_service.tokenize(request.text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
