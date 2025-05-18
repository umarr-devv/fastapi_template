from typing_extensions import Optional

from sqlalchemy import select

from models import User

from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User
