from sqlalchemy import String, Float, Boolean, Date, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import Any, Optional
import uuid

from assistant_budget.src.models.model_base import Base, BaseModelMixin


class Expense(Base, BaseModelMixin):
    __tablename__ = "expenses"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default="RUB",
    )

    # UUID foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid"),
        nullable=False,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("expenses_categories.uuid"),
        nullable=False,
    )

    tag: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    shared: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    date: Mapped[Date] = mapped_column(Date, nullable=False)

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    participants = relationship("ExpenseParticipant", back_populates="expense")

    def __repr__(self) -> str:
        return (
            f"Expense(uuid={self.uuid}, name={self.name}, amount={self.amount}, "
            f"date={self.date}, shared={self.shared})"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "amount": self.amount,
            "currency": self.currency,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "tag": self.tag,
            "shared": self.shared,
            "date": self.date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }