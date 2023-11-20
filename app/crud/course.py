"""
Generate an Object of CRUD
"""
from sqlalchemy.orm import Session
from app import schemas
from app.config.database.crud_base import CRUDBase
from app.models.course import Course as CourseModel


class CRUDCourse(CRUDBase[CourseModel, schemas.CourseCreateSchema, schemas.CourseUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """
    def get_course_by_name(self, name: str, db: Session):
        return db.query(self.model).filter(self.model.name == name).first()  # type: ignore


course = CRUDCourse(CourseModel)
