"""
Generate an Object of CRUD
"""
from sqlalchemy.orm import Session
from app import schemas
from app.config.database.crud_base import CRUDBase
from app.models.lesson import Lesson as LessonModel


class CRUDLesson(CRUDBase[LessonModel, schemas.LessonCreateSchema, schemas.LessonUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """
    def get_lesson_by_name(self, name: str, db: Session):
        return db.query(self.model).filter(self.model.name == name).first()  # type: ignore


lesson = CRUDLesson(LessonModel)
