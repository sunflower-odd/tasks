from typing import List, Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from assistant_budget.src.models.category import Category
from assistant_budget.src.schemas.category_schema import CategoryCreate, CategoryUpdate
from assistant_budget.src.database import get_session


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        result = await self.db.execute(select(Category).where(Category.uuid == category_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.db.execute(select(Category).where(Category.name == name))
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        return await self.get_by_name(name) is not None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.db.execute(select(Category).order_by(Category.name).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, category_data: CategoryCreate) -> Category:
        category = Category(**category_data.dict())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category_id: UUID, category_data: CategoryUpdate) -> Optional[Category]:
        category = await self.get_by_id(category_id)
        if category:
            for key, value in category_data.dict(exclude_unset=True).items():
                setattr(category, key, value)
            await self.db.commit()
            await self.db.refresh(category)
        return category

    async def delete(self, category_id: UUID) -> Optional[Category]:
        category = await self.get_by_id(category_id)
        if category:
            await self.db.delete(category)
            await self.db.commit()
        return category

    async def search_by_name(self, name_pattern: str, skip: int = 0, limit: int = 100) -> List[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.name.ilike(f"%{name_pattern}%"))
            .order_by(Category.name)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


async def get_category_repository(db: AsyncSession = Depends(get_session)) -> CategoryRepository:
    return CategoryRepository(db)