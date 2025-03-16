from dependency_injector import containers, providers


class UserService:
    def send(self, name: str):
        print(f"My name is {name}")


class Container(containers.DeclarativeContainer):
    user_service = providers.Singleton(UserService)


container = Container()
user_service = container.user_service()

user_service.send("bao")
