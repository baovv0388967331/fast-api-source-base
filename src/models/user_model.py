from sqlalchemy import Column, Integer, String

from src.databases.mysql import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
