#agegar modelo de auditoria
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AuditRequest(Base):
    __tablename__ = "audit_requests"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(20), nullable=False)  # "create", "status_change"
    previous_status = Column(String(20), nullable=True)
    new_status = Column(String(20), nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    request = relationship("Request", back_populates="audit_logs")
    user = relationship("User", back_populates="request_audits")