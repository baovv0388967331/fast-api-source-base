from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.databases.mysql import mysql_database
from src.modules.app_container import add_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = app
    mysql_database.init_db()
    await mysql_database.check_db_session()
    yield
    await mysql_database.close()


app = FastAPI(lifespan=lifespan)

add_container(app)
