from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    department = Column(String)
    position = Column(String)
    degree = Column(String)

    lessons = relationship("Lesson", back_populates="teacher")
