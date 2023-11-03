from typing import Any, ClassVar
from pydantic import Field, BaseModel, EmailStr, field_validator
from app.utils import constants


class UserBaseSchema(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    first_name: str = Field(min_length=5, max_length=50, examples=['Some First Name'])
    last_name: str = Field(min_length=5, max_length=50, examples=['Some Last Name'])
    email: EmailStr = Field(examples=['Some@Some.Some'])
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
    pass


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
