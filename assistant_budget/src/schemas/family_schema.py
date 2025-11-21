from uuid import UUID
from typing import Optional
from pydantic import BaseModel, constr

class FamilyBase(BaseModel):
    name: constr(min_length=1, max_length=100)


class FamilyCreate(FamilyBase):
    pass

class FamilyUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None

class FamilyResponse(FamilyBase):
    uuid: UUID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True