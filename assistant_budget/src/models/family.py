from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from assistant_budget.src.models.model_base import Base, BaseModelMixin


class Family(Base, BaseModelMixin):
    __tablename__ = "families"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Family(uuid={self.uuid}, name={self.name})"

    def to_dict(self) -> dict[str, any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }