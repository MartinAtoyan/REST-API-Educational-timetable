from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hours = Column(Integer)
    exam_type = Column(String)
    required = Column(String)
    metadata = Column(JSONB, nullable=True)

    lessons = relationship("Lesson", back_populates="subject")
