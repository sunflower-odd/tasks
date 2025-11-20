from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from assistant_budget.src.models.model_base import Base, BaseModelMixin


class User(Base, BaseModelMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="user")
    expenses_participated = relationship("ExpenseParticipant", back_populates="user")

    def __repr__(self) -> str:
        return f"User(uuid={self.uuid}, name={self.name})"

    def to_dict(self) -> dict[str, any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }