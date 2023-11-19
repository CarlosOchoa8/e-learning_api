from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from app import crud, schemas
from app.helpers.db import get_db

router = APIRouter()


@router.post('/create/', description='Add new lesson')
async def create(files_in: list[UploadFile] = File(default=None), lesson_in: schemas.LessonFileCreateSchema | None = None, db: Session = Depends(get_db)):
    return await crud.lesson_file.create(obj_in=lesson_in, file_in=files_in, db=db)


lesson_file_router = router
