from typing import Optional, List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user_id: int
    full_name: str
    role_name: str
    roles: List[str]

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None
    refresh: Optional[bool] = False

class RefreshToken(BaseModel):
    refresh_token: str

class Message(BaseModel):
    message: str 