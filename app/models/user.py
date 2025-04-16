from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.request import Request, CommentRequest
from app.models.audit import AuditRequest

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relación muchos a muchos con roles
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    requests = relationship("Request", back_populates="user", foreign_keys=[Request.user_id])
    supervised_requests = relationship("Request", back_populates="supervisor", foreign_keys=[Request.supervisor_id])
    request_comments = relationship("CommentRequest", back_populates="user")
    request_audits = relationship("AuditRequest", back_populates="user") 