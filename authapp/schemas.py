import uuid
from typing import Optional, Literal, List
from fastapi_users import schemas
from pydantic import BaseModel

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class Query(BaseModel):
    text: str

class Data(BaseModel):
    urls: List[str]
