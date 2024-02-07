from datetime import datetime
import pendulum
from pydantic import BaseModel, Field


class LessonProgressBase(BaseModel):
    user_id: int | None = None
    lesson_id: int
    lesson_completed: bool


class LessonProgressCreate(LessonProgressBase):
    updated_at: datetime = Field(
        default_factory=lambda: pendulum.now(pendulum.UTC)
    )


class LessonProgressUpdate(LessonProgressBase):
    pass


class LessonProgressInDB(BaseModel):
    lesson_completed: bool

