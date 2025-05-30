import logging

from aiocache import cached
from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.exc import IntegrityError
from typing_extensions import Annotated

from deps import get_repositories, get_user
from models import User
from repositories import RepositoryManager
from schemes import UserScheme, CreateUserScheme, TokenScheme, LoginUserScheme, TokenPayloadScheme
from services import HashService, JWTService
from asyncio import sleep

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    path='',
    response_model=UserScheme
)
async def on_create_user(
        data: Annotated[CreateUserScheme, Body(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
):
    try:
        data.password = HashService.to_hash(data.password)
        user = await rep_manager.user.new(**data.model_dump())
        await rep_manager.commit()
        return user
    except IntegrityError as exc:
        logging.info(exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'invalid data'
        )
    except Exception as exc:
        logging.warning(exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get(
    path='',
    response_model=list[UserScheme]
)
@cached(ttl=60, key='all_users')
async def on_get_users(
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
):
    return await rep_manager.user.all()


@router.post(
    path='/login',
    response_model=TokenScheme
)
async def on_user_login(
        data: Annotated[LoginUserScheme, Body(...)],
        rep_manager: Annotated[RepositoryManager, Depends(get_repositories)]
):
    user = await rep_manager.user.by_filter_one(
        username=data.username
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    if HashService.check_hash(data.password, user.password):
        payload = TokenPayloadScheme(
            sub=str(user.id),
            username=user.username
        )
        access_token = JWTService.encode(
            payload=payload.model_dump()
        )
        return TokenScheme(
            access_token=access_token
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid password'
        )


@router.get(
    path='/login',
    response_model=UserScheme,
)
async def on_get_user(
        user: Annotated[User, Depends(get_user)]
):
    return user
