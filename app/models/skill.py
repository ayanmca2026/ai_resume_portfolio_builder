from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.base import Base
import enum

class SkillCategory(str, enum.Enum):
    language = "language"
    framework = "framework"
    database = "database"
    cloud = "cloud"
    tool = "tool"
    soft = "soft"

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String)
    category = Column(String) # use Enum in pydantic
    
    user = relationship("User", backref="skills")
