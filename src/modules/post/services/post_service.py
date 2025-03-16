from src.modules.post.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_post(self, user_id: str):
        print("users", user_id)
        return user_id
