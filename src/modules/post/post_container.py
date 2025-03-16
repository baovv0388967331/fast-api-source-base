from dependency_injector import containers, providers

from src.modules.post.repositories.post_repository import PostRepository
from src.modules.post.services.post_service import PostService


class PostContainer(containers.DeclarativeContainer):
    post_repository = providers.Singleton(PostRepository)
    post_service = providers.Singleton(PostService, post_repository=post_repository)
