"""
Generate an Object of CRUD
"""
from typing import Any
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.models.user import User as UserModel
from app.auth.services import get_password_hash
from app.config.database.crud_base import CRUDBase


class CRUDUser(CRUDBase[UserModel, schemas.UserCreateSchema, schemas.UserUpdateSchema]):
    """Item CRUD class

    Args:
        CRUDBase ([Item, ItemCreate, ItemUpdate])
    """
    def create(self, db: Session, obj_in: schemas.UserCreateSchema | dict[str, Any]) -> UserModel:
        """Create a ModelType object"""
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = get_password_hash(obj_in_data['password'])
        obj_in_data.pop("re_password")
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, email: str, db: Session):
        return db.query(self.model).filter(self.model.email == email).first()  # type: ignore

    def get_by_username(self, username: str, db: Session):
        return db.query(self.model).filter(self.model.username == username).first()  # type: ignore


user = CRUDUser(UserModel)
