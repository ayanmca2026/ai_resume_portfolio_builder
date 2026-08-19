from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    degree = Column(String)
    university = Column(String)
    department = Column(String, nullable=True)
    cgpa = Column(String, nullable=True)
    graduation_year = Column(String)
    coursework = Column(String, nullable=True)
    
    user = relationship("User", backref="educations")
