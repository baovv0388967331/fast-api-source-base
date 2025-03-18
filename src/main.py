from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.databases.mysql import mysql_database
from src.modules.app_container import add_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = app
    await mysql_database.open_database()

    yield

    await mysql_database.close_database()


app = FastAPI(lifespan=lifespan)

add_container(app)
