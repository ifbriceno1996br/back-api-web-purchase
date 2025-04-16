from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.request import Request
from app.schemas.request import RequestCreate, RequestUpdate


class CRUDRequest(CRUDBase[Request, RequestCreate, RequestUpdate]):
    def create_with_user(
            self, db: Session, *, obj_in: RequestCreate, user_id: int, supervisor_id: Optional[int] = None
    ) -> Request:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, user_id=user_id, supervisor_id=supervisor_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[Request]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(
        self, db: Session, *, db_obj: Request, obj_in: Union[RequestUpdate, Dict[str, Any]]
    ) -> Request:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
            supervisor_id: Optional[int] = None
    ) -> List[Request]:
        query = db.query(self.model).join(self.model.user)
        if user_id is not None:
            query = query.filter(self.model.user_id == user_id)
        if supervisor_id is not None:
            query = query.filter(self.model.supervisor_id == supervisor_id)
        return query.order_by(self.model.id).offset(skip).limit(limit).all()


request = CRUDRequest(Request)


def get(db: Session, id: int) -> Optional[Request]:
    return db.query(Request).filter(Request.id == id).first()


def update(
        db: Session, *, db_obj: Request, obj_in: Union[RequestUpdate, Dict[str, Any]]
) -> Request:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.dict(exclude_unset=True)

    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
def get_multi(
        # self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        supervisor_id: Optional[int] = None
) -> List[Request]:
    query = db.query(Request)
    if user_id is not None:
        query = query.filter(Request.user_id == user_id)
    if supervisor_id is not None:
        query = query.filter(Request.supervisor_id == supervisor_id)
    return query.order_by(Request.id).offset(skip).limit(limit).all()

def create_with_user(
        db: Session, *, obj_in: RequestCreate, user_id: int, supervisor_id: Optional[int] = None
) -> Request:
    obj_in_data = obj_in.dict()
    db_obj = Request(**obj_in_data, user_id=user_id, supervisor_id=supervisor_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_request(db: Session, request_id: int) -> Optional[Request]:
    return db.query(Request).filter(Request.id == request_id).first()


def get_requests(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        supervisor_id: Optional[int] = None
) -> List[Request]:
    query = db.query(Request).order_by(Request.id)
    if user_id is not None:
        query = query.filter(Request.user_id == user_id)
    if supervisor_id is not None:
        query = query.filter(Request.supervisor_id == supervisor_id)
    return query.offset(skip).limit(limit).all()


def create_request(db: Session, request: RequestCreate) -> Request:
    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def update_request(
        db: Session,
        request_id: int,
        request: RequestUpdate
) -> Optional[Request]:
    db_request = get_request(db, request_id)
    if db_request:
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_request, field, value)
        db.commit()
        db.refresh(db_request)
    return db_request


def delete_request(db: Session, request_id: int) -> bool:
    db_request = get_request(db, request_id)
    if db_request:
        db.delete(db_request)
        db.commit()
        return True
    return False
