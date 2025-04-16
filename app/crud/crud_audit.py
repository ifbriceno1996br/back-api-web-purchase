from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.audit import AuditRequest
from app.schemas.audit import AuditRequestBase

class CRUDAudit(CRUDBase[AuditRequest, AuditRequestBase, AuditRequestBase]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        request_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> List[AuditRequest]:
        query = db.query(self.model).join(self.model.user)
        if request_id is not None:
            query = query.filter(self.model.request_id == request_id)
        if user_id is not None:
            query = query.filter(self.model.user_id == user_id)
        return query.order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

audit = CRUDAudit(AuditRequest) 