from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database.base_class import Base


class Lesson(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    content = Column(Integer, nullable=False)
    description = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'))

    course = relationship("Course", back_populates='lesson')
    lesson_file = relationship("LessonFile", back_populates='lesson')
    lesson_progress = relationship("Progress", back_populates="lesson")

    def __repr__(self) -> str:
        return (f'<{self.id},'
                f'{self.name},'
                f'{self.description}>'
                )
