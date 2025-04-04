from src.models.user_model import UserModel
from src.modules.user.dto.requests.user_request import UserRequest
from src.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user(self, user_id: str):
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

    async def transaction(self, user: UserRequest):
        async for session in self.user_repository.get_session():
            try:
                new_user = UserModel(**user.__dict__)
                session.add(new_user)
                await session.commit()
            except Exception as e:
                print(f"Error: {e}, transaction rolled back")
                await session.rollback()
            finally:
                await session.close()
