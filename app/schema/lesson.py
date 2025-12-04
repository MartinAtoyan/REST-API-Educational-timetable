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

class LessonWithDetails(Lesson):
    teacher_name: str
    subject_name: str
    
    class Config:
        from_attributes = True


class UpdateLessonsRequest(BaseModel):
    min_lesson_count: int = 5
    new_classroom: str