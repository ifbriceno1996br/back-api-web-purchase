from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.user import User

class RequestBase(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: str = Field(..., max_length=500)
    status: str = Field("pendiente", max_length=20)
    amount: float
    expected_date: date = Field(..., description="Fecha esperada de entrega")

class RequestCreate(RequestBase):
    pass

class RequestUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, max_length=20)
    amount: Optional[float] = None
    expected_date: Optional[date] = None
    supervisor_id: Optional[int] = None
    comment: Optional[str] = Field(None, max_length=500)

class CommentRequestBase(BaseModel):
    comment: str = Field(..., max_length=500)

class CommentRequestCreate(CommentRequestBase):
    pass

class CommentRequestInDBBase(CommentRequestBase):
    id: int
    request_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CommentRequest(CommentRequestInDBBase):
    pass

class RequestInDBBase(RequestBase):
    id: int
    user_id: int
    supervisor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    comments: List[CommentRequest] = []
    user: User

    class Config:
        orm_mode = True

class Request(RequestInDBBase):
    pass

class RequestInDB(RequestInDBBase):
    pass 