from sqlalchemy import Column, String, Integer, text
from sqlalchemy.orm import relationship
from app.config.database.base_class import Base
from app.utils.datetime_custom_type import CustomDateTime


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone_number = Column(Integer, nullable=False)
    user_type = Column(String, nullable=False)
    created_at = Column(CustomDateTime,
                        nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))

    user_course = relationship("UserCourse", back_populates="user")

    def __repr__(self) -> str:
        return (f'<{self.id},'
                f'{self.username},'
                f'{self.first_name},'
                f'{self.last_name},'
                f'{self.email},'
                f'{self.country}>'
                f'{self.phone_number},'
                f'{self.user_type}>'
                )
