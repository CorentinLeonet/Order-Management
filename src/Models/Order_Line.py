from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint

class Order_Line(Base):
    __tablename__ = "order_lines"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id : Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    article_id : Mapped[int] = mapped_column(
        ForeignKey("articles.id")
    )

    quantity : Mapped[int] = mapped_column(
        CheckConstraint("quantity >= 0")
    )

    unit_price : Mapped[int] = mapped_column(
        CheckConstraint("unit_price >= 0")
    )
    article = relationship('Article')

    def __init__(self, **kw: Any):
        super().__init__(**kw)
