from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database.base_class import Base


class LessonFile(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    lesson_id = Column(Integer, ForeignKey('lesson.id'))

    lesson = relationship('Lesson', back_populates='lesson_file')

    def __repr__(self) -> str:
        return (f'<{self.id},'
                f'{self.name},'
                f'{self.file}>'
                )
