from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from assistant_budget.src.models.expense_participant import ExpenseParticipant
from assistant_budget.src.schemas.expense_participant_schema import ExpenseParticipantCreate
from assistant_budget.src.database import get_session


class ExpenseParticipantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, participant_id: UUID) -> Optional[ExpenseParticipant]:
        result = await self.db.execute(
            select(ExpenseParticipant).where(ExpenseParticipant.uuid == participant_id)
        )
        return result.scalar_one_or_none()

    async def get_by_expense(self, expense_id: UUID) -> List[ExpenseParticipant]:
        result = await self.db.execute(
            select(ExpenseParticipant).where(ExpenseParticipant.expense_id == expense_id)
        )
        return result.scalars().all()

    async def create(self, data: ExpenseParticipantCreate) -> ExpenseParticipant:
        part = ExpenseParticipant(**data.dict())
        self.db.add(part)
        await self.db.commit()
        await self.db.refresh(part)
        return part

    async def delete(self, participant_id: UUID) -> Optional[ExpenseParticipant]:
        part = await self.get_by_id(participant_id)
        if part:
            await self.db.delete(part)
            await self.db.commit()
        return part


async def get_expense_participant_repository(
    db: AsyncSession = Depends(get_session),
) -> ExpenseParticipantRepository:
    return ExpenseParticipantRepository(db)