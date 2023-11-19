"""
Generate an Object of CRUD
"""
from typing import Any
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.utils.save_files import save_files_to_static
from app.models.lesson_files import LessonFile as LessonFileModel
from app.config.database.crud_base import CRUDBase, CreateSchemaType, ModelType


class CRUDLessonFile(CRUDBase[LessonFileModel, schemas.LessonFileCreateSchema, schemas.LessonFileUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """
    async def create(self, db: Session, obj_in: CreateSchemaType | dict[str, Any],
                     file_in: UploadFile = File(default=None)) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        files_saved = await save_files_to_static(file_in)
        obj_in_data['file'] = files_saved
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


lesson_file = CRUDLessonFile(LessonFileModel)
