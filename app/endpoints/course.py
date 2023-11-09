from sqlalchemy.orm import Session
from fastapi import APIRouter, status, HTTPException, Depends
from app import crud, schemas
from app.helpers.db import get_db

router = APIRouter()


@router.post('/create/', description='Create new course')
def create(course_in: schemas.CourseCreateSchema, db: Session = Depends(get_db)):
    if course := crud.course.get_course_by_name(name=course_in.name, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'The course {course_in.name} already exists.')
    return crud.course.create(db=db, obj_in=course_in)


course_router = router
