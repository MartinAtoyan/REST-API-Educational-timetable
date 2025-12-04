from fastapi import FastAPI
from database import SessionLocal

app = FastAPI()

from app.routers.lesson import router as lesson_router
from app.routers.teacher import router as teacher_router
from app.routers.subject import router as subject_router
from app.routers.queries import router as queries_router

app.include_router(lesson_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(queries_router)


