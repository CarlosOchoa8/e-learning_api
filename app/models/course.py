from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
from app.config.database.base_class import Base


class Course(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    teacher = Column(String, nullable=True)
    description = Column(String, nullable=False)

    lesson = relationship('Lesson', back_populates='course')

    def __repr__(self) -> str:
        return (f'<{self.id},'
                f'{self.name},'
                f'{self.teacher}>'
                )
