from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.modules.post.post_container import PostContainer
from src.modules.post.services.post_service import PostService

router = APIRouter()


@router.get("/posts/{user_id}", tags=["Post"])
@inject
def get_user_by_id(
    user_id: str,
    post_service: PostService = Depends(Provide[PostContainer.post_service]),
):
    post_service.get_post(user_id=user_id)

    return {}
