from uuid import UUID
from typing import Optional
from datetime import date
from pydantic import BaseModel, constr, condecimal

class ExpenseBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    amount: condecimal(gt=0)
    currency: Optional[str] = "RUB"
    category_id: UUID
    tag: Optional[str] = None
    shared: Optional[bool] = False
    date: date

class ExpenseCreate(ExpenseBase):
    user_id: UUID

class ExpenseUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    amount: Optional[condecimal(gt=0)] = None
    currency: Optional[str] = None
    category_id: Optional[UUID] = None
    tag: Optional[str] = None
    shared: Optional[bool] = None
    date: Optional[date] = None

class ExpenseResponse(ExpenseBase):
    uuid: UUID
    user_id: UUID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True