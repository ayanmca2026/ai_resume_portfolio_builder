from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    target_role = Column(String, nullable=True)
    ats_score = Column(Float, nullable=True)
    content_json = Column(Text) # The generated content representation
    template_name = Column(String, default="modern")
    
    pdf_path = Column(String, nullable=True)
    docx_path = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="resumes")
