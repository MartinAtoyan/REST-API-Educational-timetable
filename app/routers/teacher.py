from fastapi import Depends, APIRouter, HTTPException, Query
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


@router.get("/teachers", response_model=dict)
def list_teachers(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(get_db)
):
    total = db.query(Teacher).count()
    items = db.query(Teacher).offset(skip).limit(limit).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in data.dict().items():
        setattr(teacher, key, value)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return {"message": "Teacher deleted"}
