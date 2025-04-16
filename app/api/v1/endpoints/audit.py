from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.audit.AuditRequest])
def read_audit_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    request_id: Optional[int] = None,
    user_id: Optional[int] = None,
    current_user: schemas.user.User = Depends(deps.has_role("supervisor")),
) -> List[schemas.audit.AuditRequest]:
    """
    Retrieve audit logs.
    Only supervisors can access this endpoint.
    """
    audit_logs = crud.audit.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        request_id=request_id,
        user_id=user_id
    )
    return audit_logs 