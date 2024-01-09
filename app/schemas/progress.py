from pydantic import BaseModel


class LessonProgressBase(BaseModel):
    user_id: int | None = None
    lesson_id: int
    lesson_completed: bool


class LessonProgressCreate(LessonProgressBase):
    pass


class LessonProgressUpdate(LessonProgressBase):
    pass


class LessonProgressInDB(BaseModel):
    lesson_completed: bool
