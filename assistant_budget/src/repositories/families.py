from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from assistant_budget.src.models.family import Family
from assistant_budget.src.schemas.family_schema import FamilyCreate, FamilyUpdate
from assistant_budget.src.database import get_session


class FamilyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, family_id: UUID) -> Optional[Family]:
        result = await self.db.execute(select(Family).where(Family.uuid == family_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Family]:
        result = await self.db.execute(select(Family).where(Family.name == name))
        return result.scalar_one_or_none()

    async def exists_by_name(self, name: str) -> bool:
        return await self.get_by_name(name) is not None

    async def get_all(self) -> List[Family]:
        result = await self.db.execute(select(Family).order_by(Family.created_at))
        return result.scalars().all()

    async def create(self, family_data: FamilyCreate) -> Family:
        fam = Family(**family_data.dict())
        self.db.add(fam)
        await self.db.commit()
        await self.db.refresh(fam)
        return fam

    async def update(self, family_id: UUID, family_data: FamilyUpdate) -> Optional[Family]:
        fam = await self.get_by_id(family_id)
        if fam:
            for key, value in family_data.dict(exclude_unset=True).items():
                setattr(fam, key, value)
            await self.db.commit()
            await self.db.refresh(fam)
        return fam

    async def delete(self, family_id: UUID) -> Optional[Family]:
        fam = await self.get_by_id(family_id)
        if fam:
            await self.db.delete(fam)
            await self.db.commit()
        return fam


async def get_family_repository(
    db: AsyncSession = Depends(get_session),
) -> FamilyRepository:
    return FamilyRepository(db)