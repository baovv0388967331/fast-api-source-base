from fastapi import FastAPI

from src.modules.user.controllers import user_controller
from src.modules.user.user_container import UserContainer
from src.utils.helper import extendContainers


def add_container(app: FastAPI):
    app.container = extendContainers([UserContainer])
    controllers = [user_controller]

    app.container.wire(modules=controllers)

    for controller in controllers:
        app.include_router(controller.router)
