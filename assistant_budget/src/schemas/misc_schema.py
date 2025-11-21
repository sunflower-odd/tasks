from uuid import UUID
from typing import Optional

from pydantic import BaseModel

class BudgetSchema(BaseModel):
    status: str
    version: str