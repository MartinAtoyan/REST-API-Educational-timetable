from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import sqlalchemy as sa
from sqlalchemy import func
from app.deps import get_db
from app.models import Lesson, Teacher, Subject
from app.schema import lesson as lesson_schemas
from app.schema import teacher as teacher_schemas

router = APIRouter()


@router.get("/lessons/by-teacher-date/", response_model=List[lesson_schemas.Lesson])
def get_lessons_by_teacher_and_date(
    teacher_id: int = Query(..., description="Teacher ID"),
    date_str: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    from datetime import datetime
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    lessons = db.query(Lesson).filter(
        Lesson.teacher_id == teacher_id,
        Lesson.date == date
    ).all()
    
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this teacher on this date")
    
    return lessons


@router.get("/lessons-detailed/", response_model=List[lesson_schemas.LessonWithDetails])
def get_lessons_with_details(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    lessons = db.query(
        Lesson.id,
        Lesson.date,
        Lesson.time,
        Lesson.classroom,
        Lesson.group,
        Lesson.lesson_type,
        Lesson.teacher_id,
        Teacher.full_name.label('teacher_name'),
        Lesson.subject_id,
        Subject.name.label('subject_name')
    ).join(Teacher, Lesson.teacher_id == Teacher.id).join(
        Subject, Lesson.subject_id == Subject.id
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": row[0],
            "date": row[1],
            "time": row[2],
            "classroom": row[3],
            "group": row[4],
            "lesson_type": row[5],
            "teacher_id": row[6],
            "teacher_name": row[7],
            "subject_id": row[8],
            "subject_name": row[9]
        }
        for row in lessons
    ]



@router.post("/lessons/update-prolific-teachers/")
def update_lessons_for_prolific_teachers(
    request: lesson_schemas.UpdateLessonsRequest,
    db: Session = Depends(get_db)
):
    subquery = db.query(Teacher.id).join(Lesson).group_by(Teacher.id).having(
        func.count(Lesson.id) >= request.min_lesson_count
    ).subquery()
    # use subquery directly in IN expression
    updated_count = db.query(Lesson).filter(
        Lesson.teacher_id.in_(subquery)
    ).update({Lesson.classroom: request.new_classroom}, synchronize_session=False)
    
    db.commit()
    
    return {
        "message": f"Updated {updated_count} lessons for teachers with at least {request.min_lesson_count} lessons",
        "updated_count": updated_count
    }



@router.get("/teachers/lesson-counts/", response_model=List[teacher_schemas.TeacherLessonCount])
def get_lesson_counts_per_teacher(db: Session = Depends(get_db)):
    results = db.query(
        Teacher.id,
        Teacher.full_name,
        func.count(Lesson.id).label('lesson_count')
    ).outerjoin(Lesson, Teacher.id == Lesson.teacher_id).group_by(
        Teacher.id,
        Teacher.full_name
    ).all()
    
    return [
        {
            "teacher_id": row[0],
            "teacher_name": row[1],
            "lesson_count": row[2]
        }
        for row in results
    ]


@router.get("/lessons-paginated/")
def get_lessons_paginated(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    sort_by: str = Query("date", description="Sort by: date, time, or classroom"),
    order: str = Query("asc", description="Order: asc or desc"),
    db: Session = Depends(get_db)
):
    valid_sorts = ["date", "time", "classroom"]
    if sort_by not in valid_sorts:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {valid_sorts}")
    
    if order.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order must be 'asc' or 'desc'")
    
    query = db.query(Lesson)
    
    if sort_by == "date":
        if order.lower() == "desc":
            query = query.order_by(Lesson.date.desc())
        else:
            query = query.order_by(Lesson.date.asc())
    elif sort_by == "time":
        if order.lower() == "desc":
            query = query.order_by(Lesson.time.desc())
        else:
            query = query.order_by(Lesson.time.asc())
    elif sort_by == "classroom":
        if order.lower() == "desc":
            query = query.order_by(Lesson.classroom.desc())
        else:
            query = query.order_by(Lesson.classroom.asc())
    
    lessons = query.offset(skip).limit(limit).all()
    
    return lessons


@router.get("/subjects/search/", response_model=List[dict])
def search_subjects(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db)
):
    
    sql = sa.text(
        """
        SELECT id, name, metadata
        FROM subjects
        WHERE name % :q OR (metadata->>'description') % :q
        ORDER BY greatest(similarity(name, :q), similarity(metadata->>'description', :q)) DESC
        LIMIT :limit OFFSET :skip
        """
    )

    res = db.execute(sql, {"q": q, "limit": limit, "skip": skip}).mappings().all()

    return [
        {"id": row['id'], "name": row['name'], "metadata": row['metadata']} for row in res
    ]
