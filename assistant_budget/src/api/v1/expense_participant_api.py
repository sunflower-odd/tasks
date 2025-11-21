from fastapi import APIRouter, Depends
from uuid import UUID

from assistant_budget.src.schemas.expense_participant_schema import (
    ExpenseParticipantCreate,
    ExpenseParticipantResponse
)
from assistant_budget.src.repositories.expense_participants import (
    ExpenseParticipantRepository,
    get_expense_participant_repository
)
from assistant_budget.src.repositories.expenses import get_expense_repository, ExpenseRepository
from assistant_budget.src.repositories.users import get_user_repository, UserRepository
from assistant_budget.src.services.expense_participant_service import ExpenseParticipantService

router = APIRouter(prefix="/expense-participants", tags=["Expense Participants"])


def get_service(
    repo: ExpenseParticipantRepository = Depends(get_expense_participant_repository),
    users: UserRepository = Depends(get_user_repository),
    expenses: ExpenseRepository = Depends(get_expense_repository),
) -> ExpenseParticipantService:
    return ExpenseParticipantService(repo, users, expenses)


@router.post("/", response_model=ExpenseParticipantResponse, status_code=201)
async def add_participant(
    data: ExpenseParticipantCreate,
    service: ExpenseParticipantService = Depends(get_service)
):
    return await service.add(data)


@router.delete("/{participant_id}")
async def delete_participant(
    participant_id: UUID,
    service: ExpenseParticipantService = Depends(get_service)
):
    return await service.delete(participant_id)