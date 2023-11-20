from pydantic import Field, BaseModel


class LessonBaseSchema(BaseModel):
    name: str = Field(min_length=5)
    content: str
    course_id: int
    description: str = Field(min_length=5)


class LessonCreateSchema(LessonBaseSchema):
    pass


class LessonUpdateSchema(LessonBaseSchema):
    pass


class LessonInDBSchema(LessonBaseSchema):
    id: int

    class Config:
        """
        Use SQLAlchemy to Pydantic
        """
        from_attributes = True


class LessonsInDBSchema(BaseModel):
    courses: list[LessonInDBSchema]
