from typing import Any, ClassVar

from fastapi import HTTPException, status
from pydantic import Field, BaseModel, EmailStr, field_validator, model_validator
from app.auth.services import validate_password
from app.utils import constants


class UserBaseSchema(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    first_name: str = Field(min_length=5, max_length=50, examples=['Some First Name'])
    last_name: str = Field(min_length=5, max_length=50, examples=['Some Last Name'])
    email: EmailStr = Field(examples=['Some@Some.Some'])
    country: str = Field(examples=['México'])
    user_type: constants.UserType = Field(default=constants.UserType.STUDENT)
    phone_number: str   # pendiente utilizar phonenumber from pydantic.extramodels

    @field_validator('first_name', 'last_name')
    def std_name(cls, value: Any) -> BaseModel:
        value = value.capitalize()
        return value.strip()

    @field_validator('phone_number')
    def std_phone(cls, value: Any) -> BaseModel:
        return value.strip()


class UserCreateSchema(UserBaseSchema):
    re_password: str

    @model_validator(mode="before")
    def validate_passwords(cls, values):
        if values["password"] != values["re_password"]:
            raise HTTPException(
                detail="Passwords do not match.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not validate_password(values["password"]):
            raise HTTPException(
                status_code=400,
                detail="La contraseña debe tener de 5 a 10 caracteres, 1 letra mayúscula, 1 letra minúscula, 1 número, "
                       "1 signo (! @ # $ % & * . _) y no debe contener espacios",
            )

        return values


class UserUpdateSchema(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None


class UserResponseSchema(UserBaseSchema):
    password: ClassVar[str]


class UserListResponseSchema(BaseModel):
    data: list[UserBaseSchema]
    # password: ClassVar[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class UserAuthSchema(BaseModel):
    username: str
    password: str


class UserInDBSchema(UserBaseSchema):
    password: ClassVar[str]

    class Config:
        """
        Use SQLAlchemy to Pydantic
        """
        from_attributes = True


class UsersInDBSchema(BaseModel):
    usuarios: list[UserBaseSchema]
    # password: ClassVar[str]

    class Config:
        """
        Use SQLAlchemy to Pydantic
        """
        from_attributes = True
