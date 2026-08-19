from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String)
    problem = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    technologies = Column(String, nullable=True) # comma separated
    features = Column(Text, nullable=True)
    contribution = Column(Text, nullable=True)
    results = Column(Text, nullable=True)
    github_url = Column(String, nullable=True)
    live_url = Column(String, nullable=True)
    
    # AI generated
    strength_score = Column(Float, nullable=True)
    resume_description = Column(Text, nullable=True)
    
    user = relationship("User", backref="projects")
