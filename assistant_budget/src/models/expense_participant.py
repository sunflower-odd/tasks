from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
import uuid

from assistant_budget.src.models.model_base import Base, BaseModelMixin


class ExpenseParticipant(Base, BaseModelMixin):
    __tablename__ = "expense_participants"

    # UUID PK наследуется из BaseModelMixin, отдельный id не нужен

    expense_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("expenses.uuid"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.uuid"),
        nullable=False,
    )

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