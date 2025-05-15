from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class File(Base):
    __tablename__ = 'files'

    file_name: Mapped[str] = mapped_column(
        unique=True, nullable=False
    )
    file_type: Mapped[str] = mapped_column(
        nullable=False
    )

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.file_name}>'
