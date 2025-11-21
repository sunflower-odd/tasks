from typing import Optional, List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from assistant_budget.src.models.expense import Expense
from assistant_budget.src.schemas.expense_schema import ExpenseCreate, ExpenseUpdate
from assistant_budget.src.database import get_session


class ExpenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, expense_id: UUID) -> Optional[Expense]:
        result = await self.db.execute(
            select(Expense).where(Expense.uuid == expense_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(self, user_id: UUID) -> List[Expense]:
        result = await self.db.execute(
            select(Expense).where(Expense.user_id == user_id)
        )
        return result.scalars().all()

    async def get_all_by_family(self, family_id: UUID) -> List[Expense]:
        result = await self.db.execute(
            select(Expense).where(Expense.family_id == family_id)
        )
        return result.scalars().all()

    async def create(self, data: ExpenseCreate) -> Expense:
        expense = Expense(**data.dict())
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def update(
        self, expense_id: UUID, data: ExpenseUpdate
    ) -> Optional[Expense]:
        expense = await self.get_by_id(expense_id)
        if expense:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(expense, key, value)
            await self.db.commit()
            await self.db.refresh(expense)
        return expense

    async def delete(self, expense_id: UUID) -> Optional[Expense]:
        expense = await self.get_by_id(expense_id)
        if expense:
            await self.db.delete(expense)
            await self.db.commit()
        return expense


async def get_expense_repository(
    db: AsyncSession = Depends(get_session),
) -> ExpenseRepository:
    return ExpenseRepository(db)