"""
Generate an Object of CRUD
"""

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.config.database.crud_base import CRUDBase
from app.models import Progress


class CRUDProgress(CRUDBase[Progress, schemas.LessonProgressCreate, schemas.LessonProgressUpdate]):
    """Item CRUD class
    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """

    def get_course_progress(self, course_id: int, db: Session) -> str:
        """
        Cáculo de lecciones totales y porcentaje por lecciones completadas.
        """
        total_lessons = (
            db.query(func.count())
            .filter(models.Lesson.course_id == course_id)
            .scalar()
        )

        completed_lessons = (
            db.query(func.count())
            .filter(
                and_(
                    self.model.lesson_completed == True,
                    self.model.lesson_id.in_(
                        db.query(models.Lesson.id).filter(models.Lesson.course_id == course_id)
                    )
                )
            )
            .scalar()
        )
        return f"{round((completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0, 2)}%"


progress = CRUDProgress(Progress)
