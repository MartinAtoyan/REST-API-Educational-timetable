from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from app.schema import subject as schemas
from app.models.subject import Subject
from app.deps import get_db

router = APIRouter()

@router.post("/subjects", response_model=schemas.Subject)
def create_subject(data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = Subject(**data.dict())
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("/subjects", response_model=dict)
def list_subjects(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(get_db)
):
    total = db.query(Subject).count()
    items = db.query(Subject).offset(skip).limit(limit).all()
    return {"items": items, "total": total, "skip": skip, "limit": limit}


@router.get("/subjects/{subject_id}", response_model=schemas.Subject)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.put("/subjects/{subject_id}", response_model=schemas.Subject)
def update_subject(subject_id: int, data: schemas.SubjectCreate, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in data.dict().items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject

@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted"}
