from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from app.schema import lesson as schemas
from app.models.lesson import Lesson
from app.models.teacher import Teacher
from app.models.subject import Subject
from app.deps import get_db
from fastapi import HTTPException

router = APIRouter()

@router.post("/lessons", response_model=schemas.Lesson)
def create_lesson(data: schemas.LessonCreate, db: Session = Depends(get_db)):
    # Validate foreign keys: teacher and subject must exist
    if data.teacher_id is not None:
        teacher = db.query(Teacher).filter(Teacher.id == data.teacher_id).first()
        if not teacher:
            raise HTTPException(status_code=400, detail=f"Teacher with id {data.teacher_id} does not exist")
    if data.subject_id is not None:
        subject = db.query(Subject).filter(Subject.id == data.subject_id).first()
        if not subject:
            raise HTTPException(status_code=400, detail=f"Subject with id {data.subject_id} does not exist")

    lesson = Lesson(**data.dict())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/lessons", response_model=dict)
def list_lessons(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(get_db)
):
    total = db.query(Lesson).count()
    items = db.query(Lesson).offset(skip).limit(limit).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.put("/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(lesson_id: int, data: schemas.LessonCreate, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    for key, value in data.dict().items():
        setattr(lesson, key, value)
    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}
