from sqlalchemy import ForeignKey, String, Float, Boolean, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any
from assistant_budget.src.models.model_base import Base
from assistant_budget.src.models.model_base import BaseModelMixin
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

class Category(Base, BaseModelMixin):
    __tablename__ = "expenses_categories"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    desc: Mapped[str] = mapped_column(String,  nullable=False)

    expenses = relationship("Expense", back_populates="category")
    def __repr__(self) -> str:
        return f"uuid - {self.uuid}, name - {self.name}, desc - {self.desc}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "desc": self.desc,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


async def create_db():
    engine = create_async_engine(
        "postgresql+asyncpg://user:password@localhost:5432/postgres"
    )

    async with engine.begin() as connection:
        pass
        # await connection.run_sync(Base.metadata.drop_all)
        # await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_db())