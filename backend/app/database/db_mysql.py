
from core.conf import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

# SQLALCHEMY_DATABASE_URL = (
#     f'mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
#     f'{settings.DB_PORT}/{settings.DB_DATABASE}?charset={settings.DB_CHARSET}'
# )
SQLALCHEMY_DATABASE_URL = (
    f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:'
    f'{settings.DB_PORT}/{settings.DB_DATABASE}'
)

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DB_ECHO, future=True, pool_pre_ping=True)


async def create_table():
    """데이터베이스 테이블 만들기"""
    async with async_engine.begin() as coon:
        await coon.run_sync(SQLModel.metadata.create_all)
