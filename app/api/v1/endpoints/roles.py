from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.role.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.role.RoleCreate,
) -> schemas.role.Role:
    role = crud.crud_role.get_role_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system.",
        )
    role = crud.crud_role.create_role(db=db, role=role_in)
    return role

@router.get("/", response_model=List[schemas.role.Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.role.Role]:
    roles = crud.crud_role.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=schemas.role.Role)
def read_role(
    role_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.role.Role:
    role = crud.crud_role.get_role(db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=schemas.role.Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: schemas.role.RoleUpdate,
) -> schemas.role.Role:
    role = crud.crud_role.get_role(db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role = crud.crud_role.update_role(db=db, role_id=role_id, role=role_in)
    return role

@router.delete("/{role_id}", response_model=dict)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
) -> dict:
    role = crud.crud_role.get_role(db, role_id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    crud.crud_role.delete_role(db=db, role_id=role_id)
    return {"message": "Role deleted successfully"} 