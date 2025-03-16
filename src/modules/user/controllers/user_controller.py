from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.modules.user.services.user_service import UserService
from src.modules.user.user_container import UserContainer

router = APIRouter()


@router.get("/users/{user_id}", tags=["User"])
@inject
def get_user_by_id(
    user_id: str,
    user_service: UserService = Depends(Provide[UserContainer.user_service]),
):
    user_service.get_user(user_id=user_id)

    return {}
