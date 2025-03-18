# from dependency_injector import containers, providers


# class UserService:
#     def send(self, name: str):
#         print(f"My name is {name}")


# class Container(containers.DeclarativeContainer):
#     user_service = providers.Singleton(UserService)


# container = Container()
# user_service = container.user_service()

# user_service.send("bao")


from typing import TypeVar

T = TypeVar("T")


def first_elements(items: list[T]) -> T:
    return items[0]


numbers = [1, 2, 3]
first_number = first_elements(numbers)

names = ["Alice", "Bob", "Charlie"]
first_name = first_elements(names)

print("first_number", first_number)
print("first_name", first_name)
