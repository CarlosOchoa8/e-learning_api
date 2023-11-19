from typing import Any

from pydantic import Field, BaseModel, validator, root_validator, ValidationError, model_validator
import json


class BaseModelValidateToJSON(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        """Validate to json"""
        return cls(**json.loads(value)) if isinstance(value, str) else value


class LessonFileBaseSchema(BaseModel):
    name: str = Field(min_length=5)
    lesson_id: int
    description: str = Field(min_length=10)


class LessonFileCreateSchema(LessonFileBaseSchema):
    # name: str | dict[str, Any] = Field(min_length=5)
    # lesson_id: int | dict[str, Any]

    # @root_validator(pre=True)
    # def parse_json(cls, value):
    #     return cls(**json.loads(value)) if isinstance(value, str) else value
    @model_validator(mode='before')
    def parse_json(cls, value):
        return cls(**json.loads(value)) if isinstance(value, str) else value


class LessonFileUpdateSchema(LessonFileBaseSchema):
    pass


class LessonFileInDBSchema(LessonFileBaseSchema):
    id: int

    class Config:
        """
        Use SQLAlchemy to Pydantic
        """
        from_attributes = True


class LessonFilesInDBSchema(BaseModel):
    courses: list[LessonFileInDBSchema]
