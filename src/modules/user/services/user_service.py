from src.models.user_model import UserModel
from src.modules.user.dto.requests.user_request import UserRequest
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_users(self):
        users = await self.user_repository.find_all()

        return users

    async def get_user_by_id(self, user_id: str):
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise Exception("User not found!")

        return user

    async def create_user(self, user: UserRequest):
        user_model = UserModel(**user.__dict__)
        new_user = await self.user_repository.create(user_model)

        return new_user

    async def update_user(self, user_id: int, user: UserRequest):
        new_user = await self.user_repository.update(user_id, user)

        return new_user

    async def delete_user(self, user_id: str):
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise Exception("User not found!")

        user = await self.user_repository.delete(user)

        return user
