from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, event, Enum as EnumSQL
from datetime import datetime
from enum import Enum

class Order_Status_Enum(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    client_id : Mapped[int] = mapped_column(
        ForeignKey("clients.id")
    )

    date_ordered : Mapped[datetime] = mapped_column(
        DateTime
    )

    date_shipped : Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    date_recieved : Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    status : Mapped[str] = mapped_column()
    # status : Mapped[Order_Status_Enum] = mapped_column(
    #     EnumSQL(Order_Status_Enum, name="status")
    #     nullable = False
    #     unique = False
    # )

    order_lines = relationship('Order_Line')
    client = relationship("Client")
    
    def __init__(self, **kw: Any):
        super().__init__(**kw)

@event.listens_for(Order, 'before_update')
def restock_on_cancel(mapper, connection, target):
    if target.status == Order_Status_Enum.CANCELLED.value:
        for line in target.order_lines:
            line.article.stock_quantity += line.quantity