from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_role_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def create_with_user(self, db: Session, *, obj_in: RoleCreate) -> Role:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

role = CRUDRole(Role)


def create_with_user(db: Session, *, obj_in: RoleCreate) -> Role:
    obj_in_data = obj_in.dict()
    db_obj = Role(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
def get_role_by_name(db: Session, *, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()
def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role).order_by(Role.id).offset(skip).limit(limit).all()

def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(
        name=role.name,
        description=role.description
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[Role]:
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    
    update_data = role.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_role, field, value)
    
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    db_role = get_role(db, role_id)
    if not db_role:
        return False
    db.delete(db_role)
    db.commit()
    return True 