from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schema import subject as schemas
from app.models.subject import Subject, Lesson
from app.deps import get_db

router = APIRouter()

@router.post("/subjects", response_model=schemas.Subject)
def create_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = Subject(**data.dict())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/subjects", response_model=list[schemas.Subject])
def list_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()


@router.put("/subjects/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return {"error": "Subject not found"}
    for key, value in data.dict().items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject

@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return {"error": "Subject not found"}
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted"}
