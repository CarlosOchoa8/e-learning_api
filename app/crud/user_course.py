"""
Generate an Object of CRUD
"""
from app import schemas
from app.config.database.crud_base import CRUDBase
from app.models import UserCourse as UserCourseModel


class CRUDUserCourse(CRUDBase[UserCourseModel, schemas.UserCourseCreateSchema, schemas.UserCourseUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """


user_course = CRUDUserCourse(UserCourseModel)
