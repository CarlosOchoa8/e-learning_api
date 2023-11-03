from typing import Any
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, schemas
from app.helpers.db import get_db
from app.auth.services import generate_token


router = APIRouter()


@router.post('/login/', description='Sign-in.', response_model=schemas.Token)
def login_for_access_token(authenticate: schemas.UserAuthSchema, db: Session = Depends(get_db)):
    access_token = generate_token(db=db, username=authenticate.username, password=authenticate.password)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post("/create/", description='Create an user.', response_model=schemas.UserResponseSchema)
def create_user(user_in: schemas.UserCreateSchema,
                db: Session = Depends(get_db)):
    if crud.user.get_by_username(db=db, username=user_in.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Already exists an user with username {user_in.username}')
    if crud.user.get_by_email(db=db, email=user_in.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Already exists an user with email {user_in.email}')
    try:
        user_created = (crud.user.create(db=db, obj_in=user_in))
        return schemas.UserResponseSchema(**user_created.__dict__)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Has been occurred a problem trying create the user.') from e


@router.put('/update/{user_id}', description='Update an user.', response_model=schemas.UserInDBSchema)
def update_user(user_id: int,
                user_in: schemas.UserUpdateSchema,
                db: Session = Depends(get_db)):
    if user_obj := crud.user.get(db=db, id=user_id):
        try:
            user_updated = crud.user.update(db=db, obj_in=user_in, db_obj=user_obj)
            return schemas.UserInDBSchema(**user_updated.__dict__)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Has been occurred a problem trying update the user.') from e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'User id {user_id} does not exist.')


@router.get('/', description='Get all users.')
def get_users(db: Session = Depends(get_db)):
    try:
        user_objs = crud.user.get_multi(db=db)
        return user_objs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='An error has been occurred while getting users.') from e


@router.get('/detail/{user_id}', description='Get user detail.', response_model=schemas.UserResponseSchema)
def get_user(user_id: int,
             db: Session = Depends(get_db)) -> dict | Any:
    try:
        user_obj = crud.user.get(db=db, id=user_id)
        return schemas.UserInDBSchema(**user_obj.__dict__)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Has been occurred a problem getting user.') from e


user_router = router
