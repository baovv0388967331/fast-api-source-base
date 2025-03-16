from dependency_injector import containers, providers

from src.modules.user.repositories.user_repository import UserRepository
from src.modules.user.services.user_service import UserService


class UserContainer(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepository)
    user_service = providers.Singleton(UserService, user_repository=user_repository)
