from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    company = Column(String)
    role = Column(String)
    duration = Column(String)
    responsibilities = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    
    user = relationship("User", backref="experiences")
