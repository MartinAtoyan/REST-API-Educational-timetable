from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schema import lesson as schemas
from app.models.lesson import Lesson
from app.deps import get_db

router = APIRouter()

@router.post("/lessons", response_model=schemas.Lesson)
def create_lesson(data: schemas.LessonCreate, db: Session = Depends(get_db)):
    lesson = Lesson(**data.dict())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/lessons", response_model=list[schemas.Lesson])
def list_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@router.put("/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(lesson_id: int, data: schemas.LessonCreate, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return {"error": "Lesson not found"}
    for key, value in data.dict().items():
        setattr(lesson, key, value)
    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return {"error": "Lesson not found"}
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}
