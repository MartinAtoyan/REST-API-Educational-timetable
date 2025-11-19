from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hours = Column(Integer)
    exam_type = Column(String)
    required = Column(String)

    lessons = relationship("Lesson", back_populates="subject")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    classroom = Column(String)
    group = Column(String)
    lesson_type = Column(String)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    teacher = relationship("Teacher", back_populates="lessons")
    subject = relationship("Subject", back_populates="lessons")
