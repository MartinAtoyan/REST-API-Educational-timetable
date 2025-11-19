from fastapi import Depends
from sqlalchemy.orm import Session
from app.schema import teacher as schemas
from app.models.teacher import Teacher, Subject, Lesson
from app.routers.app import get_db, app


@app.post("/teachers", response_model=schemas.Teacher)
def create_teacher(data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = Teacher(**data.dict())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


@app.get("/teachers", response_model=list[schemas.Teacher])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()
