from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint
from .Category import Category

class Article(Base):
    __tablename__ = "articles"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    name : Mapped[str] = mapped_column()

    price : Mapped[int] = mapped_column()

    stock_quantity : Mapped[int] = mapped_column() 

    categories : Mapped[list["Category"]] = relationship(
        "Category",
        secondary="article_categories"
    )

    __table_args__ = (
        CheckConstraint("price >= 0"),
        CheckConstraint("stock_quantity >= 0")
    )

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    def __repr__(self) -> str:
        string = f"ID: {self.id}, "
        string += f"NAME: {self.name}, "
        string += f"STOCK: {self.stock_quantity}, "
        string += f"CATEGORIES: {self.categories}"
        return string