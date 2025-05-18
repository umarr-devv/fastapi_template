import logging

from fastapi import Depends, Header, HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from typing_extensions import Annotated

from deps.repository import get_repositories
from models import User
from repositories import RepositoryManager
from services import JWTService


async def get_user(
        authorization: Annotated[str, Header(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
) -> User:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='missing token for authorization'
        )
    if authorization.startswith('Bearer'):
        _, token = authorization.split(' ')
        try:
            data = JWTService.decode(token)
            id_, exp = data['sub'], data['exp']

            user = await rep_manager.user.by_id(int(id_))
            if user:
                return user
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='token is expired'
            )
        except InvalidSignatureError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='invalid token'
            )
        except Exception as exc:
            logging.warning(exc)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )
