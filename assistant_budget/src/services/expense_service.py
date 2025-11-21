from fastapi import HTTPException
from uuid import UUID

from assistant_budget.src.repositories.expenses import ExpenseRepository
from assistant_budget.src.repositories.categories import CategoryRepository
from assistant_budget.src.repositories.users import UserRepository
from assistant_budget.src.schemas.expense_schema import ExpenseCreate, ExpenseUpdate


class ExpenseService:
    def __init__(
        self,
        repo: ExpenseRepository,
        users: UserRepository,
        categories: CategoryRepository,
    ):
        self.repo = repo
        self.users = users
        self.categories = categories

    async def get(self, expense_id: UUID):
        expense = await self.repo.get_by_id(expense_id)
        if not expense:
            raise HTTPException(404, "Expense not found")
        return expense

    async def get_by_user(self, user_id: UUID):
        return await self.repo.get_all_by_user(user_id)

    async def create(self, data: ExpenseCreate):
        # validate user exists
        if not await self.users.get_by_id(data.user_id):
            raise HTTPException(404, "User not found")

        # validate category exists
        if not await self.categories.get_by_id(data.category_id):
            raise HTTPException(404, "Category not found")

        return await self.repo.create(data)

    async def update(self, expense_id: UUID, data: ExpenseUpdate):
        updated = await self.repo.update(expense_id, data)
        if not updated:
            raise HTTPException(404, "Expense not found")
        return updated

    async def delete(self, expense_id: UUID):
        deleted = await self.repo.delete(expense_id)
        if not deleted:
            raise HTTPException(404, "Expense not found")
        return {"status": "deleted"}