from functools import wraps
from app import models, crud
from fastapi import HTTPException, status
from app.utils.constants import UserType


def check_user_type(user_type: UserType):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            db = kwargs.get("db")

            if not db.query(models.User).filter(models.User.id == current_user.id,
                                                models.User.user_type == user_type).first():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Your user type has not permission to do this.'
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
