from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Article_Category(Base):
    __tablename__ = "article_categories"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    article_id : Mapped[int] = mapped_column(
        ForeignKey("articles.id")
    )

    category_id : Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    
