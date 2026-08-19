from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
from app.database.base import Base

class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company = Column(String)
    role = Column(String)
    location = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    status = Column(String, default="Saved")
    match_score = Column(Float, nullable=True)
    ats_score = Column(Float, nullable=True)
    resume_version = Column(String, nullable=True)
    cover_letter = Column(Text, nullable=True)
    applied_at = Column(DateTime, nullable=True)
    interview_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    user = relationship("User")
