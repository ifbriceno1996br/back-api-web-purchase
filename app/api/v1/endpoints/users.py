from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: schemas.user.User = Depends(deps.get_current_active_superuser),
) -> schemas.user.User:
    user = crud.crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.crud_user.create_user(db=db, user=user_in)
    return user

@router.get("/", response_model=List[schemas.user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> List[schemas.user.User]:
    users = crud.crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> schemas.user.User:
    user = crud.crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.user.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.user.UserUpdate,
    current_user: schemas.user.User = Depends(deps.get_current_active_superuser),
) -> schemas.user.User:
    user = crud.crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.crud_user.update_user(db=db, user_id=user_id, user=user_in)
    return user

@router.delete("/{user_id}", response_model=dict)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: schemas.user.User = Depends(deps.get_current_active_superuser),
) -> dict:
    user = crud.crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.crud_user.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"} 