from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schema import teacher as schemas
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.models.lesson import Lesson
from app.deps import get_db

router = APIRouter()


@router.post("/teachers", response_model=schemas.Teacher)
def create_teacher(data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = Teacher(**data.dict())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


@router.get("/teachers", response_model=list[schemas.Teacher])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()


@router.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return {"error": "Teacher not found"}
    for key, value in data.dict().items():
        setattr(teacher, key, value)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return {"error": "Teacher not found"}
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}
