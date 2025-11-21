from fastapi import HTTPException, status
from uuid import UUID

from assistant_budget.src.repositories.users import UserRepository
from assistant_budget.src.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get(self, user_id: UUID):
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_all(self):
        return await self.repository.get_all()

    async def create(self, data: UserCreate):
        return await self.repository.create(data)

    async def update(self, user_id: UUID, data: UserUpdate):
        updated = await self.repository.update(
            user_id, data.dict(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return updated

    async def delete(self, user_id: UUID):
        deleted = await self.repository.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "deleted"}