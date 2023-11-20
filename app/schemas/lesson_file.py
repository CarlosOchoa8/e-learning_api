import json
from typing import ClassVar
from pydantic import Field, BaseModel, model_validator


class LessonFileBaseSchema(BaseModel):
    name: str = Field(min_length=5)
    lesson_id: int
    description: str = Field(min_length=10)


class LessonFileCreateSchema(LessonFileBaseSchema):
    @model_validator(mode='before')
    def parse_json(cls, value):
        return cls(**json.loads(value)) if isinstance(value, str) else value


class LessonFileUpdateSchema(LessonFileBaseSchema):
    lesson_id: ClassVar[int]


class LessonFileInDBSchema(LessonFileBaseSchema):
    id: int
    file: str

    class Config:
        """
        Use SQLAlchemy to Pydantic
        """
        from_attributes = True


class LessonFilesInDBSchema(BaseModel):
    files: list[LessonFileInDBSchema]
