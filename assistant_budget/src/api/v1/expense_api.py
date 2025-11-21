from fastapi import APIRouter, Depends
from uuid import UUID

from assistant_budget.src.schemas.expense_schema import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from assistant_budget.src.repositories.expenses import ExpenseRepository, get_expense_repository
from assistant_budget.src.repositories.users import UserRepository, get_user_repository
from assistant_budget.src.repositories.categories import CategoryRepository, get_category_repository
from assistant_budget.src.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_service(
    repo: ExpenseRepository = Depends(get_expense_repository),
    users: UserRepository = Depends(get_user_repository),
    categories: CategoryRepository = Depends(get_category_repository),
) -> ExpenseService:
    return ExpenseService(repo, users, categories)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: UUID, service: ExpenseService = Depends(get_service)):
    return await service.get(expense_id)


@router.post("/", response_model=ExpenseResponse, status_code=201)
async def create_expense(data: ExpenseCreate, service: ExpenseService = Depends(get_service)):
    return await service.create(data)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: UUID,
    data: ExpenseUpdate,
    service: ExpenseService = Depends(get_service)
):
    return await service.update(expense_id, data)


@router.delete("/{expense_id}")
async def delete_expense(expense_id: UUID, service: ExpenseService = Depends(get_service)):
    return await service.delete(expense_id)