from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from assistant_budget.src.configs.app import settings


DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/postgres" #"postgresql+psycopg2://postgres:pass@localhost:5432/postgres"

engine = create_async_engine(settings.db.dsl, echo=True)

async_sesion_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sesion_maker() as session:
        try:
            yield session
        finally:
            await session.close()



