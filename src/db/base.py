from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid6 import uuid7


class Base(DeclarativeBase):
    __abstract__ = True

    @staticmethod
    def utc_now() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def uuid() -> str:
        return str(uuid7())

    id: Mapped[str] = mapped_column(unique=True, primary_key=True, default=uuid)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.id}>"
