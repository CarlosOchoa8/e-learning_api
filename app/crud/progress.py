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

    def get_user_statistics(self, user_id: int, db: Session):
        # get completed lessons
        completed_lessons = (
            db.query(Progress.lesson_id)
            .filter_by(user_id=user_id, lesson_completed=True)
            .distinct()
            .subquery()
        )
        # get lessons registered by course
        total_lessons_by_course = (
            db.query(models.Lesson.course_id, func.count(models.Lesson.id).label("total_lessons"))
            .group_by(models.Lesson.course_id)
            .all()
        )

        # get lessons completed by course
        completed_lessons_by_course = (
            db.query(models.Lesson.course_id, func.count(Progress.lesson_id).label("completed_lessons"))
            .join(Progress)
            .filter(Progress.lesson_id.in_(completed_lessons))
            .group_by(models.Lesson.course_id)
            .all()
        )

        progress_by_course = []
        for total, completed in zip(total_lessons_by_course, completed_lessons_by_course):
            course_id = total[0]
            total_lessons = total[1]
            completed_lessons = completed[1]
            progress_ = (
                (completed_lessons / total_lessons) * 100
                if total_lessons > 0
                else 0
            )
            progress_by_course.append({"course_id": course_id, "progress": f"{progress_} %"})
        return progress_by_course


progress = CRUDProgress(Progress)
