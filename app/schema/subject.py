from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str
    hours: int | None = None
    exam_type: str | None = None
    required: str | None = None
    metadata: dict | None = None


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    id: int
    class Config:
        orm_mode = True

