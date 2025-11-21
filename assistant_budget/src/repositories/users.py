from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from assistant_budget.src.models.user import User
from assistant_budget.src.schemas.user_schema import UserCreate, UserUpdate
from assistant_budget.src.database import get_session


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.uuid == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def exists_by_email(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(
            select(User)
            .order_by(User.created_at)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            for key, value in user_data.dict(exclude_unset=True).items():
                setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
        return user


async def get_user_repository(
    db: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(db)