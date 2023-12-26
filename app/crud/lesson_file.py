"""
Generate an Object of CRUD
"""
from typing import Any
from sqlalchemy.orm import Session
from fastapi import File, UploadFile
from fastapi.encoders import jsonable_encoder
from app import schemas, crud
from app.utils.save_files import save_files_to_static
from app.models.lesson_files import LessonFile as LessonFileModel
from app.config.database.crud_base import CRUDBase, CreateSchemaType, ModelType
from app.config.common import Settings


class CRUDLessonFile(CRUDBase[LessonFileModel, schemas.LessonFileCreateSchema, schemas.LessonFileUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """
    async def create(self, db: Session, obj_in: CreateSchemaType | dict[str, Any],
                     file_in: UploadFile = File(default=None)) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        lesson_id = obj_in_data['lesson_id']
        lesson = crud.lesson.get(db=db, id=lesson_id)
        course_name = lesson.course.name

        files_saved = await save_files_to_static(course=course_name, upload_file=file_in)
        obj_in_data['file'] = files_saved
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        print(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, id: int, db: Session) -> LessonFileModel:
        """Get a single ModelType filtered by id"""
        lesson_files = db.query(self.model).filter(self.model.lesson_id == id).all()
        app_settings = Settings()
        api_domain = app_settings.API_DOMAIN
        schema_response = [schemas.LessonFilesSchema(
            id=item.id,
            file=f"{api_domain}{item.file.strip('{}')}") for item in lesson_files]
        return schema_response  # type: ignore


lesson_file = CRUDLessonFile(LessonFileModel)
