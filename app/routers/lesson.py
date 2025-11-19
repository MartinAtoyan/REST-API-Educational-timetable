from fastapi import Depends
from sqlalchemy.orm import Session
from app.schema import lesson as schemas
from app.models.lesson import Lesson
from app.routers.app import get_db, app

@app.post("/lessons", response_model=schemas.Lesson)
def create_lesson(data: schemas.LessonCreate, db: Session = Depends(get_db)):
    lesson = Lesson(**data.dict())
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@app.get("/lessons", response_model=list[schemas.Lesson])
def list_lessons(db: Session = Depends(get_db)):
    return db.query(Lesson).all()
