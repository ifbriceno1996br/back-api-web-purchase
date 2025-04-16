from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float,Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    description = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default="pendiente")
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expected_date = Column(Date, nullable=True)
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="requests")
    supervisor = relationship("User", foreign_keys=[supervisor_id], back_populates="supervised_requests")
    comments = relationship("CommentRequest", back_populates="request", cascade="all, delete-orphan")
    audit_logs = relationship("AuditRequest", back_populates="request", cascade="all, delete-orphan")

class CommentRequest(Base):
    __tablename__ = "comment_requests"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    request = relationship("Request", back_populates="comments")
    user = relationship("User", back_populates="request_comments") 