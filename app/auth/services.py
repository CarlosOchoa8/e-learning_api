import re
from datetime import timedelta, datetime
from typing import Any

from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Security, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app import models
from app.helpers.db import get_db
from .settings import auth_settings
from .utils import get_token_auth_header, credentials_exception

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = auth_settings.SECRET_KEY
ALGORITHM = auth_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES


def validate_password(password: str) -> Any:
    regex = re.compile(
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%&*._])(?!.*\s).{5,15}$"
    )
    return re.fullmatch(regex, password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def authenticate_user(username: str, password: str, db: Session):
    if user := db.query(models.User).filter(models.User.username == username).first():  # type: ignore
        return user if verify_password(password, user.password) else False
    return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode['exp'] = expire
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()), db: Session = Depends(get_db)
):
    """
    Auth get current user.
    """
    token = get_token_auth_header(credentials)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("id"))
        user_obj = db.query(models.User).filter(models.User.id == user_id).first()  # type: ignore
        if not user_obj:
            raise credentials_exception()
        # VALIDAR EL TIEMPO DEL TOKEN
        # VALIDAR QUE EL USUARIO ESTÉ ACTIVO
    except Exception as e:
        raise credentials_exception() from e
    return user_obj


def generate_token(
    db: Session, username: str, password: str, fake_token: bool = False
) -> str:
    """
    Generate a token for a user.
    """
    db_user = authenticate_user(username=username, password=password, db=db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='El usuario o la contraseña no coinciden',
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # transaction = crud.tae_trans.get_transaction_by_user(
    #     db=db, user_id=user.id
    # )
    payload = {
        "id": str(db_user.id),  # type: ignore
        "first_name": str(db_user.first_name),  # type: ignore
        "last_name": str(db_user.last_name),  # type: ignore
        "email": str(db_user.email),  # type: ignore
    }
    # if fields := check_fields_to_generate_token(db=db, user=user):
    #     payments_id = MVEncrypter.encrypt(str(fields["payments_id"]))
    #     data_recover = {
    #         "transaction_id": payments_id.decode(),
    #         "user_id": user.id,
    #         "amount": fields["amount"],
    #     }
    #     payload.update(data_recover)

    # if fake_token is True:
    #     payload.update({"fake_token": "True"})

    return create_access_token(data=payload, expires_delta=access_token_expires)
