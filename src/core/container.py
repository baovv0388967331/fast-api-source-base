from types import ModuleType

from dependency_injector import containers


class FactoryContainer(containers.DeclarativeContainer):
    controllers: list[ModuleType] = []

    @classmethod
    def add_controllers(cls, controllers: list[ModuleType]):
        cls.controllers = controllers
