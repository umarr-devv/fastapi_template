import logging

from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from typing_extensions import Annotated

from api.v1.repository import *
from models import *
from services import *

from .manager import get_manager


async def get_user(
    token: Annotated[str, Header(...)],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="missing token for authorization",
        )

    try:
        data = JWTService.decode(token)
        id_, exp = data["sub"], data["exp"]

        user = await manager.users.by_id(id_=str(id_))
        if user:
            return user
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="token is expired"
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="invalid token"
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
