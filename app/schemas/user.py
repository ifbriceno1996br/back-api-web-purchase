from typing import Optional, List
from pydantic import BaseModel, EmailStr

class RoleBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role_ids: Optional[List[int]] = None

class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    role_ids: List[int]

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None
    roles: List[RoleBase] = []

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str 