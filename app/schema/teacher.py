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
        orm_mode = True
