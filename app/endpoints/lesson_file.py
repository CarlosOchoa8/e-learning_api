from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from app import crud, schemas
from app.helpers.db import get_db

router = APIRouter()


@router.post('/create/', description='Append an image into a lesson.',
             response_model=schemas.LessonFileInDBSchema)
async def create(lesson_file_in: schemas.LessonFileCreateSchema, files_in: list[UploadFile] = File(default=None),
                 db: Session = Depends(get_db)):
    new_files = await crud.lesson_file.create(obj_in=lesson_file_in, file_in=files_in, db=db)
    return schemas.LessonFileInDBSchema(**new_files.__dict__)


@router.put('/update/{file_id}', description='Update lesson image.',
            response_model=schemas.LessonFileInDBSchema)
def update(lesson_file_in: schemas.LessonFileUpdateSchema, file_id: int, db: Session = Depends(get_db)):
    if lesson_file := crud.lesson_file.get(id=file_id, db=db):
        try:
            files_updated = crud.lesson_file.update(db=db, db_obj=lesson_file, obj_in=lesson_file_in)
            return schemas.LessonFileInDBSchema(**files_updated.__dict__)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='A problem has occurred while trying to update files.'
            ) from e
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='The lesson files does not exists.'
    )


@router.get('/detail/{lesson_id}', description="Get lesson's files detail.",
            response_model=list[schemas.LessonFilesSchema])
def get(lesson_id: int, db: Session = Depends(get_db)):
    if files := crud.lesson_file.get(id=lesson_id, db=db):
        return files
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='lesson files does not exists.'
    )


@router.get('/', description="Get all lesson's files")
def get_lesson_files(db: Session = Depends(get_db)):
    return crud.lesson_file.get_multi(db=db)


lesson_file_router = router
