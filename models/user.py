from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from db.base import Base


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(length=64), unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(
        String(length=255), nullable=True
    )
    password: Mapped[str] = mapped_column(
        nullable=False
    )

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.username}>'
