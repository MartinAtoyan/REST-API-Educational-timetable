from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    department = Column(String)
    position = Column(String)
    degree = Column(String)

    lessons = relationship("Lesson", back_populates="teacher")
