from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import User

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleInDBBase(RoleBase):
    id: int

    class Config:
        from_attributes = True

class Role(RoleInDBBase):
    users: List[User] = [] 