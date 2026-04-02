from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status

from api.v1.dependencies import *
from api.v1.repository import *
from api.v1.schemas import *
from models import *
from services.hash import HashService
from services.jwt import JWTService

router = APIRouter(prefix="/users", tags=["users"])


@router.get(path="", response_model=list[UserSchema], operation_id="get_users")
async def on_get_users(
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    return await manager.users.get_users()


@router.post(path="", response_model=UserSchema, operation_id="create_user")
async def on_create_user(
    data: Annotated[CreateUserSchema, Body()],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    user = await manager.users.by_username(data.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with this already exists.",
        )
    return await manager.users.create_user(data)


@router.patch(path="", response_model=UserSchema, operation_id="patch_user")
async def on_patch_user(
    user: Annotated[User, Depends(get_user)],
    data: Annotated[PatchUserSchema, Body()],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    return await manager.users.patch_user(user, data)


@router.delete(path="", response_model=UserSchema, operation_id="delete_user")
async def on_delete_user(
    user: Annotated[User, Depends(get_user)],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    return manager.users.delete(user)


@router.patch(
    path="/password",
    response_model=UserSchema,
    operation_id="patch_user_password",
)
async def on_patch_user_password(
    user: Annotated[User, Depends(get_user)],
    data: Annotated[PatchUserPasswordSchema, Body()],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    return await manager.users.patch_user_password(user, data)


@router.post(path="/login", response_model=TokenSchema, operation_id="login_user")
async def on_login_user(
    data: Annotated[LoginUserSchema, Body()],
    manager: Annotated[RepositoriesManager, Depends(get_manager)],
):
    user = await manager.users.by_username(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    if not HashService.check_hash(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid password"
        )
    payload = TokenPayloadSchema(sub=user.id)
    access_token = JWTService.encode(payload=payload.model_dump())
    return TokenSchema(access_token=access_token)


@router.get(path="/me", response_model=UserSchema, operation_id="get_user_me")
async def on_get_user_me(user: Annotated[User, Depends(get_user)]):
    return user
