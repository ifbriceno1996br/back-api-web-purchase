from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).options(joinedload(User.roles)).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).options(joinedload(User.roles)).order_by(User.id).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_active=True
    )
    
    # Asignar roles al usuario
    from app.models.role import Role
    roles = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
    db_user.roles = roles
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Actualizar roles si se proporcionan
    if "role_ids" in update_data:
        from app.models.role import Role
        roles = db.query(Role).filter(Role.id.in_(update_data.pop("role_ids"))).all()
        db_user.roles = roles
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def add_role_to_user(db: Session, user_id: int, role_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    from app.models.role import Role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return False
    user.roles.append(role)
    db.commit()
    return True

def remove_role_from_user(db: Session, user_id: int, role_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    from app.models.role import Role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return False
    user.roles.remove(role)
    db.commit()
    return True 