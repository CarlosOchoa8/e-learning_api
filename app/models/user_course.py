from sqlalchemy import text, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database.base_class import Base
from app.utils.datetime_custom_type import CustomDateTime


class UserCourse(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    started_at = Column(CustomDateTime,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates='user_course')
    course = relationship("Course", back_populates='user_course')
