from typing import Any
from src.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id : Mapped[int] = mapped_column(
        primary_key=True
    )

    firstname : Mapped[str] = mapped_column()

    surname : Mapped[str] = mapped_column()

    email : Mapped[str] = mapped_column(
        unique=True
    )

    email : Mapped[str] = mapped_column(
        unique=True
    )

    date_of_creation : Mapped[datetime] = mapped_column(
        DateTime
    )

    def __init__(self, **kw: Any):
        super().__init__(**kw)