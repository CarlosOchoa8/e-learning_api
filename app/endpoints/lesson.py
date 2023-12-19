from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from app import crud, schemas
from app.helpers.db import get_db

router = APIRouter()


@router.post('/create/', response_model=schemas.LessonInDBSchema, description='Add new lesson')
def create(lesson_in: schemas.LessonCreateSchema, db: Session = Depends(get_db)):
    if lesson_exists := crud.lesson.get_lesson_by_name(name=lesson_in.name, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Lesson {lesson_in.name} already exists.')
    new_lesson = crud.lesson.create(obj_in=lesson_in, db=db)
    return schemas.LessonInDBSchema(**new_lesson.__dict__)


@router.get('/detail/{lesson_id}', response_model=schemas.LessonInDBSchema)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    if lesson := crud.lesson.get(id=lesson_id, db=db):
        return lesson
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Lesson not found.'
    )


@router.get('/', response_model=list[schemas.LessonInDBSchema])
def get_lessons(db: Session = Depends(get_db)):
    if lessons := crud.lesson.get_multi(db=db):
        return lessons
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Lesson not found.'
    )


lesson_router = router
