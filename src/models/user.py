from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import MappedColumn, mapped_column

from src.service.database import Base


class User(Base):
    __tablename__ = 'users'

    id: MappedColumn[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    create_on: MappedColumn[datetime] = mapped_column(DateTime, default=datetime.now)
    update_on: MappedColumn[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'table: {self.__tablename__} ID: {self.id}'
