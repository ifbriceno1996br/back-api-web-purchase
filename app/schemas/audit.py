from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.user import User

class AuditRequestBase(BaseModel):
    action: str
    previous_status: Optional[str] = None
    new_status: Optional[str] = None
    comment: Optional[str] = None

class AuditRequestInDBBase(AuditRequestBase):
    id: int
    request_id: int
    user_id: int
    created_at: datetime
    user: User

    class Config:
        orm_mode = True

class AuditRequest(AuditRequestInDBBase):
    pass 