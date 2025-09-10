from pydantic import BaseModel

class TokenRequest(BaseModel):
    text: str
