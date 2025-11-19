from fastapi import Depends
from sqlalchemy.orm import Session
from app.schema import subject as schemas
from app.models.subject import Subject, Lesson
from app.routers.app import get_db, app

@app.post("/subjects", response_model=schemas.Subject)
def create_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = Subject(**data.dict())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@app.get("/subjects", response_model=list[schemas.Subject])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()
