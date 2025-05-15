from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @staticmethod
    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)

    id: Mapped[int] = mapped_column(
        autoincrement=True, unique=True, primary_key=True
    )
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.id}>'
