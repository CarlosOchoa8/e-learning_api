from datetime import datetime

import pendulum
from pydantic import Field, BaseModel, PositiveInt


class UserCourseBaseSchema(BaseModel):
    user_id: PositiveInt
    course_id: PositiveInt
    completed: bool
    started_at: datetime = Field(
        default_factory=lambda: pendulum.now(pendulum.UTC)
    )


class UserCourseCreateSchema(UserCourseBaseSchema):
    pass


class UserCourseUpdateSchema(UserCourseBaseSchema):
    pass
