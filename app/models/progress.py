from app.config.database.base_class import Base
from sqlalchemy import Text, Integer, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship


class Progress(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    lesson_completed = Column(Boolean, nullable=False)
    # course_id = Column(Integer, nullable=False) revisdar si es lesson_id o course_id

    lesson = relationship("Lesson", back_populates="lesson_progress")
