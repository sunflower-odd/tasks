from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class ExpenseParticipantBase(BaseModel):
    expense_id: UUID
    user_id: UUID


class ExpenseParticipantCreate(ExpenseParticipantBase):
    pass

class ExpenseParticipantUpdate(BaseModel):
    expense_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class ExpenseParticipantResponse(ExpenseParticipantBase):
    uuid: UUID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True