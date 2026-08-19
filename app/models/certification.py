from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String)
    issuer = Column(String)
    year = Column(String)
    url = Column(String, nullable=True)
    
    user = relationship("User", backref="certifications")
