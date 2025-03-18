from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.modules.user.dto.requests.user_request import UserRequest
from src.modules.user.services.user_service import UserService
from src.modules.user.user_container import UserContainer

router = APIRouter()


@router.get("/users/{user_id}", tags=["User"])
@inject
async def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    user = await user_service.get_user(user_id=user_id)

    return user


@router.post("/users", tags=["User"])
@inject
async def create_user(
    user: UserRequest,
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    user = await user_service.create_user(user)

    return user


@router.put("/users/{user_id}", tags=["User"])
@inject
async def update_user(
    user_id: int,
    user: UserRequest,
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    user = await user_service.update_user(user_id, user)

    return user
