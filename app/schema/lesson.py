from pydantic import BaseModel
from datetime import date, time


class LessonBase(BaseModel):
    date: date
    time: time
    classroom: str | None = None
    group: str | None = None
    lesson_type: str | None = None
    teacher_id: int
    subject_id: int


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    id: int
    class Config:
        orm_mode = True
