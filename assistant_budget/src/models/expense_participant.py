from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import Any
import uuid

from assistant_budget.src.models.model_base import Base, BaseModelMixin


class ExpenseParticipant(Base, BaseModelMixin):
    __tablename__ = "expense_participants"

    # UUID PK наследуется из BaseModelMixin

    expense_id = Column(PG_UUID(as_uuid=True), ForeignKey("expenses.uuid"), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)

    # Связи
    expense = relationship("Expense", back_populates="participants")
    user = relationship("User", back_populates="expenses_participated")

    def __repr__(self) -> str:
        return f"ExpenseParticipant(uuid={self.uuid}, expense_id={self.expense_id}, user_id={self.user_id})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "expense_id": self.expense_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }