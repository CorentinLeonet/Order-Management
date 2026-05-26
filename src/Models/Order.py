from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Enum as EnumSQL, CheckConstraint
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

    date_confirmed : Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    date_shipped : Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True
    )

    status : Mapped[str] = mapped_column()

    __table_args__ = (
        CheckConstraint("date_confirmed >= date_ordered"),
        CheckConstraint("date_shipped >= date_confirmed")
    )

    order_lines = relationship('Order_Line')
    client = relationship("Client")
    
    def __init__(self, **kw: Any):
        super().__init__(**kw)