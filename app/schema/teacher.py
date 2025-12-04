from pydantic import BaseModel

class TeacherBase(BaseModel):
    full_name: str
    department: str | None = None
    position: str | None = None
    degree: str | None = None


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    id: int
    class Config:
        from_attributes = True


class TeacherLessonCount(BaseModel):
    teacher_id: int
    teacher_name: str
    lesson_count: int
