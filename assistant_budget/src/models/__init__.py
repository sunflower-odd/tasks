# from sqlalchemy.orm import relationship

from .model_base import Base, BaseModelMixin

from .category import Category
from .expense import Expense
from .expense_participant import ExpenseParticipant
from .family import Family
from .user import User

# Posts.category = relationship("Categories", back_populates="posts")
# Category.posts = relationship("Posts", back_populates="category")

__all__ = ["Base", "BaseModelMixin", "Category", "Expense", "ExpenseParticipant", "Family", "User"]