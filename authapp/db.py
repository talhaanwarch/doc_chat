from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .utils import get_settings

# Retrieve the PostgreSQL credentials from environment variables
db_host = get_settings().postgres_host
db_port = get_settings().postgres_port
db_name = get_settings().postgres_db
db_user = get_settings().postgres_user
db_password = get_settings().postgres_password

# Construct the PostgreSQL URL
DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)