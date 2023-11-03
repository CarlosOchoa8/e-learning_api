from sqlalchemy import Column, String, Integer
from app.config.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(Integer, nullable=False)
    user_type = Column(String, nullable=False)

    def __repr__(self) -> str:
        return (f'<{self.id},'
                f'{self.username},'
                f'{self.first_name},'
                f'{self.last_name},'
                f'{self.email},'
                f'{self.phone_number},'
                f'{self.user_type}>'
                )
