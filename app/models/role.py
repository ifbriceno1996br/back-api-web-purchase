from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255))
    
    # Relación muchos a muchos con usuarios
    users = relationship("User", secondary="user_roles", back_populates="roles") 