from fastapi import HTTPException, status
from uuid import UUID

from assistant_budget.src.repositories.families import FamilyRepository
from assistant_budget.src.schemas.family_schema import FamilyCreate, FamilyUpdate


class FamilyService:
    def __init__(self, repository: FamilyRepository):
        self.repository = repository

    async def get(self, family_id: UUID):
        fam = await self.repository.get_by_id(family_id)
        if not fam:
            raise HTTPException(status_code=404, detail="Family not found")
        return fam

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, data: FamilyCreate):
        if await self.repository.exists_by_name(data.name):
            raise HTTPException(409, "Family name already exists")

        return await self.repository.create(data)

    async def update(self, family_id: UUID, data: FamilyUpdate):
        fam = await self.repository.update(
            family_id,
            data.dict(exclude_unset=True)
        )
        if not fam:
            raise HTTPException(404, "Family not found")
        return fam

    async def delete(self, family_id: UUID):
        fam = await self.repository.delete(family_id)
        if not fam:
            raise HTTPException(404, "Family not found")
        return {"status": "deleted"}