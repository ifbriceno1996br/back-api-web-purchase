from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=schemas.token.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Get role information
    role_names = [role.name for role in user.roles]
    role_name = role_names[0] if role_names else "No Role"
    
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "user_id": user.id,
        "full_name": user.full_name,
        "role_name": role_name,
        "roles": role_names
    }

@router.post("/refresh", response_model=schemas.token.Token)
def refresh_token(
    refresh_token: schemas.token.RefreshToken,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Refresh access token
    """
    token_data = security.verify_token(refresh_token.refresh_token)
    if not token_data or not token_data.get("refresh"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = int(token_data["sub"])
    user = crud.crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Get role information
    role_names = [role.name for role in user.roles]
    role_name = role_names[0] if role_names else "No Role"
    
    access_token = security.create_access_token(user.id)
    new_refresh_token = security.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
        "user_id": user.id,
        "full_name": user.full_name,
        "role_name": role_name,
        "roles": role_names
    }

@router.post("/logout", response_model=schemas.token.Message)
def logout(
    current_user: schemas.user.User = Depends(deps.get_current_user)
) -> Any:
    """
    Logout user and invalidate current token
    """
    return {"message": "Successfully logged out"} 