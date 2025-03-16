from fastapi import FastAPI

from src.modules.app_container import add_container

app = FastAPI()

add_container(app)
