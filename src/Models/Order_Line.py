from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint, event, inspect

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

@event.listens_for(Order_Line, 'before_delete')
def restock_on_line_delete(mapper, connection, target):
    target.article.stock_quantity += target.quantity

@event.listens_for(Order_Line, 'before_update')
def restock_on_line_update(mapper, connection, target):
    history = inspect(target).attrs.quantity.history
    if history.deleted:
        old_quantity = history.deleted[0]
        target.article.stock_quantity += old_quantity - target.quantity