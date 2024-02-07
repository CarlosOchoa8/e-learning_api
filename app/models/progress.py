from app.config.database.base_class import Base
from sqlalchemy import Integer, Boolean, Column, ForeignKey, text
from sqlalchemy.orm import relationship

from app.utils.datetime_custom_type import CustomDateTime


class Progress(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    lesson_id = Column(Integer, ForeignKey("lesson.id"))
    lesson_completed = Column(Boolean, nullable=False)
    # course_id = Column(Integer, nullable=False) revisdar si es lesson_id o course_id
    updated_at = Column(CustomDateTime,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    lesson = relationship("Lesson", back_populates="lesson_progress")
