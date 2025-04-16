from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud, schemas
from app.api import deps
from app.models import CommentRequest, AuditRequest
from datetime import date
import csv
import io

router = APIRouter()


@router.post("/", response_model=schemas.request.Request)
def create_request(
        *,
        db: Session = Depends(deps.get_db),
        request_in: schemas.request.RequestCreate,
        current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> schemas.request.Request:
    """
    Create new request.
    """
    # Si el usuario es supervisor, se asigna como supervisor de la solicitud
    supervisor_id = None
    if any(role.name == "supervisor" for role in current_user.roles):
        supervisor_id = current_user.id

    # Crear la solicitud con el usuario actual
    request = crud.crud_request.create_with_user(
        db=db,
        obj_in=request_in,
        user_id=current_user.id,
        supervisor_id=supervisor_id
    )

    # Registrar en auditoría
    audit = AuditRequest(
        action="create",
        new_status=request.status,
        request_id=request.id,
        user_id=current_user.id
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    return request


@router.get("/", response_model=List[schemas.request.Request])
def read_requests(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        supervisor_id: Optional[int] = None,
        # current_user: schemas.user.User = Depends(deps.has_role("supervisor")),
) -> List[schemas.request.Request]:
    """
    Retrieve requests. Only supervisors can list requests.
    """
    requests = crud.crud_request.get_multi(
        db=db, skip=skip, limit=limit, user_id=user_id, supervisor_id=supervisor_id
    )
    return requests


@router.get("/{request_id}", response_model=schemas.request.Request)
def read_request(
        *,
        db: Session = Depends(deps.get_db),
        request_id: int,
        current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> schemas.request.Request:
    """
    Get request by ID.
    """
    request = crud.crud_request.get(db=db, id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@router.put("/{request_id}", response_model=schemas.request.Request)
def update_request(
        *,
        db: Session = Depends(deps.get_db),
        request_id: int,
        request_in: schemas.request.RequestUpdate,
        current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> schemas.request.Request:
    """
    Update a request.
    """
    request = crud.crud_request.get(db=db, id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request = crud.crud_request.update(db=db, db_obj=request, obj_in=request_in)
    return request


@router.put("/{request_id}/status", response_model=schemas.request.Request)
def change_status_request(
        *,
        db: Session = Depends(deps.get_db),
        request_id: int,
        request_in: schemas.request.RequestUpdate,
        current_user: schemas.user.User = Depends(deps.has_role("supervisor")),
) -> schemas.request.Request:
    """
    Change request status. Only supervisors can approve or reject requests.
    A comment is required if:
    - The request amount is greater than 500
    - The status is "rechazado"
    """
    # Obtener la solicitud
    request = crud.crud_request.get(db=db, id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Validar que el status sea "aprobado" o "rechazado"
    if request_in.status not in ["aprobado", "rechazado"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be either 'aprobado' or 'rechazado'"
        )
    
    # Validar que se requiera comentario
    requires_comment = request.amount > 500 or request_in.status == "rechazado"
    if requires_comment and not request_in.comment:
        raise HTTPException(
            status_code=400,
            detail="Comment is required" if request_in.status=="rechazado" else "Comment is required for rejected requests or requests with amount greater than 500"
        )
    
    # Crear el comentario si se proporciona
    if request_in.comment:
        comment = CommentRequest(
            comment=request_in.comment,
            request_id=request_id,
            user_id=current_user.id
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
    
    # Registrar en auditoría antes de actualizar
    audit = AuditRequest(
        action="status_change",
        previous_status=request.status,
        new_status=request_in.status,
        comment=request_in.comment,
        request_id=request_id,
        user_id=current_user.id
    )
    db.add(audit)
    
    # Actualizar la solicitud
    request = crud.crud_request.update(
        db=db,
        db_obj=request,
        obj_in=request_in
    )
    
    db.commit()
    db.refresh(audit)
    return request


@router.delete("/{request_id}", response_model=dict)
def delete_request(
        *,
        db: Session = Depends(deps.get_db),
        request_id: int,
        current_user: schemas.user.User = Depends(deps.get_current_active_user),
) -> dict:
    """
    Delete a request.
    """
    request = crud.crud_request.get(db=db, id=request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    crud.crud_request.remove(db=db, id=request_id)
    return {"message": "Request deleted successfully"}


@router.get("/report/csv")
def download_request_report(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    current_user: schemas.user.User = Depends(deps.has_role("supervisor")),
) -> Response:
    """
    Download request report in CSV format.
    Only supervisors can access this endpoint.
    """
    # Execute the stored procedure
    result = db.execute(
        text("EXEC sp_GetRequestReport @StartDate=:start_date, @EndDate=:end_date, @Status=:status, @UserId=:user_id"),
        {
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "user_id": user_id
        }
    ).fetchall()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Request ID", "Title", "Description", "Status", "Amount", 
        "Expected Date", "Created At", "Updated At",
        "Creator Email", "Creator Name",
        "Supervisor Email", "Supervisor Name",
        "Last Status Change", "Last Status Change Date", "Last Status Comment",
        "Comment Count", "Days Since Creation", "Days Until Expected Date"
    ])
    
    # Write data
    for row in result:
        writer.writerow([
            row.RequestId, row.RequestTitle, row.RequestDescription,
            row.RequestStatus, row.RequestAmount, row.ExpectedDate,
            row.RequestCreatedAt, row.RequestUpdatedAt,
            row.RequestCreatorEmail, row.RequestCreatorName,
            row.SupervisorEmail, row.SupervisorName,
            row.LastStatusChange, row.LastStatusChangeDate, row.LastStatusComment,
            row.CommentCount, row.DaysSinceCreation, row.DaysUntilExpectedDate
        ])
    
    # Prepare response
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=request_report.csv"
        }
    )


@router.get("/user-stats/csv")
def download_user_stats_report(
    db: Session = Depends(deps.get_db),
    current_user: schemas.user.User = Depends(deps.has_role("supervisor")),
) -> Response:
    """
    Download user request statistics report in CSV format.
    Only supervisors can access this endpoint.
    """
    # Execute the stored procedure
    result = db.execute(
        text("EXEC sp_GetUserRequestStats")
    ).fetchall()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "User ID", "Email", "Name", 
        "Total Requests", "Approved Requests", "Rejected Requests", "Pending Requests",
        "Average Amount", "Max Amount", "Min Amount"
    ])
    
    # Write data
    for row in result:
        writer.writerow([
            row.UserId, row.UserEmail, row.UserName,
            row.TotalRequests, row.ApprovedRequests, row.RejectedRequests, row.PendingRequests,
            row.AverageAmount, row.MaxAmount, row.MinAmount
        ])
    
    # Prepare response
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=user_stats_report.csv"
        }
    )
