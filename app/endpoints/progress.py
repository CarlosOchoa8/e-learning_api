from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app import crud
from app import models
from app import schemas
from app.auth.services import get_current_user
from app.helpers.db import get_db

router = APIRouter()


@router.post('/create', status_code=200, response_model=schemas.LessonProgressInDB)
def check_progress(lesson: schemas.LessonProgressCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user),
                   ):
    lesson.user_id = current_user.id

    try:
        if lesson_checked := db.query(models.Progress)\
                .filter(and_(models.Progress.user_id == current_user.id,
                             models.Progress.lesson_id == lesson.lesson_id)).first():
            return crud.progress.update(obj_in=lesson, db_obj=lesson_checked, db=db)

        return crud.progress.create(obj_in=lesson, db=db)
    except BaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Algo ha salido mal.") from e


@router.get("/course_progress/{course_id}")
def get_course_progress(course_id: int,
                        db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)) -> str:
    return crud.progress.get_course_progress(course_id=course_id, db=db)


progress_router = router
