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


@router.put('/update/{course_id}', response_model=schemas.CourseInDBSchema)
def update(course_id: int, course_in: schemas.CourseUpdateSchema, db: Session = Depends(get_db)):
    if course_exists := crud.course.get_course_by_name(name=course_in.name, db=db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'The course {course_in.name} already exists.')
    course_db = crud.course.get(id=course_id, db=db)
    updated_course_db = crud.course.update(obj_in=course_in, db_obj=course_db, db=db)
    return schemas.CourseInDBSchema(**updated_course_db.__dict__)


@router.get('/detail/{course_id}', response_model=schemas.CourseInDBSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    if course_db := crud.course.get(id=course_id, db=db):
        return schemas.CourseInDBSchema(**course_db.__dict__)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Course does not exists.')


@router.get('/', response_model=schemas.CoursesInDBSchema)
def get_courses(db: Session = Depends(get_db)):
    if courses_db := crud.course.get_multi(db=db):
        courses = [
            schemas.CourseInDBSchema(**course.__dict__)
            for course in courses_db
        ]
        return schemas.CoursesInDBSchema(courses=courses)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Something gone wrong while getting courses.')


course_router = router
