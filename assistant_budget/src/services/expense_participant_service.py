from fastapi import HTTPException
from uuid import UUID

from assistant_budget.src.repositories.expense_participants import ExpenseParticipantRepository
from assistant_budget.src.repositories.users import UserRepository
from assistant_budget.src.repositories.expenses import ExpenseRepository
from assistant_budget.src.schemas.expense_participant_schema import ExpenseParticipantCreate


class ExpenseParticipantService:
    def __init__(
        self,
        repo: ExpenseParticipantRepository,
        users: UserRepository,
        expenses: ExpenseRepository
    ):
        self.repo = repo
        self.users = users
        self.expenses = expenses

    async def get(self, participant_id: UUID):
        part = await self.repo.get_by_id(participant_id)
        if not part:
            raise HTTPException(404, "Participant not found")
        return part

    async def add(self, data: ExpenseParticipantCreate):
        if not await self.users.get_by_id(data.user_id):
            raise HTTPException(404, "User not found")

        if not await self.expenses.get_by_id(data.expense_id):
            raise HTTPException(404, "Expense not found")

        return await self.repo.create(data)

    async def delete(self, participant_id: UUID):
        deleted = await self.repo.delete(participant_id)
        if not deleted:
            raise HTTPException(404, "Participant not found")
        return {"status": "deleted"}