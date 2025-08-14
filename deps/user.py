import logging

from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from typing_extensions import Annotated

from deps.repository import get_rep_manager
from models import User
from repositories import RepositoryManager
from services import JWTService


async def get_user(
    jwt_token: Annotated[str, Header(...)],
    rep_manager: Annotated[RepositoryManager, Depends(get_rep_manager)],
) -> User:
    if not jwt_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="missing token for authorization",
        )

    try:
        data = JWTService.decode(jwt_token)
        id_, exp = data["sub"], data["exp"]

        user = await rep_manager.by_id(User, id_=int(id_))
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
    except Exception as exc:
        logging.warning(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
